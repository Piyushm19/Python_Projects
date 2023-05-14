import re
from matplotlib import pyplot as plt

# This includes Part A
def Tokenizer(tokens, string):
    tokenized = []
    # Opening input file
    file1 = open(string, "r")
    
    # Indexing for each line 
    for line in file1.readlines():
        # Stripping the new line char and split into strings at new space
        line = line.strip('\n') 
        # Turn each word into lowercase
        for term in line.split(): 
            term = term.lower()
            def tokenize(term):             
                punc = []
                if term == "one's":
                    x = 0
                for char in term:
                    # print(term)
                    if (not char.isalnum() and char != "'" and not char in punc):
                        punc.append(char)

                #if no punc found, append the term
                if (punc == []):
                    term = term.replace("'", '')
                    term = term.replace('"', '')
                    tokenized.append(term)
                else:
                    x = 0
                    for i in punc:
                        term = term.replace(i, " ")
                        term = term.replace("'", '')
                        term = term.replace('"', '')
                        if punc.index(i) == len(punc) - 1:
                            add = term.split(" ")
                            for j in add:
                                if j != "":

                                    tokenized.append(j)
            pattern = re.findall((r"\b(?:[a-z]\.){2,}"), term)
#check if it's an abbreviation, if its not an abbreviation tokenize, if it is then process . and also 's
            if len(pattern) == 1:
                index = term.index(pattern[0])   
                if index > 0:
                    for i in range(0, index):
                        if term[i].isalnum():
                            tokenize(term)
                        else:
                            continue
                                   
                if term.endswith(pattern[0]) or (len(term) == index + len(pattern[0]) + 2 and term.endswith("'s")):         
                    if term.endswith("'s"): #or term.endswith("'s."):
                        term = term.replace("'", '')
                    term = term.replace('.', '')
                    tokenize(term)   
                elif("'s" in term and (term.index("'s") == index + len(pattern[0]) + 1)):
                    end = index + len(pattern[0])   
                    for i in range(end + 2, len(term)):
                        if term[i].isalnum():
                            tokenize(term)
                            break
                        else:
                            term = term.replace('.', '')
                            tokenize(term)
                            break
                else:
                    end = index + len(pattern[0])
                    for i in range(end, len(term)):
                        if term[i].isalnum():
                            tokenize(term)
                            break
                        else:
                            term = term.replace('.', '')
                            tokenize(term)
                            break
            else:
                tokenize(term)

    file1.close()
    return tokenized
# stopwords removal function 
# stopword removal on the tokens then put the tokens in a set
def removeStopwords(tokens, stop):
    arr = []
    for term in tokens:
        if (stop.get(term, "Not Found") != "Not Found"):
            pass
        else:
            arr.append(term)
    return arr

# now perform stemming on the tokens
def stemming(tokens):

    def hasVowel(string):
        if ('a' in string or 'e' in string or 'i' in string or 'o' in string or 'u' in string):
            return True
        else:
            return False

    def helperB(term, ending, length):
        tempWord = term.replace(ending, '')
        if hasVowel(tempWord):
            if(tempWord.endswith('at') or tempWord.endswith('bl') or tempWord.endswith('iz')):
                return tempWord + 'e'
            elif (tempWord[-1] == tempWord[-2] and not tempWord.endswith('ll') and not tempWord.endswith('ss') and not tempWord.endswith('zz')):
                return tempWord[0:-1]
            elif (len(tempWord) <= 3):
                return tempWord + 'e'
            else:
                return tempWord
        else:
            return tempWord

    tempListA = []
    tempListB = []
    for term in tokens:
        # go largest to smallest: ends in sses then ied or ies then ss/us then s
        if (term.endswith('sses')):
            tempListA.append(term.replace('sses', 'ss'))
        elif ((term.endswith('ied')) or term.endswith('ies')):
            if (len(term) > 4):
                if(term.endswith('ied')):
                    tempListA.append(term.replace('ied', 'ie'))
                else:
                    tempListA.append(term.replace('ies', 'ie'))
            else:
                if(term.endswith('ied')):
                    tempListA.append(term.replace('ied', 'i'))
                else:
                    tempListA.append(term.replace('ies', 'i'))
        elif ((term.endswith('ss')) or (term.endswith('us'))):
            pass
        elif (term.endswith('s')):
            if(hasVowel(term[0:-2])):
                tempListA.append(term.replace('s', ''))
            else:
                tempListA.append(term)
        else:
            tempListA.append(term)
                
    #look at 1b stem rules   
    for term in tempListA:
        if(term.endswith('eedly')):
            word = term[0:-6]
            if hasVowel(word):
                if (not hasVowel(term[-6])):
                    tempListB.append(term.replace('eedly', 'ee'))
                else:
                    tempListB.append(term)
            else:
                tempListB.append(term)
        elif(term.endswith('edly')):
            word = term[0:-5]
            if hasVowel(word):
                if not hasVowel(term[-5]):
                    tempListB.append(term.replace('eedly', 'ee'))
                else:
                    tempListB.append(term)
            else:
                tempListB.append(term)
        elif term.endswith('ingly'):
            tempListB.append(helperB(term, 'ingly', 5))
        elif term.endswith('edly'):
            tempListB.append(helperB(term, 'edly', 4))
        elif term.endswith('ing'):
            tempListB.append(helperB(term, 'ing', 3))
        elif term.endswith('ed'):
            tempListB.append(helperB(term, 'ed', 2))
        else:
            tempListB.append(term)

    return tempListB



# This includes Part B and calls stuff needed for Part A             
def mainFunc():
    # Creating dictionary for stop words txt file
    stop = {}
    # Retrieving stop words and inputing into dictionary
    stopF = open('stopwords.txt', 'r')
    for item in stopF.readlines():
        item = item.strip('\n')
        stop.update({item : item})
    stopF.close()
    # Creating an array to store the tokens
    tokens = []
    tokens = Tokenizer(tokens, "tokenization-input-part-A.txt")
    tokens = removeStopwords(tokens, stop) 
    tokens = stemming(tokens)

    f = open("tokenized.txt", "w")
    for term in tokens:
        f.write(term + '\n')
    f.close()
    tokens = []
    tokens = Tokenizer(tokens, 'tokenization-input-part-B.txt')
    x = 0
    tokens = removeStopwords(tokens, stop)
    tokens = stemming(tokens)
    #Getting counts of all the words in Moby-Dick
    countDict = {}
    for tok in tokens:
        if (countDict.get(tok, "Not Found") != "Not Found"):
            countDict.update({tok : (countDict.get(tok) + 1)})
        else:
            countDict.update({tok: 1})

    def helper300(count, top):
        num = 0
        while num < 300:
            max_key = max(count, key=count.get)
            count.pop(max_key)
            top.append(max_key)
            num = num + 1
        return top

    count = countDict.copy()
    top = list([])
    top = helper300(count, top)

    f = open("terms.txt", "w")
    for term in top:
        string = str(term) + ' ' + str(countDict.get(term)) + '\n'
        f.write(string)
    f.close()


if __name__ == '__main__':
    mainFunc()


