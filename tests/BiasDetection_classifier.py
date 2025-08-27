# README: This script will hopefully create an idea of how to integrate these functions into a web app

# ---------- Dependencies & Initializations ------------------------------------------ #
import BiasDetection_utilities
from colorama import Fore, Back, Style, init
init()
probs_path = "models/sourcebias_probabilities.csv"
bias_model_path = "models/DistilBert_PoliticalBias_FineTuned/"
claim_model_path = "models/claimdetection_oneClassSVM.pkl"

# Some parameters to keep tuning by hand!
weights = {
  "prior": 3.0,
  "source": 1.0,
  "article": 5.0,
  "sentence": 0.05
}
certainties = {
  "claims": 0.5,
  "left": 0.85,
  "right": 0.5,
  "center": 0.5
}
print("Initializing Models...")
source_checker = BiasDetection_utilities.SourceChecker(probs_path)
bias_detection_model = BiasDetection_utilities.BiasDetector(bias_model_path)
claim_detection_model = BiasDetection_utilities.SentenceClaimDetector(claim_model_path)

while True:
  # ---------- Inputs ------------------------------------------------------------------ #
  max_attempts = 3
  attempts = 0
  while True:
      url = input("Enter a URL to a newspaper article: ")
      print("Scraping the URL for the article...")
      article = BiasDetection_utilities.NewsScrape(url)
      if article:
          break
      else:
          print("Failed to scrape article. Please try again.\n")
          attempts += 1
          if attempts == max_attempts:
            article = {}
            article['text'] = input("Enter the article here: ")
            article['source'] = input("Enter the source here: ")
            break

  # ---------- Function calls ---------------------------------------------------------- #
  print("Checking the source for any biases...")
  source_match, source_dist = source_checker.search(article['source'])
  print("Checking the parts of the article for any biases")
  claim_predictions = claim_detection_model.text_predict(article['text'], claim_threshold=certainties["claims"])
  sentence_predictions = [bias_detection_model.text_predict(sentence, thresholds=certainties) for sentence in claim_detection_model.split_sentences(article['text'])]
  print("Checking the full article for any biases...")
  article_output = bias_detection_model.text_predict(article['text'])
  print("Combining total scores...")
  nb_probs, top_pred = BiasDetection_utilities.NBScore(priors={"left": 0.25, "right": 0.25, "center": 0.5},
                                          source_probs={"left": source_dist['P(left|source)'], "right": source_dist['P(right|source)'], "center": source_dist['P(center|source)']},
                                          article_probs={"left": article_output["probability"][0], "right": article_output["probability"][2], "center": article_output["probability"][1]},
                                          sentence_probs=[{"left": sent_output["probability"][0], "right": sent_output["probability"][2], "center": sent_output["probability"][1]} for sent_output in sentence_predictions],
                                          weights=weights)
  print("Done!")
  print()

  # ---------- Outputs ----------------------------------------------------------------- (p.s. thank you so much for AI who helped me in styling this output) #
  print("="*120)
  print(f"[🔍 Source Match] Closest source in our database: {source_match}")
  print(source_dist)
  print("="*120)
  print()
  print("="*120)
  print("[🧠 Detected Claims]")
  print("="*120)
  for claim_pred, sentence_pred in zip(claim_predictions, sentence_predictions):
      sentence = claim_pred['text'].replace("\n", " ").strip()
      if claim_pred['label'] == "claim":
          if sentence_pred['label'] == "left":
              color = Back.BLUE
          elif sentence_pred['label'] == "right":
              color = Back.RED
          else:
              color = Back.WHITE # Optional YELLOW for center claims, but we'll set it to WHITE so that we only see RED and BLUE different.
      else:
          color = Back.WHITE
      print(color + Fore.BLACK + "• " + sentence + Style.RESET_ALL)
  print()
  print("="*120)
  print(f"[📊 Article Embedding Prediction] → {article_output["probability"][article_output["class_id"]]*100:.2f}% {article_output['label'].upper()} leaning")
  print("="*120)
  print()
  print("="*120)
  print(f"[🧮 Final Naive Bayes Prediction] → {nb_probs[top_pred]*100:.2f}% {top_pred.upper()} leaning")
  print("="*120)
  user_choice = input("Got another article? [Y/N] ")
  if user_choice.lower()[0] == "y":
    continue
  else:
    break

# If we want to implement human feedback, here's some code to get started:
# feedback = []
# while True:
#     response = input("Is this a match? [Y/N] ").strip().lower()
#     if response in ['y', 'n']:
#         feedback.append(response)
#         break
#     else:
#         print("Invalid input. Please enter 'Y' or 'N'.")