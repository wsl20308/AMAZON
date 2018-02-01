'''
if hasattr(MydupeFilter,'from_settings'):
    func=getattr(MydupeFilter,'from_settings')
    obj=func()
else:
    obj=MyDupeFilter()
'''
class MyDupeFilter(object):
    def __init__(self):
        self.visited=set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        if request.url in self.visited:
            return True
        self.visited.add(request.url)

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass
