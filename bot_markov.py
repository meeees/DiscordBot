from markov import markov_chain, personal_markov_chain
import base64
import re
import random

# use this to generate markov chains for each name
class named_bot_markov_chain(personal_markov_chain) :
	def __init__(self, two = False) :
		personal_markov_chain.__init__(self, [], two)

	def load_markov(self, path) :
		with open(path, 'r') as f_in :
			for line in f_in:
				data = line.split(' ')
				name = base64.b64decode(data[0]).decode('utf-16')
				name = name.replace(' ', '_')
				content = base64.b64decode(data[1]).decode('utf-16').split('\n')

				for l in content :
					if not name in self.chains :
						self.chains[name] = markov_chain(self.two)
					self.chains[name].train(l)
		for k in self.chains.keys() :
			self.chains[k].compute()

	def generate_for(self, name) :
		if not name in self.chains :
			raise Exception('Username not found!')
		return bot_markov_chain.remove_mentions(super().generate_for(name))

	def make_sentence(self) :
		key = list(self.chains.keys())[random.randint(0, len(self.chains))]
		return bot_markov_chain.remove_mentions(self.chains[key].make_sentence())

# use this for generic markov chains (no names)
class bot_markov_chain(markov_chain) :

	def __init__(self, two = False) :
		markov_chain.__init__(self, two)

	def load_markov(self, path, keep_names = False) :
		with open(path, 'r') as f_in :
			for line in f_in:
				data = line.split(' ')
				name = base64.b64decode(data[0]).decode('utf-16')
				name = name.replace(' ', '_')
				content = base64.b64decode(data[1]).decode('utf-16').split('\n')

				for l in content :
					if keep_names :
						self.train(name + ': ' + l)
					else :
						self.train(l)
		self.compute()

	@staticmethod
	def remove_mentions(text):
  		return re.sub(r"<(@[0-9]+)>", r"-\1-", text)
	
	def make_sentence(self, start=None) :
			return bot_markov_chain.remove_mentions(super().make_sentence(start))


if __name__ == '__main__' :
	#print(bot_markov_chain.remove_mentions('meeees: <@142767245905494016> send me your address, ill grab some dry ice'))
	test = named_bot_markov_chain(True)
	test.load_markov('bot-data/136984919875387393/general')
	print(test.generate_for('meeees'))
