
def memoize(func):

	cache = {}

	def memf(*x):
		if x not in cache:
			cache[x] = func(*x)
		return cache[x]

	return memf
