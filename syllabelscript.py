#skript na extrekaciu slabik z textu #WIP
#WIP
#WIP
#WIP
from nltk.corpus import cmudict
import string
phoneme_dict = dict(cmudict.entries())

def syllables_in_word(word):
    if word in phoneme_dict:   
        return len( [ph for ph in phoneme_dict[word] if ph.strip(string.ascii_letters)] )
    else:        
        return 0                           

def syllables_in_text(text):
    return sum([syllables_in_word(word.strip(string.punctuation))
                for word in text.split()])                            


text = ("Hello, how are you?")
print(syllables_in_text(text.lower()))