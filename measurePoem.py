import pronouncing
from string import punctuation
from string import ascii_lowercase
from functools import reduce
import re, unicodedata

##Code is stolen from hyperreality/PoetryTools

def remove_accents(string):
	"""
	Removes unicode accents from a string, downgrading to the base character
	"""

	nfkd = unicodedata.normalize('NFKD', string)
	return u"".join([c for c in nfkd if not unicodedata.combining(c)])

def tokenize(poem):

	tokens = []

	# Problematic characters to replace before regex
	replacements = {u'-': u' ', u'—': u' ', u'\'d': u'ed'}

	for original, replacement in replacements.items():
		replaced = poem.replace(original, replacement)
	replaced = remove_accents(replaced)

	# Keep apostrophes, discard other non-alphanumeric symbols
	cleaned = re.sub(r'[^0-9a-zA-Z\s\']', '', replaced)

	for line in cleaned.split('\n'):
		tokens.append([word for word in line.strip().lower().split(' ')])

	return tokens


def getStressStruct(line):
	stresses = ""
	for word in line:
		phones = pronouncing.phones_for_word(word)
		if phones:
			stress_list = [pronouncing.stresses(phone) for phone in phones]
			if len(stress_list) > 1:
				def xnor(a, b):
					if '2' in a or '2' in b:
						return '0'*len(b)
					else:
						if len(a) == len(b):
							return str(bin(~(int(a, 2)^int(b, 2))))
						elif len(a)>len(b): 
							return '0'*len(a)
						else:
							return '0'*len(b)
				matches = reduce(xnor, stress_list)
				if matches:
					for index, stress in enumerate(stress_list[0]):
						if matches[index]==1:
							stresses += stress
						else:
							stresses += "*"
				else:
					stresses += "*"*len(stress_list[0])
			else:
				stresses += stress_list[0]
		else:
			stresses += "X"
	return stresses


def rhyme_scheme(tokenized_poem):
	"""
	Get a rhyme scheme for the poem. For each line, lookahead to the future lines of the poem and see whether last words rhyme.
	"""

	num_lines = len(tokenized_poem)

	# By default, nothing rhymes
	scheme = ['X'] * num_lines

	rhyme_notation = list(ascii_lowercase)
	currrhyme = -1 # Index into the rhyme_notation

	for lineno in range(0, num_lines):
		matched = False
		for futurelineno in range(lineno + 1, num_lines):
			# If next line is not already part of a rhyme scheme
			if scheme[futurelineno] == 'X':
				base_line = tokenized_poem[lineno]
				current_line = tokenized_poem[futurelineno]

				if base_line == ['']: # If blank line, represent that in the notation
					scheme[lineno] = ' '

				elif rhymes(base_line[-1], current_line[-1]):
					if not matched: # Increment the rhyme notation
						matched = True
						currrhyme += 1

					if base_line == current_line: # Capitalise rhyme if the whole line is identical
						scheme[lineno] = scheme[futurelineno] = rhyme_notation[currrhyme].upper()
					else:
						scheme[lineno] = scheme[futurelineno] = rhyme_notation[currrhyme]

	return scheme


def num_vowels(syllables):
	return len([syl for syl in syllables if any(char.isdigit() for char in syl)])

def rhymes(word1, word2): #This function has been tranformed and is my own now. Sorry hyperreality. 
	"""
	For each word, get a list of various syllabic pronunications. Then check whether the last level number of syllables is pronounced the same. If so, the words probably rhyme
	"""

	pronunciations = [pronouncing.rhyming_part(pronunciation) for pronunciation in pronouncing.phones_for_word(word1)]
	pronunciations2 = [pronouncing.rhyming_part(pronunciation) for pronunciation in pronouncing.phones_for_word(word2)]
	if not (pronunciations and pronunciations2):
		print("no pronunciation for at least one of", word1, word2)
		return False

	# Work around some limitations of CMU
	equivalents = {"ER0": "R"} 
	def replace_syllables(syllables):
		return [equivalents[syl] if syl in equivalents else syl for syl in syllables]

	for syllables in pronunciations:
		syllables = replace_syllables(syllables)

		for syllables2 in pronunciations2:
			syllables2 = replace_syllables(syllables2)
			if syllables == syllables2:
				print(word1, "rhymes with", word2)
				return True
	print(word1, "does not rhyme with", word2)
	return False








