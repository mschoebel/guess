
import core

COLORS = 6
PLACES = 4

def main():

	# determine all combinations
	allCombinations = core.getSolutionSet(PLACES, COLORS)

	print 'Overall number of combinations : %d' % len(allCombinations)

	guess = core.bestFirstGuess(PLACES, COLORS)
	#guess = core.bestGuess(allCombinations, PLACES)
	#guess = (0,0,1,1) # C6 P4

	print 'Best initial guess             : %s' % str(guess)

	print
	print 'Optimal game'

	nr = 1

	evaluation = core.bestEvaluation(allCombinations, guess, PLACES)
	remaining = core.reduceSolutionSet(guess, evaluation, allCombinations)

	while (evaluation != (PLACES,0)):

		print '%2d: %s %s - %d solutions remaining' % (nr, guess, evaluation, len(remaining))

		guess = core.bestGuess(remaining, PLACES)
		evaluation = core.bestEvaluation(remaining, guess, PLACES)
		remaining = core.reduceSolutionSet(guess, evaluation, remaining)

		nr += 1

	print '%2d: %s %s' % (nr, guess, evaluation)

main()
