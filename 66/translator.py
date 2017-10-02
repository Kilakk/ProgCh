import re

class Dictionary:
	
	def __init__(self, textfile):
		
		self.dict = {}
		
		self.regex_kling = re.compile('tlh:\t\{(.*?)\}')
		self.regex_eng = re.compile('en:\t(.*?)\n')
		
		try:
			file = open(textfile)
			self.readData(file)
		except IOError:
			print("IOError: invalid file!")
			exit()
		
			
		print("It worked!")
		
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
				self.dict[english] = klingon
				english = ""
				klingon = ""
				
		print(self.dict)

def main():
	dict = Dictionary("dict.txt")


if __name__ == "__main__":
	main()