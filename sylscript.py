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

def get_communication_records(filename):
    f = open(filename, "r")
    file_content= f.read()

    file_content_split = file_content.split("\n\n")

    communication_strings = []
    for stringgg in file_content_split:
        if stringgg.startswith("((FROM"):
            communication_strings.append(stringgg)
    return communication_strings

def get_direction_from_communication_record(record):
    if record[7] == "F":
        return "AP1"
    return "PA1"

def get_text_from_communication_record(record):
    string = record.split("(TEXT ")[1]
    open_parentheses = 1
    output = ""
    for char in string:
        if char == "(":
            open_parentheses += 1
        if char == ")":
            open_parentheses -= 1
            continue
        if open_parentheses == 0:
            break
        if open_parentheses == 1:
            output += char
    return output

def get_duration_from_communication_record(record):
    string = record.split("(TIMES")[1]
    # remove rear parentheses
    
    float_string = ""
    for char in string:
        if char == ")":
            break
        float_string += char
        
    float_strings = float_string.split(" ")

    duration = float(float_strings[2]) - float(float_strings[1])
    return duration

communication_records = get_communication_records("bos.txt") 
f = open("tempoformatted.txt","a")     

for record in communication_records:
    direction = get_direction_from_communication_record(record)
    text = get_text_from_communication_record(record)
    duration = get_duration_from_communication_record(record)    
    syll = syllables_in_text(text.lower())
    tempo = syll/duration
    tempo = str(tempo)
    print (direction, tempo)
    f.write(direction)
    f.write("\n")
    f.write(tempo)
    f.write("\n")    
f.close()
    
    



    

    


