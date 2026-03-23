# n! = n * (n-1) * n-2) * ... * 1
def factorial(n):
	val = 1
	while(abs(n) >= 2):
		val *= n
		n -= 1

	return val

# n! / (n-s)!s!
def choose(n, m):
	n_fac = factorial(n)
	m_fac = factorial(m)
	n_m_fac = factorial(n-m)

	return n_fac / (n_m_fac * m_fac)

# P(X < n)
def less_than_binomial(size, success, prob_success):
	val = 0
	for i in range(success):
		val += binomial(size, i, prob_success)

	return val

# P(X > n)
def greater_than_binomial(size, success, prob_success):
	val = 0
	for i in range(success + 1, size + 1):
		val += binomial(size, i, prob_success)

	return val


# P(l <= X <= u)
def between_binomial(size, prob_success, lower_bound, upper_bound):
	if (lower_bound > upper_bound):
		tmp = lower_bound
		lower_bound = upper_bound
		upper_bound = tmp

	val = 0
	for i in range(lower_bound, upper_bound + 1):
		val += binomial(size, i, prob_success)

	return val

# P(X = n)
def binomial(size, success, prob_success):
	if (prob_success > 1 or prob_success < 0):
		raise Exception("Probability of success must be a non-zero value and 0 <= p <= 1")

	if (success < 0 or success > size):
		raise Exception("Number of successes must be a non-negative value and ")

	choosen = choose(size, success)
	success_rate = prob_success ** success
	failure_rate = (1 - prob_success) ** (size - success)
	return choosen * success_rate * failure_rate
