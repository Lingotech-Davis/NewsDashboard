# -------------------- Import requirements ------------------------------------------------------------------------------------------------------------------------ #
# !pip install thefuzz[speedup] transformers datasets torch nltk pandas numpy scipy scikit-learn

# Source checker + Transformers reqs
import numpy as np
import pandas as pd

# Extra transformers reqs
import os.path as op
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F
from datasets import Dataset
from datasets.utils.logging import disable_progress_bar
import torch
from transformers import AutoTokenizer
from transformers import AutoModel
import nltk
nltk.download('punkt_tab')
import pickle
from scipy.special import expit
import sklearn

# Extras
from thefuzz import process
from newspaper import Article
import re
from urllib.parse import urlparse
from functools import reduce
import math
from datasets.utils.logging import disable_progress_bar, set_verbosity_error
disable_progress_bar()
set_verbosity_error()


# -------------------- Class definitions ------------------------------------------------------------------------------------------------------------------------- #
class SourceChecker():
  def __init__(self, df_path: str): # Loads in a dataframe with columns: "source", "P(left|source)", "P(center|source)", and "P(right|source)"
    dataframe = pd.read_csv(df_path)
    self.probs = dataframe.set_index('source')
    print("Source checking has been successfully loaded!")
  def get_bias_distribution_fuzzy(self, query, prob_table, cutoff=70): # Helper function for search
      sources = prob_table.index.tolist()
      match_result = process.extractOne(query, sources)
      if match_result is None or match_result[1] < cutoff:
          return f"No good match found for '{query}'"
      match, score = match_result
      return match, prob_table.loc[match]
  def search(self, query): # Fuzzy search the dataframe for the query (news outlet)
    match_info = self.get_bias_distribution_fuzzy(query, self.probs)
    if isinstance(match_info, tuple):
        match, dist = match_info
    else:
        return None, None
    return match, dist

class SentenceClaimDetector():
  def __init__(self, pkl_path: str): # Loads in OneClassSVM model along with DistilBERT
    with open(pkl_path, 'rb') as f:
      self.classifier = pickle.load(f)
    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    self.model = AutoModel.from_pretrained("distilbert-base-uncased")
    self.model.to(self.device);
    print("Model has been successfully loaded!")
  def split_sentences(self, article: str): # Splits sentences using nltk
    return nltk.sent_tokenize(article)
  def get_embeddings(self, sentences: list[str]): # Gets embeddings for a given list of sentences
    raw_sentences = Dataset.from_list([{"text": s} for s in sentences])
    tokenized_sentences = raw_sentences.map(lambda x: self.tokenizer(x["text"], padding=True, truncation=True), batched=True)
    @torch.inference_mode()
    def get_output_embeddings(batch):
        input_ids = torch.tensor(batch["input_ids"]).to(self.device)
        attention_mask = torch.tensor(batch["attention_mask"]).to(self.device)
        output = self.model(input_ids, attention_mask=attention_mask).last_hidden_state[:, 0]
        return {"features": output.cpu().numpy()}
    return tokenized_sentences.map(get_output_embeddings, batched=True, batch_size=10)
  def embedding_predict(self, sentences, embeddings): # Given an embedding, predicts whether or not it is a claim
    X = embeddings
    predictions = self.classifier.predict(X)
    prob_estimates = expit(self.classifier.decision_function(X))
    output = []
    for estimated_probability, prediction, sentence in zip(prob_estimates, predictions, sentences):
      id2label = {-1: "not claim", 1: "claim"}
      predicted_label = id2label[prediction] if estimated_probability >= self.claim_threshold else id2label[-1]
      output.append({"text": sentence,
                     "probability": estimated_probability,
                     "class_id": prediction,
                     "label": predicted_label})
    return output
  def text_predict(self, article: str, claim_threshold=0): # Splits text into sentences. Tokenizes those sentences. Grabs embeddings. Predicts.
    self.claim_threshold = claim_threshold
    sentences = self.split_sentences(article)
    sentence_features = self.get_embeddings(sentences)
    return self.embedding_predict(sentences, np.array(sentence_features['features']))

class BiasDetector():
  def __init__(self, checkpoint_path): # Loads the fine-tuned checkpoint along with DistilBERT
    self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
    self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    self.model.to(self.device)
    self.model.eval()
    print("Model has been successfully loaded!")
  def text_predict(self, text, thresholds={"left": 0.0, "right": 0.0, "center": 0.0}): # Feeds the input into the fine-tuned model for a prediction
    tokenized_input = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    tokenized_input = {key: value.to(self.device) for key, value in tokenized_input.items()}
    with torch.no_grad():
        outputs = self.model(**tokenized_input)
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1).numpy().flatten()
    predicted_class_id = np.argmax(probs, axis=0)
    id2label = {0: "left", 1: "center", 2: "right"}
    predicted_label = id2label[predicted_class_id] if probs[predicted_class_id] >= thresholds[id2label[predicted_class_id]] else "center"
    return {"text": text,
            "probability": probs,
            "class_id": predicted_class_id,
            "label": predicted_label}

def BaseURL(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        base = domain_parts[-3]
    else:
        base = domain_parts[0]
    return base

def NewsScrape(url): # Webscrapes the URL and filters for the article
  try:
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
  except:
    return None
  sentences = nltk.sent_tokenize(article.text)
  def is_valid_sentence(s):
      s = s.strip()
      if len(s) < 30: return False  # Too short
      if re.search(r'http[s]?://', s): return False  # Contains URL
      if re.search(r'\bsubscribe\b|\bread more\b|\bclick here\b', s, re.IGNORECASE): return False # Other common items
      return True
  cleaned_sentences = [s for s in sentences if is_valid_sentence(s)]
  cleaned_article = "\n".join(cleaned_sentences)
  return {"title": article.title,
          "authors": article.authors,
          "publish_date": article.publish_date,
          "text": cleaned_article,
          "source": BaseURL(url)}

def NBScore(priors, source_probs, article_probs, sentence_probs, weights=None):
    if weights is None:
        weights = {
            "prior": 3.0,
            "source": 1.0,
            "article": 5.0,
            "sentence": 0.05
        }
    scores = {}
    for label in priors:
        log_prior = weights["prior"] * math.log(priors[label] + 1)
        log_source = weights["source"] * math.log(source_probs.get("P("+label+"|source)", 0) + 1)
        log_article = weights["article"] * math.log(article_probs.get(label, 0) + 1)
        log_sentences = sum([
            weights["sentence"] * math.log(sent.get(label, 0) + 1)
            for sent in sentence_probs
        ])
        scores[label] = log_prior + log_source + log_article + log_sentences
    def normalize_log_scores(log_scores):
      max_log = max(log_scores.values())
      exp_scores = {label: math.exp(score - max_log) for label, score in log_scores.items()}
      total = sum(exp_scores.values())
      return {label: score / total for label, score in exp_scores.items()}
    probabilities = normalize_log_scores(scores)
    return probabilities, max(probabilities, key=probabilities.get)
