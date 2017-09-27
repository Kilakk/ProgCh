import random

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
	  
    return line
	
def random_sentence():
	verbFile = open('verbs.txt')
	nounFile = open('nouns.txt')
	adjFile = open('adjectives.txt')
	
	noun_subj = random_line(nounFile).rstrip()
	
	nounFile.seek(0, 0)
	noun_obj = random_line(nounFile).rstrip()
	
	verb = random_line(verbFile).rstrip()
	adjective = random_line(adjFile).rstrip()
	
	sentence = "The " + noun_subj + " " + verb + " the " + adjective + " " + noun_obj + "."
	
	return sentence

def main():
	for i in range(4):
		print(random_sentence())


if __name__ == "__main__":
	main()