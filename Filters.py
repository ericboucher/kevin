import time, copy

class Filter:
	def __init__(self, filterText, ttl):
		self.filterText = filterText
		self.ttl = ttl
		self.createdAt = time.time()

	def isExpired(self):
		return ((time.time() - self.createdAt) > self.ttl)

	def __str__(self):
		return ('Filter on: "'+ self.filterText + '", created at: ' + str(self.createdAt) + ' and expires after: ' + str(self.ttl))

class FiltersList:
	def __init__(self, listFilters=[]):
		self.countFilters = len(listFilters)
		self.filters = listFilters

	def addFilter(self, filter):
		self.countFilters += 1
		self.filters.append(filter)

	def cleanFiltersList(self):
		self.filters = [filter for filter in self.filters if not (filter.isExpired())]

	def exportFiltersList(self):
		self.cleanFiltersList()
		return copy.deepcopy([filter.filterText for filter in self.filters])

	def __str__(self):
		return (str([str(filter) for filter in self.filters]))


if __name__ == "__main__":
	print "This demonstrates how the Filters and FiltersList work"
	print "Create Filter"
	filterBla = Filter("bla", 0.5)
	print filterBla
	print "Create FiltersList"
	filters = FiltersList([filterBla])
	print filters
	print "Exported filters"
	print filters.exportFiltersList()
	time.sleep(0.5)
	print "Exported filters after expiration"
	print filters.exportFiltersList()