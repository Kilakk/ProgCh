import translator

def main():
	dictionary = translator.Dictionary("dict.txt")
	print(dictionary.getValue("Hap"))
	print(dictionary.getValue("Haq"))
	print(dictionary.getEntry("Haq"))
	print(dictionary.getValue("roflmao"))
	print(dictionary.getEntry("roflmao"))
	print("")
	print(dictionary.find("Haq"))
	print(dictionary.find("gun"))
	print(dictionary.find("banana"))
	print(dictionary.find("diminutive"))
	print(dictionary.find("bloxxor"))
	print("")
	print(dictionary.random())
	print(dictionary.random())
	print(dictionary.random())
	print("")
	
	while True:
		test_input = input("Find in dictionary: ")
		print("You inputted: " + test_input)
		print(dictionary.find(test_input))

if __name__ == "__main__":
	main()