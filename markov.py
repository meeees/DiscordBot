#even though this is included as part of my discord bot it can be used entirely as a standalone
import random
import base64

class markov_word :

	def __init__(self) :
		self.next = {}
		self.total = 0

	def train(self, word) :
		if word in self.next :
			self.next[word] += 1
		else :
			self.next[word] = 1
		self.total += 1

	def compute_probabilities(self) :
		self.probs = []
		self.sorted_words = []
		sorted_dict = [(k, v) for v, k in sorted([(v, k) for (k,v) in self.next.items()])]
		culm_chance = 0.
		for k, v in sorted_dict :
			self.sorted_words.append(k)
			this_prob = float(v) / float(self.total)
			culm_chance += this_prob
			self.probs.append(culm_chance)

	def get_next(self) :
		if self.probs == None :
			print ('We cannot generate the next word if probabilities have not been computed!')
			return None
		if len(self.probs) == 0 :
			return None
		test = random.random()
		for i in range(0, len(self.probs)) :
			if self.probs[i] >= test :
				return self.sorted_words[i]



class markov_chain :

	def __init__(self, two = False) :
		self.words = {}
		self.two = two
		if self.two :
			self.words[('','')] = markov_word()
		else :
			self.words[''] = markov_word()

	def train(self, sentence) :
		prev = ''
		prev2 = ''
		s_words = sentence.split(' ')
		if self.two :
			for w in s_words :
				self.words[(prev2, prev)].train(w)
				if (prev, w) not in self.words :
					self.words[(prev, w)] = markov_word()
				prev2 = prev
				prev = w
			#we do this to recognize endings
			self.words[(prev2, prev)].train('')
		else :
			for w in s_words :
				self.words[prev].train(w)
				if w not in self.words :
					self.words[w] = markov_word()
				prev2 = prev
				prev = w
			#we do this to recognize endings
			self.words[prev].train('')

	def compute(self) :
		for w in self.words :
			self.words[w].compute_probabilities()

	def make_sentence(self) :
		res = []
		if self.two :
			nxt = self.words[('','')]
		else :
			nxt = self.words['']
		prevwd = ''
		while True :
			new_nxt = nxt.get_next()
			if new_nxt == None or new_nxt == '':
				break
			res.append(new_nxt)
			if self.two :
				nxt = self.words[(prevwd, new_nxt)]
			else :
				nxt = self.words[new_nxt]
			prevwd = new_nxt
		if len(res) == 0 :
			return self.make_sentence()
		return ' '.join(res)

	def load_markov(self, path) :
		with open(path, 'r') as f_in :
			for line in f_in:
				if line.strip() != '' :
					self.train(line[:-1].lower())
		self.compute()


#if we want to pull chains for multiple people from the same data
class personal_markov_chain :

	def __init__(self, names, two = False) :
		self.names = names
		self.chains = {}
		for n in names :
			self.chains[n] = markov_chain(two)

	#with personalized chains the input should be
	#<base64_name> <base64_text_data>
	#this accounts for potential spaces in names
	def load_markov(self, path) :
		with open(path, 'r') as f_in :
			for line in f_in:
				data = line.split(' ')
				name = base64.b64decode(data[0]).decode('utf-16').lower()
				#whether texts cares about lower case or not
				content = base64.b64decode(data[1]).decode('utf-16').split("\n")
				#content = base64.b64decode(data[1]).decode('utf-16').split("\n")
				if not name in self.names :
					continue
				for l in content :
					self.chains[name].train(l)
		print ("We loaded the things")
		for n in self.names :
			self.chains[n].compute()
		print ("We computed the things")

	def generate_for(self, name) :
		return self.chains[name].make_sentence()


if __name__ == '__main__' :
	#this is where you can generate text inside this file
	#just make either a personal chain or a generic chain and load from a correct path
	bee_movie = personal_markov_chain([''], True)
	bee_movie.load_markov("bot-data/136984919875387393/general")
	for x in range(0, 100) :
		try :
			print (bee_movie.generate_for(''))
		except :
			x -= 1
