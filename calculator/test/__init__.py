from math import inf
from operator import neg


min_iterations = 10
max_iterations = 100

def appropriate_indeterminate(determining_num):
	return None if determining_num == 0 else neg(inf) if determining_num < 0 else inf