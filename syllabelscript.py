#import nltk.corpus.cmudict  # this does not work!?!?
from nltk.corpus import cmudict
import string
phoneme_dict = dict(cmudict.entries())

def syllables_in_word(word):
    '''Attempts to count the number of syllables in the string argument 'word'.
    
    Limitation: word must be in the CMU dictionary (but that was a premise of the Exercise)
    "Algorithm": no. syllables == no. (0,1,2) digits in the dictionary entry, right??        
    '''
    
    # although listcomps may be readable, you can't insert print statements to instrument them!!
    if word in phoneme_dict:   
        #return sum([ phoneme.count(str(num)) for phoneme in phoneme_dict[word] for num in range(3) ])
        return len( [ph for ph in phoneme_dict[word] if ph.strip(string.ascii_letters)] )   # more destructive; less efficient? NO! see timeit results in my comments below
    else:        
        return 0                           
    

def syllables_in_text(text):
    '''Attempts to count the number of syllables in the string argument 'text'.
    
    Limitation: any "internal punctuation" must be part of the word. (it wouldn't get "this,and" correctly)
    Lets syllables_in_word do the heavy lifting.
    '''

    # ok, so apparently str.split(delim) only works for A SINGLE CHAR delim...
    # anything fancier, and you might want a regex (and its associated performance penalty)
    return sum([syllables_in_word(word.strip(string.punctuation))       # but str.strip(delims) will strip all leading and trailing chars in "delims"!
                for word in text.split()])                              # - alternatives at http://stackoverflow.com/questions/265960/    
    
    

print(syllables_in_text("potato is perfect"))