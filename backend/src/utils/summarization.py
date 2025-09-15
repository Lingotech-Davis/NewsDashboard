# Extractive summarization
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import numpy as np
from spacy.cli import download
download('en_core_web_sm')
PUNC = punctuation

# Gemini summarization
from src.utils.gemini import ask_gemini

# Summarize via extractive summarization
def summarize_nlp(text: str, num_sentences: float):

	# Initialize variables
	stopwords = STOP_WORDS
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(text)
	tokens = [token.text for token in doc]
	punctuation = PUNC + '\n' + '—' + '“' + '”' + '...'
	word_frequencies = {}

	# Create bag of words
	for word in doc:
		if (word.text.lower() not in stopwords) and (word.text.lower() not in punctuation):
			if word.text not in word_frequencies.keys():
				word_frequencies[word.text] = 1
			else:
				word_frequencies[word.text] = word_frequencies[word.text] + 1

	# Calculate "importance" of a word (how many times a word appears / how many times the most common word appears)
	max_frequency = max(word_frequencies.values())
	for word in word_frequencies.keys():
		word_frequencies[word] = word_frequencies[word]/max_frequency

	# Calculate "importance" of a sentence (sum of "importance" of every word in the sentence) + more weight on intro & conclusions
	sentence_tokens = [sent for sent in doc.sents]
	sentence_scores = {}
	score_values = list(sentence_scores.values())
	standard_deviation = np.std(score_values)
	length = len(sentence_tokens)
	x = np.linspace(-1, 1, length)
	bell_shape_curve = np.exp(-x**2 / 0.5)
	for i, sent in enumerate(sentence_tokens):
		for word in sent:
			if word.text.lower() in word_frequencies.keys():
				if sent not in sentence_scores.keys():
					sentence_scores[sent] = word_frequencies[word.text.lower()]
				else:
					sentence_scores[sent] += word_frequencies[word.text.lower()]
		if sent in sentence_scores.keys():
			sentence_scores[sent] += standard_deviation*bell_shape_curve[i]

	# Create summary
	# select_length = int(len(sentence_tokens)*size)
	select_length = num_sentences
	summary = nlargest(min(select_length, len(sentence_tokens)), sentence_scores, key=sentence_scores.get)
	# return "".join([str(sentence) for sentence in summary]).replace("\n", " ").strip()
	return [str(sentence).replace("\n", " ").strip() for sentence in summary]

# Summarize via GenAI
def summarize_generate(text: str, num_sentences: float, gemini_key: str):

	# Call Gemini, feeding the instructions, prompt, and article.
	instructions = "You don't know anything except the information provided for you. Base your answer solely off of this information provided."
	prompt = f"Generate an accurate {num_sentences} sentence summary from the information provided."
	gemini_response = ask_gemini(
        prompt, text, instructions, gemini_key, test_mode=False
	)

	# Call extractive summarization for formatting & ensuring correct size
	return summarize_nlp(gemini_response, num_sentences)
