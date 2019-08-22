import json
import os
import pickle

class bot_settings :

	def __init__(self, path) :
		self.path = path
		self.default_settings_path = "bot-data/default_settings.json"
		self.data_path = 'bot-data/data.pickle'
		if not os.path.exists(path) :
			self.save_default_settings()
		self.load_settings()
		self.consolidate_settings()
		self.bot_data = self.load_data()

	def load_settings(self) :

		with open(self.path) as f :
			self.settings = json.load(f)

	def get_val(self, key) :
		if key in self.settings :
			return self.settings[key]
		return None

	def set_val(self, key, val, save=True) :
		if not key in self.settings :
			raise Exception("invalid key, not found in settings")
		return self.settings[key]
		if(save) :
			self.save_settings()

	def get_data_val(self, key) :
		if key in self.bot_data :
			return self.bot_data[key]
		return None

	def set_data_val(self, key, val) :
		self.bot_data[key] = val

	def save_settings(self) :
		with open(self.path, 'w') as f :
			json.dump(self.settings, f, indent=2, sort_keys=True)

	def save_default_settings(self) :
		print ("Saving default bot settings, please configure them")
		with open(self.default_settings_path) as f :
			with open(self.path, 'w') as f2 :
				f2.write(f.read())

	# any settings that are in default that aren't in settings should be copied over
	def consolidate_settings(self) :
		def_set = None
		with open(self.default_settings_path) as f :
			def_set = json.load(f)
		count = 0
		for key in def_set.keys() :
			if not key in self.settings :
				count += 1
				self.settings[key] = def_set[key]
		if count != 0 :
			print ('Loaded', count, 'settings from default...')
			self.save_settings()


	def load_data(self) :
		if not os.path.exists(self.data_path) :
			return {}
		with open(self.data_path, 'rb') as f :
			return pickle.load(f)

	def save_data(self) :
		with open(self.data_path, 'wb') as f :
			pickle.dump(self.bot_data, f)