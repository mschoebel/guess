
import core

COLORS = 6
PLACES = 4

def main():

	# create game configuration
	game = core.GameConfiguration(PLACES, COLORS)

	# determine all combinations
	allCombinations = core.getSolutionSet(game)

	print 'Overall number of combinations : %d' % len(allCombinations)

	guess = core.bestFirstGuess(game)
	#guess = core.bestGuess(game, allCombinations)
	#guess = (0,0,1,1) # C6 P4

	print 'Best initial guess             : %s' % str(guess)

	print
	print 'Optimal game'

	nr = 1

	evaluation = core.bestEvaluation(game, allCombinations, guess)
	remaining = core.reduceSolutionSet(guess, evaluation, allCombinations)

	while (evaluation != (game.places,0)):

		print '%2d: %s %s - %d solutions remaining' % (nr, guess, evaluation, len(remaining))

		guess = core.bestGuess(game, remaining)
		evaluation = core.bestEvaluation(game, remaining, guess)
		remaining = core.reduceSolutionSet(guess, evaluation, remaining)

		nr += 1

	print '%2d: %s %s' % (nr, guess, evaluation)

main()
