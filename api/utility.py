from summarizers.summarymanager import SummaryManager

class Utility:
	@staticmethod
	def summarize(document,method = None):
		# ducument is the text to Summarizer
		# method is the summarizer method
		# if method == None or if it does not match with listed ones then KeyPhraseSummarizer
		# will be chosen
		return SummaryManager.summarize(document,method)
