class SearchCache(dict):
  def __init__(self, maxsize):
    self.maxsize = maxsize

  def add_search(self, v):
    if v in self:
      self.pop(v, None)
    elif len(self) == self.maxsize:
      self.pop(next(iter(self.keys())))

    self[v] = True

  def get_hot_searches(self):
    return self.keys()

cache = SearchCache(3)
cache.add_search(1)
assert cache.get_hot_searches() == {1}
cache.add_search(1)
assert cache.get_hot_searches() == {1}
cache.add_search(2)
assert cache.get_hot_searches() == {2, 1}
cache.add_search(3)
assert cache.get_hot_searches() == {1, 2, 3}
cache.add_search(4)
assert cache.get_hot_searches() == {2, 3, 4}
cache.add_search(5)
assert cache.get_hot_searches() == {3, 4, 5}
cache.add_search(4)
assert cache.get_hot_searches() == {3, 4, 5}
cache.add_search(3)
assert cache.get_hot_searches() == {3, 4, 5}
