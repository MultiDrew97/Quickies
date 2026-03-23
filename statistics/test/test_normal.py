from random import randint, random
from pytest import approx, raises

from statistics.normal import *

def test_mu():
	with raises(Exception):
		Mu(-1, random())
		Mu(randint(10, 100), -1)
		Mu(randint(10, 100), 2)