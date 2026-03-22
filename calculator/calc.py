from operator import neg

def addition(num1, num2):
	# The heart of the operation
	return num1 + num2

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


	# 2 ^ 4
	# 2 * 2 * 2 * 2
	# (2 + 2) * 2 * 2
	if exp == 0:
		return 1

	if exp == 1:
		return base

	val = base
	for _ in range(abs(exp)-1):
			val = multiplication(val, base)

	return val

def division(num1, num2, max_figs=5):
	def is_negative_result():
		return (num1 < 0 and num2 > 0) or (num1 > 0 and num2 < 0)

	if num2 == 0:
		print("[WARN] Can't divide by 0")
		return

	curr = abs(num1)
	quot = 0

	while (curr > 0):
		print(f"Curr: {curr}")
		curr = subtraction(curr, abs(num2))
		print(f"After Curr: {curr}")
		if (curr < 0):
			break

		quot += 1


	return neg(quot) if is_negative_result() else abs(quot), curr