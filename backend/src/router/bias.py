from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.utils.bias_detection import (
    NewsScrape,
    BaseURL,
    SourceChecker,
    SentenceClaimDetector,
    BiasDetector,
    NBScore,
)

from pathlib import Path

# Initialize router
bias_router = APIRouter()

# Load models and data (assuming you are in the backend directory) ADJUST IF NEEDED!
BASE_DIR = Path(__file__).resolve().parent.parent
source_checker = SourceChecker(str(BASE_DIR / "models/sourcebias_probabilities.csv"))
sentence_detector = SentenceClaimDetector(
    str(BASE_DIR / "models/claimdetection_oneClassSVM.pkl")
)
bias_detector = BiasDetector(
    str(BASE_DIR / "models/DistilBert_PoliticalBias_FineTuned/")
)


# Define request schema
class ArticleURL(BaseModel):
    url: str


@bias_router.post("/analyze")
def analyze_article(input: ArticleURL):

    # Step 0: Weights
    priors = { # Default probabilities for how biased something is.
        "left": 0.25,
        "center": 0.50,
        "right": 0.25
    }
    thresholds = { # The model must be this amount sure. (i.e. model must be 85% sure something is left leaning)
        "claims": 0.5,
        "left": 0.90,
        "center": 0.5,
        "right": 0.5
    }
    weights = { # For final output, how important is each component? (i.e. we want to consider prior and article the most, but sentence probabilities might be unreliable)
        "prior": 2.5,
        "source": 3.0,
        "article": 2.0,
        "sentence": 0.10
    }

    # Step 1: Scrape article
    article_data = NewsScrape(input.url)
    if not article_data or not article_data["text"]:
        raise HTTPException(
            status_code=400, detail="Failed to scrape article or extract text."
        )

    # Step 2: Source bias
    source_name = article_data["source"]
    match, source_probs = source_checker.search(source_name)
    if source_probs is None:
        source_probs = priors  # fallback
    source_bias = source_probs.idxmax().split('(')[1].split('|')[0]

    # Step 3: Article-level bias
    article_probs = bias_detector.text_predict(article_data["text"])["probability"]
    article_probs = {
        "left": article_probs[0],
        "center": article_probs[1],
        "right": article_probs[2],
    }

    # Step 4: Sentence-level claims
    sentence_outputs = sentence_detector.text_predict(
        article_data["text"], claim_threshold=thresholds["claims"]
    )
    sentence_probs = []
    for sent in sentence_outputs:
        if sent['label'] == "claim":
            probs = bias_detector.text_predict(sent["text"])["probability"]
            sentence_probs.append({
                "left": probs[0],
                "center": probs[1],
                "right": probs[2],
            })
        else:
            sentence_probs.append(priors)

    # Step 5: Combine scores
    final_probs, predicted_label = NBScore(
        priors=priors,
        source_probs=source_probs,
        article_probs=article_probs,
        sentence_probs=sentence_probs,
        weights=weights
    )

    # Step 6: Return response
    return {
        "title": article_data["title"],
        "source": source_name,
        "source_bias": source_bias,
        "bias_prediction": predicted_label,
        "bias_distribution": final_probs,
        "article_summary": {
            "authors": article_data["authors"],
            "publish_date": article_data["publish_date"],
            "text": "\n" + article_data["text"].replace("\n", " ").strip(),
        },
    }
