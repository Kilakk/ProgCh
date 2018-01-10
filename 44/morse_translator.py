# translate some morse code ok?
import csv
import os

# from https://github.com/TaylorSMarks/playsound
from playsound import playsound

class MorseTranslator:
	
	def __init__(self, file = "morse.csv", morse_separator = "/"):
		DICT_FILE = file
		
		global MORSE_SEPARATOR
		MORSE_SEPARATOR = morse_separator
		
		self.english_dictionary = dict({})
		self.morse_dictionary = dict({})
		
		f = open(DICT_FILE)
		
		print("Initializing dictionary...")
		for row in csv.reader(f):
			self.english_dictionary[row[0]] = row[1]
			self.morse_dictionary[row[1]] = row[0]
		
		print(self.english_dictionary)
		print("Dictionary initialized!")
		
	def get_morse(self, char):
		morse = ""
		try:
			morse = self.english_dictionary[char.upper()]
		except KeyError:
			pass
		
		return morse
		
	def get_eng(self, str):
		eng = " "
			
		try:
			eng = self.morse_dictionary[str]
		except KeyError:
			pass
		
		return eng
		
	def translate_eng(self, english):
		morse = ""
		english = english.upper()
		
		for i in range(0, len(english)):
			morse += self.get_morse(english[i])
			morse += MORSE_SEPARATOR
			
		return morse
		
	def translate_morse(self, morse):
		english = ""
		m = morse.split(MORSE_SEPARATOR)
		
		for i in m:
			english += self.get_eng(i)
		
		return english
		
	def play_morse(self, morse):
		# dot = wave.open("dot.wav", 'rb')
		# dash = wave.open("dash.wav", 'rb')
	
		for i in range(0, len(morse)):
			if morse[i] == MORSE_SEPARATOR:
				continue
				
			if morse[i] == ".":
				playsound("dot.wav")
			else: 
				if morse[i] == "-":
					playsound("dash.wav")
		
def main():
	trans = MorseTranslator()
	chicken = (trans.translate_eng("CHICKEN 12345 lowercase bad$%chars!!"))
	print(chicken)
	print(trans.translate_morse(chicken))
	
	print("Playing previously generated morse code...")
	trans.play_morse(chicken)
	print("Done!")
	
if __name__ == "__main__":
	main()