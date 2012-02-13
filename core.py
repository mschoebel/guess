
import itertools
import unittest
import tools

@tools.memoize
def blackWhite(places):

	result = []

	for b in range(places+1):
		for w in range(places+1):
			if b+w <= places:
				result += [(b,w)]

	return result

def maxRemainingSolutions(solutionSet, guess, places):

	remaining = 0

	# try all combinations of black and white evaluation
	for evaluation in blackWhite(places):
		r = len(reduceSolutionSet(guess, evaluation, solutionSet))
		if r > remaining:
			remaining = r

	return remaining

def bestGuess(solutionSet, places):

	bestGuess = solutionSet[0]
	remaining = len(solutionSet)+1

	i = 0

	for guess in solutionSet:

	 	r = maxRemainingSolutions(solutionSet, guess, places)
	 	if r < remaining:
	 		bestGuess = guess
	 		remaining = r

		i += 1

	return bestGuess

def bestEvaluation(solutionSet, guess, places):

	result = (0,0)

	remaining = -1

	# try all combinations of black and white evaluation
	for evaluation in blackWhite(places):
		r = len(reduceSolutionSet(guess, evaluation, solutionSet))
		if r > remaining:
			result = evaluation
			remaining = r

	return result

def probability(solutionSet, place, color):
	count = len([s for s in solutionSet if s[place] == color])
	return float(count) / len(solutionSet)

def printProbabilities(solutionSet, places, colors):
	for c in range(colors):
		print c
		for p in range(places):
			print ' %f' % probability(solutionSet, p, c)

def printEvaluationOverview(solutionSet, guess, places):
	for b in range(places+1):
		for w in range(places+1):
			if b+w <= places:
				print '%dB %dW -- %d' % (b, w, len(reduceSolutionSet(guess, (b, w), solutionSet)))

def match(guess, evaluation, solution):
	return evaluation == evaluate(guess, solution)

def reduceSolutionSet(guess, evaluation, solutionSet):
	return [s for s in solutionSet if match(guess, evaluation, s)]

def getSolutionSet(places, colors):
	return list(itertools.product(range(colors), repeat=places))

@tools.memoize
def evaluate(guess, solution):
	'''Returns the evaluation result of the specified guess compared to the solution.'''

	tmpSolution = list(solution)

	black = 0
	white = 0

	# check every position of guessed combination ..
	for i in range(len(guess)):
		if guess[i] == tmpSolution[i]:
			# .. found exact match -> black!
			black += 1
			tmpSolution[i] = -1
		else:
			# .. look for guessed color on another position
			for j in range(len(guess)):
				if i != j and guess[i] == tmpSolution[j] and guess[j] != tmpSolution[j]:
					white += 1
					tmpSolution[j] = -1
					break

		# loop invariant
		assert black+white <= i+1

	# final consistency check
	assert black+white <= len(guess)

	return (black, white)

class TestEvaluateMethod(unittest.TestCase):

	def test_no_match(self):
		self.assertEqual((0,0), evaluate((0,0), (1,1)))

	def test_0B_1W(self):
		self.assertEqual((0,1), evaluate((1,0), (2,1)))

	def test_0B_2W(self):
		self.assertEqual((0,2), evaluate((1,0), (0,1)))

	def test_1B_0W(self):
		self.assertEqual((1,0), evaluate((1,0), (1,1)))

	def test_2B_0W(self):
		self.assertEqual((2,0), evaluate((1,0), (1,0)))


if __name__ == '__main__':
	unittest.main()
