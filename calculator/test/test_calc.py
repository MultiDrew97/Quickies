from calculator.calc import *

def test_addition():
	assert addition(1, 1) == 2

def test_subtraction():
	assert subtraction(1, 1) == 0

def test_multiplication():
	assert multiplication(2, 2) == 4

def test_division():
	assert division(12, 2) == 6