import time, copy

class Filter():
    """Create an Object Filter
        :filter_text: the # the filter is selecting
        :ttl: The expiration time for this filter
        :source: The twitter user who issued the request.
    """
    def __init__(self, filter_text, ttl, source=""):
        self.filter_text = filter_text
        self.ttl = ttl
        self.created_at = time.time()
        self.created_by = source

    def is_expired(self):
        return (time.time() - self.created_at) > self.ttl

    def __str__(self):
        return 'Filter on: "'+ self.filter_text + '", created at: ' + str(self.created_at) + ' and expires after: ' + str(self.ttl)

class FiltersList():
    """Create an Object FiltersList to manage a list of filters.
        :list_filters: a list of filters
    """
    def __init__(self, list_filters=[]):
        self.count_filters = len(list_filters)
        self.filters = list_filters

    def add_filter(self, new_filter):
        self.count_filters += 1
        self.filters.append(new_filter)

    def clean_filters_list(self):
        self.filters = [filter for filter in self.filters if not filter.is_expired()]

    def export_filters_list(self):
        self.clean_filters_list()
        return copy.deepcopy([filter.filter_text for filter in self.filters])

    def __str__(self):
        return str([str(filter) for filter in self.filters])


if __name__ == "__main__":
    print "This demonstrates how the Filters and FiltersList work"
    print "Create Filter"
    filter_bla = Filter("bla", 0.5)
    print filter_bla
    print "Create FiltersList"
    filters = FiltersList([filter_bla])
    print filters
    print "Exported filters"
    print filters.export_filters_list()
    time.sleep(0.5)
    print "Exported filters after expiration"
    print filters.export_filters_list()