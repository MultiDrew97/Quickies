from random import randint, random
from pytest import approx, raises

from statistics.test import min_sample_size, max_sample_size
from statistics.normal import *

def test_mu():
	with raises(Exception):
		Mu(-1, random()) # Bad sample size
		Mu(randint(min_sample_size, 100), -1) # Negative probability
		Mu(randint(10, 100), 2) # Bad probability

def test_sigma():
	mu = Mu(randint(10, 100), random())
	with raises(Exception):
		Sigma(-1, random()) # Bad sample size
		Sigma(mu, -1) # Negative probability
		Sigma(mu, 2) # Bad probability

def test_normal():
	with raises(Exception):
		normal(-1, randint(0, 10), random()) # Bad sample size
		normal(0, randint(0, 10), random()) # Bad sample size
		normal(randint(min_sample_size, max_sample_size), -1, random()) # Bad success size
		spl = randint(min_sample_size, max_sample_size)
		normal(spl, spl+1, random()) # Too many successes
		normal(spl, randint(0, spl), -1) # Bad prob
		normal(spl, randint(0, spl), 2) # Bad prob

	sample = randint(10, 100)
	succ = randint(0, sample)
	prob = random()
	normal(sample, succ, prob)