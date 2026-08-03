# helper.py
# Library functions for use with your word guess game
#

import random
def random_secret_word():
  """Selects a random word from the file word_list.txt in the same directory"""
  input_file = open('word_list.txt','r')
  word_list = [word.strip().lower() for word in input_file.readlines() if word.strip().isalpha() and len(word) > 4]
  input_file.close()
  
  return word_list[random.randint(0,len(word_list)-1)]
  
