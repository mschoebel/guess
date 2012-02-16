
import itertools
import unittest
import tools


## core methods ###############################################################

def reduceSolutionSet(guess, evaluation, solutionSet):
	'''Returns the (reduced) set of candidate solutions if the specified guess
	is evaluated as specified'''
	return [s for s in solutionSet if match(guess, evaluation, s)]

def getSolutionSet(places, colors):
	'''Returns the list of all possible solutions with the specified number
	of places and colors'''
	return list(itertools.product(range(colors), repeat=places))

def bestFirstGuess(places, colors):
	'''Returns the (first) guess that reduces the initial number of possible
	solutions the most. Optimizes the set of checked initial guesses.'''

	# get all solutions for the specified number of places and colors
	completeSolutionSet = getSolutionSet(places, colors)

	# determine reduced candidate set for first guess
	optimizedCandidateSet = []
	for guess in itertools.combinations_with_replacement(range(places), places):
		# guess is starting with '0'?
		if guess[0] != 0:
			continue
		# guess is monoton increasing, without "holes"?
		for i in range(len(guess)-1):
			if guess[i+1] - guess[i] > 1:
				guess = ()
				break
		# valid first guess?
		if guess != ():
			optimizedCandidateSet.append(guess)

	return bestGuess(completeSolutionSet, places, optimizedCandidateSet)

def bestGuess(solutionSet, places, candidateSet = []):
	'''Returns the (first) guess from the candidateSet that reduces the number
	of possible solutions the most. If no candidateSet is given, all possible
	solutions are considered as candidates.'''

	if len(candidateSet) == 0:
		candidateSet = solutionSet

	bestGuess = candidateSet[0]
	remaining = len(solutionSet)+1

	for guess in candidateSet:
	 	r = maxRemainingSolutions(solutionSet, guess, places)
	 	if r < remaining:
	 		bestGuess = guess
	 		remaining = r

	return bestGuess

def bestEvaluation(solutionSet, guess, places):
	'''Returns the evaluation for guess that "keeps" the most possible solutions.'''

	result = (0,0)

	remaining = -1

	# try all combinations of black and white evaluation
	for evaluation in blackWhite(places):
		r = len(reduceSolutionSet(guess, evaluation, solutionSet))
		if r > remaining:
			result = evaluation
			remaining = r

	return result


## evaluation method ##########################################################

@tools.memoize
def evaluate(guess, solution):
	'''Returns the evaluation result of the specified guess compared to the solution.'''

	if guess == solution:
		return (len(guess), 0)

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


## misc. utility methods ######################################################

@tools.memoize
def blackWhite(places):
	'''Returns all possible evaluation results -- all possible combinations
	of white and black with #white+#black <= places'''

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

def match(guess, evaluation, solution):
	'''Returns whether the evaluation matches the guess for the specified solution'''
	return evaluation == evaluate(guess, solution)


## main method to execute unittests ###########################################

if __name__ == '__main__':
	unittest.main()
