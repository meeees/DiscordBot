import json
import os

class bot_settings :

	def __init__(self, path) :
		self.path = path
		self.default_settings_path = "bot-data/default_settings.json"
		if not os.path.exists(path) :
			self.save_default_settings()
		self.load_settings()

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

	def save_settings(self) :
		with open(self.path) as f :
			json.dump(self.settings, f)

	def save_default_settings(self) :
		print ("Saving default bot settings, please configure them")
		with open(self.default_settings_path) as f :
			with open(self.path) as f2 :
				f2.write(f.read())
