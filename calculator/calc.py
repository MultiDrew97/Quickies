from operator import neg

def addition(num1, num2):
	# The heart of the operation
	return num1 + num2

def subtraction(num1, num2):
	return addition(num1, neg(num2))

def multiplication(num1, num2):
	product = 0
	for _ in range(num2):
		product += addition(num1, num1)

	return product

def division(num1, num2):
	curr = num1
	quot = 0
	while (curr > 0):
		curr = subtraction(curr, num2)

		if (curr >= 0):
			quot += 1

	return quot