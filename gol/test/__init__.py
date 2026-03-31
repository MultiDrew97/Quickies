from random import randint

min_iterations, max_iterations = 10, 100

min_x_limit, max_x_limit = 3, 15
min_y_limit, max_y_limit = 3, 15

def gen_x_limit():
	return randint(min_x_limit, max_x_limit)
def gen_y_limit():
	return randint(min_y_limit, max_y_limit)