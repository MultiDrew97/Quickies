from pytest import raises, approx
from math import floor
from random import randint, random

from statistics.binomial import *

min_size=10
max_size = 100

size = randint(min_size, max_size)
success = randint(0, size)
prob_success = round(random(), 2)

def test_binomial():
	with raises(Exception):
		binomial(-1, success, prob_success) # Bad sample size
		binomial(size, size+1, prob_success) # Bad success count
		binomial(size, size+1, 2) # Bad probability
		binomial(size, size+1, -1) # Bad probability
		binomial(size, size+1, -0.4) # Bad probability

	lower, equal, upper = less_than_binomial(size, success, prob_success), binomial(size, success, prob_success), greater_than_binomial(size, success, prob_success)
	allProbs = lower + equal + upper

	assert (allProbs) == approx(1)
	assert (allProbs) == approx(between_binomial(size, prob_success, 0, size))


	# Check for consistent "identity" of binomial distribution
	for _ in range(25):
		t_size = randint(min_size, max_size)
		t_succ = randint(0, t_size)
		t_prob = random()
		lower, equal, upper = less_than_binomial(t_size, t_succ, t_prob), binomial(t_size, t_succ, t_prob), greater_than_binomial(t_size, t_succ, t_prob)
		allProb = lower + equal + upper

		assert allProb == approx(1)
		assert allProb == approx(between_binomial(t_size, t_prob, 0, t_size))


def test_less_binomial():
	print(f"P(X<{success}) = {less_than_binomial(size, success, prob_success)}", flush=True)

def test_greater_binomial():
	print(f"P(X>{success}) = {greater_than_binomial(size, success, prob_success)}")

def test_between_binomial():
	lower_bound = randint(0, floor(size / 2))
	upper_bound = randint(lower_bound, size)
	print(f"P({lower_bound} <= X <= {upper_bound}) = {between_binomial(size, prob_success, lower_bound, upper_bound)}")
	#  Should be equivalent since internal logic swaps flipped bounds
	assert between_binomial(size, prob_success, size, 0) == approx(between_binomial(size, prob_success, 0, size))

	with raises(Exception):
		between_binomial(size, prob_success, -1, size) # bad lower bound
		between_binomial(size, prob_success, 0, size+1) # bad lower bound

