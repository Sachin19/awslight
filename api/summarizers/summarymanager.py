from keyphrasesummarizer import KeyPhraseSummarizer
# from lsasummarizer import LSASummarizer

class SummaryManager():

	@staticmethod
	def summarize(document,method = None):
		# return LSASummarizer.summarize(document,2)
		return SummaryManager.TldrSummarize(document,method)
	
	@staticmethod
	def TldrSummarize(document,method = None):
		# currently method is not used
		w_a = 0.0
		w_b = 0.0
		w_c = 0.0
		w_d = 1.0

		#a = PageRankSummarizer.summarize(document)
		#b = LuhnSummarizer.summarize(document)
		#c = CommunitySummarizer.summarize(document)
		d = KeyPhraseSummarizer.summarize(document)

		sentences = [s[0] for s in d]
		#a_score = [w_a * score[1] for score in a]
		#b_score = [w_b * score[1] for score in b]
		#c_score = [w_c * score[1] for score in c]
		d_score = [w_d * score[1] for score in d]
		#combined_score = [sa + sb + sc + sd for sa,sb,sc,sd in zip(a_score,b_score,c_score,d_score)]
                combined_score = d_score

                # use sentence indices for chronological ordering
		final_sentences_and_score = zip(xrange(len(sentences)), combined_score)
                
                #sort by score 
		final_sentences_and_score = sorted(final_sentences_and_score, key=lambda tup: tup[1], reverse=True)
                
		K = len(final_sentences_and_score)

                # take top L sentences
                L = 5 if K > 5 else 1 + K / 3
                final_sentences_and_score = final_sentences_and_score[0:L]
                
                # always add the first sentence
                contains_first = False
                for s in final_sentences_and_score:
                        if s[0] == 0:
                                contains_first = True
                                break

                if not contains_first:
                        s = final_sentences_and_score[-1]
                        final_sentences_and_score.append((0, s[1]))
                
                # now sort top L sentences chronologically
                final_sentences_and_score = sorted(final_sentences_and_score, key=lambda tup: tup[0])

                # get the sentences from the indices
                summary = [sentences[s[0]] for s in final_sentences_and_score]

		return ["OLD SUMMARIZERS : "] + summary

