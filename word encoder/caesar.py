# In The Name Of God
# Studernt Name: Rasoul Soltanzadeh
# Student ID: 40413160281816
# Teacher Name: Dr. Afrabandpay
# University: University Of Mazandaran 
# Field Of Study: Computer Engineerung 
# Term: 2
# Course: Advanced Programing
# Modify Date: 1405/2/7/9:20 - 2026/5/28/9:20
# Language Version: Python 3.11 (64-bit) 
# Subject: encoding and decoding  
import string
import gensim
from gensim.utils import tokenize

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    dct_mapping_punctuation = {ch : ch for ch in (string.punctuation + string.whitespace + string.digits)}

    def __init__(self, text : str):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)


    def get_message_text(self) -> str:
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text[:]

    def get_valid_words(self) -> list[str]:
        '''
        Used to safely access a copy of self.valid_words outside of the class
        to avoid accidentally mutating class attributes.
        
        Returns: a copy of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift : int) -> dict[str, str]:
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        assert ((shift >= 0) and (shift < 26))
        lower_letters = string.ascii_lowercase
        upper_letters = string.ascii_uppercase
        dct_lower = dict({lower_letters[i] : lower_letters[(i+shift)%26] for i in range(26)})
        dct_upper = dict({upper_letters[i] : upper_letters[(i+shift)%26] for i in range(26)})
        return dct_lower | dct_upper
        

    def apply_shift(self, shift : int) -> str:
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        mapping_dct = self.build_shift_dict(shift) | self.dct_mapping_punctuation
        return str.join("", [mapping_dct[ch] for ch in self.message_text])

class PlainMessage(Message):
    def __init__(self, text : str, shift : int):
        '''
        Initializes a PlainMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlainMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self) -> int:
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self) -> dict[str, str]:
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a copy of self.encryption_dict
        '''
        return self.encryption_dict.copy() # این متدی یک کپی از این شی را بر می گرداند

    def get_message_text_encrypted(self) -> str:
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted[:] # این متدی یک کپی از این رشته را بر می گرداند

    def change_shift(self, shift : int):
        '''
        Changes self.shift of the PlainMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

class CipherMessage(Message):
    def __init__(self, text : str):
        '''
        Initializes a CipherMessage object
                
        text (string): the message's text

        a CipherMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self) -> list[tuple[int, str]] | None:
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. "best" is defined as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.
        
        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a list of tuples as the best shift values used to decrypt the message
        and the decrypted valild messages text using that shift value
        '''
        result = []
        for i in range(26):
            shifted_message = self.apply_shift(i)
            shifted_message_words = tokenize(shifted_message) # gensim.utils.tokenize()  متدی برای لیست کردن کلمات یک متن به همراه حذف کاراکتر های اضافه مثل علامت های نوشتاری است این ماژول توسط شرکت آمازون ساخته شده و در پردازش کلمات توسط هوش مصنوعی و... کاربرد دارد
            result.append((sum([word in self.valid_words for word in shifted_message_words]), i, shifted_message)) # لیستی از تاپل های سه تایی داریم عنصر اول تعداد کلمات صحیح و دومی مقدار شیفت و سومی متن رمزگشایی شده
        result = list(sorted(result))[::-1] # لیست را مرتب می کنیم سپس برعکس می کنیم تا جواب هایی با بیشترین کلمات صحیح در ابتدای لیست قرار گیرند
        result = [(result[i][1], result[i][2]) for i in range(result.__len__()) if result[i][0] == result[0][0]] #خروجی به شکل لیست از زیرا در بعضی حالت های خاص می توانیم چندین حالت درست داشته باشیم
        return result if result.__len__() != 26 else [] # اگر لیست 26 عنصر داشته باشد یعنی تمام result[i][0] برابر صفر اند. لذا با شرط گذاری خروجی تابع تهی خواهد بود

if __name__ == '__main__':

#    #Example test case (PlainMessage)
    plaintext = PlainMessage('hello', 2)
    print('\n   Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CipherMessage)
    ciphertext = CipherMessage('jgnnq')
    print('\n   Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
    encrypted_story_text = get_story_string()
    cipher_message = CipherMessage(encrypted_story_text)
    print(f"\n   Encrypted message: {cipher_message.get_message_text()}")
    
    #TODO: best shift value and unencrypted story 
    decrypted_story_result = cipher_message.decrypt_message()
    if decrypted_story_result != None:
        shift, decrypted_story_message = decrypted_story_result[0]
        print(f"\n   Decryption shift number: {shift}")
        print(f"   Decrypted message: {decrypted_story_message}")
    else: print("\nThe encrypted message cannot have any decryption. Maybe message encrypting had some issues.")
 
    
    
    
