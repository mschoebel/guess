
import core

COLORS = 6
PLACES = 4

def main():

	# determine all combinations
	allCombinations = core.getSolutionSet(PLACES, COLORS)

	print 'Overall number of combinations : %d' % len(allCombinations)

	guess = core.bestGuess(allCombinations, PLACES)
	#guess = (0,0,1,1) # C6 P4

	print 'Best initial guess             : %s' % str(guess)

	print
	print 'Worst case game'

	core.printEvaluationOverview(allCombinations, guess, PLACES)
	evaluation = core.bestEvaluation(allCombinations, guess, PLACES)
	remaining = core.reduceSolutionSet(guess, (0,0), allCombinations)

	print '%s %s - %d solutions remaining' % (guess, evaluation, len(remaining))


	guess = core.bestGuess(remaining, PLACES)
	evaluation = core.bestEvaluation(remaining, guess, PLACES)
	remaining = core.reduceSolutionSet(guess, evaluation, remaining)

	print '%s %s - %d solutions remaining' % (guess, evaluation, len(remaining))

	guess = core.bestGuess(remaining, PLACES)
	evaluation = core.bestEvaluation(remaining, guess, PLACES)
	remaining = core.reduceSolutionSet(guess, evaluation, remaining)

	print '%s %s - %d solutions remaining' % (guess, evaluation, len(remaining))

	guess = core.bestGuess(remaining, PLACES)
	evaluation = core.bestEvaluation(remaining, guess, PLACES)
	remaining = core.reduceSolutionSet(guess, evaluation, remaining)

	print '%s %s - %d solutions remaining' % (guess, evaluation, len(remaining))

	guess = core.bestGuess(remaining, PLACES)
	evaluation = core.bestEvaluation(remaining, guess, PLACES)
	remaining = core.reduceSolutionSet(guess, evaluation, remaining)

	print '%s %s - %d solutions remaining' % (guess, evaluation, len(remaining))


if __name__ == '__main__':
	main()
