from random import randint
from pytest import approx

from wdc.base import *
from wdc.test import appropriate_indeterminate, min_iterations, max_iterations

def test_addition():
	assert approx(addition(1.5, 1.5)) == 1.5 + 1.5
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = num1 + num2
		print(num1, num2, sep=" + ", end=f" == {valid}\n")
		assert approx(addition(num1, num1)) == 2 * num1
		assert approx(addition(num1, num2)) == valid


def test_subtraction():
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = num1 - num2
		print(num1, num2, sep=" - ", end=f" == {valid}\n")
		assert approx(subtraction(num1, num1)) == 0
		assert approx(subtraction(num1, num2)) == valid
	assert approx(subtraction(1.5, 1.5)) == 1.5 - 1.5

def test_multiplication():
	assert approx(multiplication(1.5, 1.5)) == 1.5 * 1.5
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = num1 * num2
		print(num1, num2, sep=" * ", end=f" == {valid}\n")
		assert approx(multiplication(num1, -1)) == neg(num1)
		assert approx(multiplication(num1, 0)) == 0
		assert approx(multiplication(num1, 1)) == num1
		assert approx(multiplication(num1, num2)) == valid

def test_exponents():
	assert approx(multiplication(1.5, 1.5)) == 1.5 * 1.5
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(2, 100)
		valid = num1 ** num2
		print(num1, num2, sep=" ^ ", end=f" == {valid}\n")
		assert approx(exponential(num1, 0)) == 1
		assert approx(exponential(num1, 1)) == num1
		assert approx(exponential(num1, num2)) == valid


def test_division():
	# valid = 66 / 68
	# assert division(66, 68) == valid
	assert approx(division(1.5, 1.25)) == 1.5 / 1.25
	solo = randint(1, 1000)
	assert approx(division(solo, solo)) == 1
	assert approx(division(solo, neg(solo))) == -1
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		if (num2 == 0):
			valid = appropriate_indeterminate(num1)
		else:
			valid = num1 / num2

		print(num1, num2, sep=" / ", end=f" == {valid}\n")
		assert approx(division(num1, num2)) == valid

