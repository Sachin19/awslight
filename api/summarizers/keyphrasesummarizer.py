import networkx as nx
import numpy as np
import math
import nltk

# nltk.data.path.append('/home/sourav/Planck/awstest/basicsummarizer/awstest/api/nltk_data/')
nltk.data.path.append('api/nltk_data/')

from nltk.tokenize import sent_tokenize 
from nltk.tokenize import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

import operator

class KeyPhraseSummarizer():

	NUM_NP = 10
	K = 5
	stopword_list = stopwords.words('english')
	
	@staticmethod
	def preprocess(body):
		sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

		body = sent_tokenizer.tokenize(body)
		body = [word_tokenize(sent) for sent in body]
		body = [nltk.pos_tag(sent) for sent in body]
		
		return body

	@staticmethod
	def acceptable_phrase(phrase):
		l = [word for word in phrase.split() if word not in KeyPhraseSummarizer.stopword_list and len(word) > 3]
		return len(l) > 0

	@staticmethod
	def cleaned_phrase(phrase):
		cleaned = ""
		for word in phrase.split():
			if KeyPhraseSummarizer.acceptable_phrase(word):
				cleaned = word + " "
		cleaned = cleaned.strip()
		return cleaned
	
	@staticmethod
	def get_score(keyphrases, freq_phrases, freq_words):
		score = 0
		for phrase in freq_phrases.items():
			for keyphrase in keyphrases:
				if phrase[0] == keyphrase[0]:
					score += keyphrase[1] * math.sqrt(phrase[1])
					break
					
		for word in freq_words.items():
			for keyphrase in keyphrases:
				if word[0] == keyphrase[0]:
					score += keyphrase[1] * math.sqrt(word[1])
					break
		return score

	@staticmethod
	def leaves_NP(tree):
		for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
			yield subtree.leaves()
		
	@staticmethod
	def summarize(body):

		body_pos = KeyPhraseSummarizer.preprocess(body)
			
		# grammar = "NP: {<DT>?<JJ>*<NN>}"
		grammar = r"""
		NBAR:
		{<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
		
		NP:
		{<DT>?<JJ>*<NN>}
		{<NBAR>}
		{<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
		"""
		chunker = nltk.RegexpParser(grammar)
		trees = [chunker.parse(sent) for sent in body_pos]
		
		NP = {}
		cnt = 0
		for tree in trees:
			for leaf_NP in KeyPhraseSummarizer.leaves_NP(tree):
				
				phrase = ""
				for word in leaf_NP:
					phrase += str(word[0]).lower() + " "
				phrase = phrase.strip()
				phrase = KeyPhraseSummarizer.cleaned_phrase(phrase)
				
				if phrase in NP:
					NP[phrase] += 1
				elif KeyPhraseSummarizer.acceptable_phrase(phrase):
					NP[phrase] = 1
				
				if len(phrase.split()) > 1:
					for word in phrase.split():
						if word in NP:
							NP[word] += 1.0 / len(phrase.split())
						elif KeyPhraseSummarizer.acceptable_phrase(word):
							NP[word] = 1.0 / len(phrase.split())
							
		keyphrases = sorted(NP.items(), key= operator.itemgetter(1), reverse = True)[0 : KeyPhraseSummarizer.NUM_NP+1]
		keyphrases = [(phrase[0], float(phrase[1]) / len(NP)) for phrase in keyphrases]

		scores_dict = {}
		sent_score = [0.0 for x in trees]
		for i, tree in enumerate(trees):
			score = 0
			freq_phrases = {}
			freq_words = {}
			for leaf_NP in KeyPhraseSummarizer.leaves_NP(tree):
				phrase = ""
				for word in leaf_NP:
					phrase += str(word[0]).lower() + " "
				phrase = phrase.strip()
				phrase = KeyPhraseSummarizer.cleaned_phrase(phrase)
				
				if phrase in freq_phrases:
					freq_phrases[phrase] += 1
				elif KeyPhraseSummarizer.acceptable_phrase(phrase):
					freq_phrases[phrase] = 1
					
				if len(phrase.split()) > 1:
					for word in phrase.split():
						if word in freq_words:
							freq_words[word] += 1
						elif KeyPhraseSummarizer.acceptable_phrase(word):
							freq_words[word] = 1
			score = KeyPhraseSummarizer.get_score(keyphrases, freq_phrases, freq_words)
			scores_dict[i] = score
			sent_score[i] = score
			
		if len(body_pos)/3>5:
			KeyPhraseSummarizer.K = 5
		else:
			KeyPhraseSummarizer.K = len(body_pos)/3
			
		scores = sorted(scores_dict.items(), key=operator.itemgetter(1), reverse = True)[0 : KeyPhraseSummarizer.K + 1]
			
		scores = sorted(scores, key = operator.itemgetter(0))
			
		sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		body_sent = sent_tokenizer.tokenize(body)
		summary = []
		if scores[0][0] != 0:
			summary.append((body_sent[0], 0, scores_dict[0]))
		for score in scores:
			summary.append((body_sent[score[0]], score[0], score[1]))
		#return summary
		#return [sent[0] for sent in summary]
		sentences = sent_tokenizer.tokenize(body)				   
		#return sent_score
		return [(sentences[i], scores_dict[i]) for i in xrange(len(sentences))]
			