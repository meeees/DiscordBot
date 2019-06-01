from markov import markov_chain
import base64
import re

class bot_markov_chain(markov_chain) :

	def __init__(self, two = False) :
		markov_chain.__init__(self, two)

	def load_markov(self, path, keep_names = False) :
		with open(path, 'r') as f_in :
			for line in f_in:
				data = line.split(' ')
				name = base64.b64decode(data[0]).decode('utf-16')
				content = base64.b64decode(data[1]).decode('utf-16').split('\n')

				for l in content :
					if keep_names :
						self.train(name + ': ' + l)
					else :
						self.train(l)
		self.compute()

	@staticmethod
	def remove_mentions(text):
		match = re.search('<@[0-9]+>', text)
		if match == None :
			return text
		text = text[:match.start()] + '-' + text[match.start()+1:match.end()-1] + '-' + text[match.end():]
		return text

	def make_sentence(self) :
		return bot_markov_chain.remove_mentions(super().make_sentence())


if __name__ == '__main__' :
	#print(bot_markov_chain.remove_mentions('meeees: <@142767245905494016> send me your address, ill grab some dry ice'))
	test = bot_markov_chain(True)
	test.load_markov('bot-data/136984919875387393/general', True)
	print (test.make_sentence())