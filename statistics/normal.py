def Mu(size, prob):
	return size * prob

def Sigma(mu, prob):
	return (mu * (1 - prob)) ** (1/2)

def normal(size, success, prob_success):
	mu = Mu(size, prob_success)
	sigma = Sigma(mu, prob_success)
	return (success - mu) / sigma