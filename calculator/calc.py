from math import inf
from operator import neg

"""

	MAYBE: Functions
			[x] addition
			[x] subtraction
			[x] multiplication
			[x] division
			[x] exponents
			[ ] roots (fractional exponents)
			[ ] trig functions (i.e. sin, cos, tan, etc.)

	MAYBE: Numbers
			[x] integers
			[ ] real

	TODO: Next Steps

		I want to improve performance as best as I can, possible even leverage the speed of having as much as possible in a single line for processing.


 """

""" The operation that will keep addition consistent across functions """
def addition(num1, num2):
	# The heart of the operation
	return num1 + num2

""" The base subtraction function """
def subtraction(num1, num2):
	return addition(num1, neg(num2))

def multiplication(num1, num2):
	def is_negative_result():
		return (num1 < 0 and num2 > 0) or (num1 > 0 and num2 < 0)

	product = 0

	for _ in range(abs(num2)):
		product = addition(product, abs(num1))

	return neg(product) if is_negative_result() else abs(product)

def exponential(base, exp):
	def is_negative_result():
		return exp % 2 != 0 and base < 0

	# Any number to the power of 0 is 1
	if exp == 0:
		return 1

	# Any number to the power of 1 is itself (Identity)
	if exp == 1:
		return base

	#Ensure
	val = abs(base)
	for _ in range(subtraction(abs(exp), 1)):
			val = multiplication(val, abs(base))

	return neg(val) if is_negative_result() else val

def division(numerator, denominator, max_sig_figs=15):
	def is_negative_result():
		return ((numerator < 0 and denominator > 0) or (numerator > 0 and denominator < 0) or (denominator == 0 and numerator < 0)) and numerator != 0

	def count(start):
		v = 0
		while start > 0:
			start = subtraction(start, abs(denominator))
			if (start < 0):
				break
			v = addition(v, 1)
		return v

	if numerator == 0 and denominator == 0:
		return None

	if numerator == 0:
		return 0

	if denominator == 0:
		return neg(inf) if is_negative_result() else inf

	answer = 0
	fig_position = 0
	curr = abs(numerator)

	while (curr > 0 and fig_position <= max_sig_figs):
		#  Continue as long as answer isn't found and we havne't reached desired sigfigs
		if subtraction(curr, abs(denominator)) < 0:
			# All numbers to the right of the decimal

			# 10^x place
			fig_position = addition(fig_position, 1)

			# Update curr to be adjusted for the current place
			curr = multiplication(curr, 10)

			# Perform a non-recursive long division for the current place to determine value. This is only so that I don't continually call itself infinitely
			val =  count(curr)

			# Get the next remainder to continue division if needed
			curr = subtraction(curr, multiplication(abs(denominator), val))

			# The actual representation of the number found that's being added to the number
			adding = val / exponential(10, fig_position)
			print(f"Current Answer: {answer}\n1/{pow(10, fig_position)} place: {val}\nRemainder: {curr}\nAdding As: {adding}\n")
			# Update the number with the newly found 10^x place value
			answer = addition(answer, adding)
		else:
			# left of decimal
			curr = subtraction(curr, abs(denominator))
			answer = addition(answer, 1)


	return neg(answer) if is_negative_result() else abs(answer)