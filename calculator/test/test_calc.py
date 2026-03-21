from calculator.calc import *

def test_addition():
	num1 = 1
	num2 = 1
	assert addition(num1, num2) == num1 + num2

def test_subtraction():
	num1 = 1
	num2 = 1
	assert subtraction(num1, num2) == num1 - num2

def test_multiplication():
	num1 = 2
	num2 = 2
	assert multiplication(num1, num2) == num1 * num2

def test_division():
	num1 = 12
	num2 = 2
	assert division(num1, num2) == num1 / num2