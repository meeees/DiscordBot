import random

fact_files = {}
fact_index = {}

def get_fact(type) :
	if not type in fact_files.keys() :
		fact_files[type] = load_fact_file(type)
		fact_index[type] = 0

	if fact_index[type] >= len(fact_files[type]) :
		random.shuffle(fact_files[type])
		fact_index[type] = 0
	fact_index[type] += 1
	return fact_files[type][fact_index[type] - 1]


def load_fact_file(type) :
	path = 'bot-data/' + type + '_facts.txt'
	facts = []
	with open(path, 'r') as fIn :
		facts = fIn.readlines()
	random.shuffle(facts)
	return facts

