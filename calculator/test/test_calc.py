from math import trunc
from random import randint

from calculator.calc import *
from calculator.test import *

def test_addition():
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = num1 + num2
		print(num1, num2, sep=" + ", end=f" == {valid}\n")
		assert addition(num1, num1) == 2 * num1
		assert addition(num1, num2) == valid

def test_subtraction():
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = num1 - num2
		print(num1, num2, sep=" - ", end=f" == {valid}\n")
		assert subtraction(num1, num1) == 0
		assert subtraction(num1, num2) == valid

def test_multiplication():
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = num1 * num2
		print(num1, num2, sep=" * ", end=f" == {valid}\n")
		assert multiplication(num1, -1) == neg(num1)
		assert multiplication(num1, 0) == 0
		assert multiplication(num1, 1) == num1
		assert multiplication(num1, num2) == valid

def test_exponents():
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(2, 100)
		valid = num1 ** num2
		print(num1, num2, sep=" ^ ", end=f" == {valid}\n")
		assert exponential(num1, 0) == 1
		assert exponential(num1, 1) == num1
		assert exponential(num1, num2) == valid


def test_division():
	sig_figs = 5
	for _ in range(randint(min_iterations, max_iterations)):
		num1 = randint(-100, 100)
		num2 = randint(-100, 100)
		valid = round(num1 / num2, sig_figs)
		print(num1, num2, sep=" / ", end=f" == {valid}\n")
		assert division(num1, 0, sig_figs) == None
		assert division(num1, num2, sig_figs) == valid