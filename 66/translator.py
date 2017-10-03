import re
import random

class Dictionary:
	
	def __init__(self, textfile):
		
		self.dict = {}
		
		self.regex_kling = re.compile('tlh:\t.*\{(.*?)\}')
		self.regex_eng = re.compile('en:\t(.*?)\n')
		
		try:
			file = open(textfile)
			self.readData(file)
		except IOError:
			print("IOError: invalid file!")
			exit()
		
		file.close()
		print("Dictionary initialized!")
		
	def readData(self, file):
		
		english = ""
		klingon = ""
		
		for line in file:
			match = self.regex_kling.match(line)
			
			if match:
				klingon = match.group(1)
			else:
				match = self.regex_eng.match(line)
				
				if match:
					english = match.group(1)
					
			# if we have both entries, add them to the dictionary
			# then, kill both placeholders
			if english and klingon:
			
				if klingon in self.dict:
					self.dict[klingon].append(english)
					
				else:
					self.dict[klingon] = [english]
					
				english = ""
				klingon = ""
				
	def getValue(self, key):
		return self.dict.get(key)
		
	def getEntry(self, key):
		value = self.getValue(key)
		if value:
			return {key : value}
		else:
			return None
			
	def find(self, text):
		results = {}
	
		# direct hit
		if self.getValue(text):
			results[text] = self.getValue(text)
			
		# soft search
		else:
			to_find = re.compile(str(text))
			test = ""
			
			for key, values in self.dict.items():
			
				# check key
				test = to_find.search(key)
				if test is not None:
					results[key] = self.getValue(key)
					
				# check values
				for v in values:
					test = to_find.search(v)
					if test is not None:
						results[key] = self.getValue(key)
						
		if not results:
			return None
		else: 
			return results
			
	def random(self):
		key_list = list(self.dict.keys())
		return self.getEntry(key_list[random.randrange(0, len(key_list) - 1)])