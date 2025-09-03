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

# source_checker = SourceChecker("src/models/sourcebias_probabilities.csv")
# sentence_detector = SentenceClaimDetector("src/models/claimdetection_oneClassSVM.pkl")
# bias_detector = BiasDetector("src/models/DistilBert_PoliticalBias_FineTuned/")

BASE_DIR = Path(__file__).resolve().parent.parent

# Load models and data (assuming you are in the backend directory) ADJUST IF NEEDED!
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
    # Step 1: Scrape article
    article_data = NewsScrape(input.url)
    if not article_data or not article_data["text"]:
        raise HTTPException(
            status_code=400, detail="Failed to scrape article or extract text."
        )

    # Step 2: Source bias
    source_name = article_data["source"]
    _, source_probs = source_checker.search(source_name)
    if source_probs is None:
        source_probs = {"left": 0.33, "center": 0.33, "right": 0.33}  # fallback

    # Step 3: Article-level bias
    article_probs = bias_detector.text_predict(article_data["text"])["probability"]
    article_probs = {
        "left": article_probs[0],
        "center": article_probs[1],
        "right": article_probs[2],
    }

    # Step 4: Sentence-level claims
    sentence_outputs = sentence_detector.text_predict(
        article_data["text"], claim_threshold=0.5
    )
    sentence_probs = []
    for sent in sentence_outputs:
        sentence_probs.append(
            {
                "left": 0.33,  # Placeholder -- Our model can't predict sentences that well anyway.
                "center": 0.33,
                "right": 0.33,
            }
        )

    # Step 5: Combine scores
    priors = {"left": 0.33, "center": 0.33, "right": 0.33}
    final_probs, predicted_label = NBScore(
        priors, source_probs, article_probs, sentence_probs
    )

    # Step 6: Return response
    return {
        "title": article_data["title"],
        "source": source_name,
        "bias_prediction": predicted_label,
        "bias_distribution": final_probs,
        "article_summary": {
            "authors": article_data["authors"],
            "publish_date": article_data["publish_date"],
            "text_snippet": article_data["text"][:500]
            + "...",  # Truncated article. Remove if needed.
        },
    }
