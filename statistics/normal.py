def Mu(size, prob):
	if (size < 1):
		raise Exception("Size must be a non-negative number and greater than 0")

	if (prob > 1 or prob < 0):
		raise Exception("Probabliity should be a non-negative value and 0 <= p <= 1")

	return size * prob

def Sigma(mu, prob):
	return (mu * (1 - prob)) ** (1/2)

def normal(size, success, prob_success):
	mu = Mu(size, prob_success)
	sigma = Sigma(mu, prob_success)
	return (success - mu) / sigma