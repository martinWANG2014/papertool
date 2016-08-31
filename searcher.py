class Searcher:

	# content is an array of sentences
	# indexList is a corresponding array of entries in infoList
	# infoList is a list of tupes (title, authors, year)

	content = []
	lcontent = []
	indexList = []
	infoList = []
	keys = []
	suggestions = []
	searchIndex = 0
	searchInds = []
	cache = {}

	def __init__(self, content, indexList, infoList):
		self.content = content
		self.indexList = indexList
		self.infoList = infoList
		self.lcontent = [s.lower() for s in self.content]
		self.startSearch([])

	def startSearch(self, keys = []):
		if keys:
			query = " ".join(self.keys)[:-1]
			self.keys = keys
			self.suggestions = []
			self.searchInds = self.cache.get(query, range(len(self.content)))
			self.searchIndex = 0
		else:
			self.suggestions = range(0, len(self.content))
			searchIndex = len(self.content)

	def continueSearch(self):
		# search (if necessary)
		blockEnd = min(self.searchIndex + 10000, len(self.searchInds))
		for j in range(self.searchIndex, blockEnd):
			i = self.searchInds[j]
			line = self.lcontent[i]
			matches = [line.find(k) for k in self.keys]
			if not -1 in matches:
				self.suggestions.append(i)
		self.searchIndex = blockEnd
		if self.isSearchComplete():
			query = " ".join(self.keys)
			if len(query) > 0:
				self.cache[query] = self.suggestions

	def isSearchComplete(self):
		return self.searchIndex == len(self.searchInds)

	def getSuggestion(self, ind):
		sug = self.content[ind]
		info = self.infoList[self.indexList[ind]]
		infoStr = self._getInfoStr(info)
		return (sug, infoStr)

	def _getInfoStr(self, info):
		if info and 'message' in info:
			item0 = info['message']['items'][0]
			title = ''.join(item0['title'])
			if 'published-print' in item0:
				year = item0['published-print']['date-parts'][0][0]
			elif 'deposited' in item0:
				year = item0['deposited']['date-parts'][0][0]
			elif 'issued' in item0:
				year = item0['issued']['date-parts'][0][0]
			else:
				raise Exception(title)
			return '(%s, %d)' % (title, year)
		elif info:
			return '(%s)' % info['_file'].split('/')[-1].encode('utf-8')
		else:
			return ''

	def _getSentenceInfo(self, ind):
		selSug = self.suggestions[ind]
		papInd = self.indexList[selSug]
		return self.infoList[papInd]

	def getURL(self, ind):
		info = self._getSentenceInfo(ind)
		if 'message' in info:
			item0 = info['message']['items'][0]
			return item0['URL']
		else:
			return None

	def getFile(self, ind):
		info = self._getSentenceInfo(ind)
		return info['_file']

	def getSuggestionCount(self):
		return len(self.suggestions)
