import random, itertools, math, sys
from collections import Counter, OrderedDict

#constants
IN_LENGTH = 500
KEY_LENGTH = 25
UPPER = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = " abcdefghijklmnopqrstuvwxyz"
kp1 = ("cabooses meltdowns bigmouth makework flippest neutralizers gipped mule antithetical imperials carom masochism stair retsina dullness adeste corsage "
"saraband promenaders gestational mansuetude fig redress pregame borshts pardoner reforges refutations calendal moaning doggerel dendrology governs "
"ribonucleic circumscriptions reassimilating machinize rebuilding mezcal fluoresced antepenults blacksmith constance furores chroniclers overlie hoers "
"jabbing resigner quartics polishers mallow hovelling ch")
kp2 = ("biorhythmic personalizing abjure greets rewashed thruput kashmir chores fiendishly combatting alliums lolly milder postpaid larry annuli codgers apostatizing "
"scrim carillon rust grimly lignifying lycanthrope samisen founds millimeters pentagon humidification checkup hilts agonise crumbs rejected kangaroo forenoons grazable acidy "
"duellist potent recyclability capture memorized psalmed meters decline deduced after oversolicitousness demoralizers ologist conscript cronyisms melodized girdles nonago")
kp3 = ("hermitage rejoices oxgall bloodstone fisticuff huguenot janitress assailed eggcup jerseyites fetas leipzig copiers pushiness fesse precociously modules navigates "
"gaiters caldrons lisp humbly datum recite haphazardly dispassion calculability circularization intangibles impressionist jaggy ascribable overseen copses devolvement "
"permutationists potations linesmen hematic fowler pridefully inversive malthus remainders multiplex petty hymnaries cubby donne ohioans avenues reverts glide photos antiaci")
kp4 = ("leonardo oxygenate cascade fashion fortifiers annelids co intimates cads expanse rusting quashing julienne hydrothermal defunctive permeation sabines hurries "
"precalculates discourteously fooling pestles pellucid circlers hampshirites punchiest extremist cottonwood dadoes identifiers retail gyrations dusked opportunities ictus "
"misjudge neighborly aulder larges predestinate bandstand angling billet drawbridge pantomimes propelled leaned gerontologists candying ingestive museum chlorites maryland s")
kp5 = ("undercurrents laryngeal elevate betokened chronologist ghostwrites ombres dollying airship probates music debouching countermanded rivalling linky wheedled heydey sours "
"nitrates bewares rideable woven rerecorded currie vasectomize mousings rootstocks langley propaganda numismatics foetor subduers babcock jauntily ascots nested notifying "
"mountainside dirk chancellors disassociating eleganter radiant convexity appositeness axonic trainful nestlers applicably correctional stovers organdy bdrm insis")

dictionary = ["awesomeness", "hearkened", "aloneness", "beheld", "courtship", "swoops", "memphis", "attentional", "pintsized", "rustics", "hermeneutics", "dismissive",
              "delimiting", "proposes", "between", "postilion", "repress", "racecourse", "matures", "directions", "pressed", "miserabilia", "indelicacy", "faultlessly",
              "chuted", "shorelines", "irony", "intuitiveness", "cadgy", "ferries", "catcher", "wobbly", "protruded", "combusting", "unconvertible", "successors", "footfalls",
              "bursary", "myrtle", "photocompose"]

#This function can be used to encrypt a plain-text with a random non-repeating key based on an input key
def encrypt(string, key):
    index_done = []
    index_cipher = []
    string_ciphered = ""
    i = 0

    print("Your key is " + key + " of length " + str(len(key)))

    # generate a randon keystream based on shifts from the given key and save into an array (index_cipher)
    while len(index_cipher) < len(string):
        key_index = key[random.randint(0, len(key)-1)]
        #print("Key index " + str(key_index))

        rand_fromKey = UPPER.find(key_index)
        #print("rand_fromKey: " + str(rand_fromKey))
        index_cipher.append(rand_fromKey)

    #print("The keystream, based on \'" + key + "\' is: \n")
    #print(index_cipher)

    # turn the input string into an array of numerical values. Using all caps ("UPPER")
    while i < len(string):
        index = UPPER.find(string[i])
        index_done.append((index + index_cipher[i]) % len(UPPER))
        i=i+1

    for character in index_done:
        string_ciphered+=UPPER[character]

    return string_ciphered

#given a known plaintext and a ciphered string, find the key for 'length' chars
def forceKey(kp, c_string, length):
    index_kp = []
    index_c = []
    index_key = []

    if length > len(kp) or length > len(c_string):
        print("breaking, text is smaller than key length")
    else:
        i = 0
        while i  < length:
            index_kp.append(UPPER.find(kp[i]))
            index_c.append(UPPER.find(c_string[i]))
            index_key.append((((26 + index_c[i]) - index_kp[i]) % 27) + 1)
            i+=1
    #print("cipher text was " + c_string + " looking for " + kp + ". Returning:")
    #print(index_key)
    return index_key

#Checks all plaintexts to look for something that resembles a key. return the index of the KP and update the confidence value to the delta between the index sizes.
def iterateKPs(c_string, confidence):
    list = [kp1, kp2, kp3, kp4, kp5]
    counts =[]

    #go through each known plaintext and get the first part of the key (3x the max key length, assuming that plaintext
    for item in list:
        result_key = forceKey(item.upper(), c_string.upper(), KEY_LENGTH*3)
        values = []
        counter = 0
        #count the number of unique values in the resulting key.  If the count is > the keylength, we know it cannot be the key
        #(but for the random values).  For the test code, I don't use this though.
        for value in result_key:
            if value not in values:
                counter+=1
                values.append(value)
        counts.append(counter)


    #Find the comparative index lengths to determine confidence.  A large gap indicates higher confidence.
    counts_copy = counts
    m1 = sorted(counts_copy)[0]
    m2 = sorted(counts_copy)[1]
    confidence = int(m2)-int(m1)
    #The ciphertext is most likely from the plaintext where the key has the least entropy. e.g. if the key is "MARY", each shift can only be by one of 4 values.
    #The minimum count finds this reliably until the key is the length of the alphabet.  At that point we would need to add some features.
    return counts.index(min(counts)), confidence

#find the minimum number of characters needed to create a key for the word.  We pass back all shifts of that minimum length.
def findPossibileWords(word, ciphertext, minWordKeys):
    keyspace = 99
    keySequence = []
    redundant = []
    cipher_copy = ciphertext

    while len(cipher_copy) >= len(word):
        key_index = forceKey(word.upper(), cipher_copy.upper(), len(word))
       
        if len(set((key_index))) < keyspace:
            keyspace = len(set(key_index))
            keySequence = key_index
            redundant = []
        #testing looking for othe shifts of the same length
        if len(set(key_index)) == keyspace:
            if sorted(set(key_index)) not in redundant:
                redundant.append(sorted(set(key_index)))

        cipher_copy = cipher_copy[1:]
        #print(cipher_copy)
        #print("keyspace: " + str(keyspace))
    #print("for word " + word + " the redundancy array length is " + str(len(redundant)))
    minWordKeys.append(keySequence)
    if len(redundant) > 0:
        for item in redundant:
           minWordKeys.append(item)

#this version of the code looks for possible keys that overlap with eachother, and builds on that, adding values based on the output of findPossibleWords.
def getCommonality(word_index_info):
    jointIndex = []
    ordered = []
    #print(word_index_info)

    for item in word_index_info:
        ordered.append(item)
        ordered = sorted(ordered, key=len)
    
    max = 0
    root = []

    for a, b in itertools.permutations(ordered[:12], 2):
        common = len(set(a) & set(b))
        distinct = (len(set(a) | set(b)))
        #print("comparing ")
        #print(a, b)
        #First find the pair with the greatest commonality. 
        if (common / distinct * 100) > max:
            max = (common / distinct * 100)
            jointIndex = a + b
            #print((common / distinct * 100))
    
    print("Max:" + str(max))
    print("Initial key guess if this is a test 2 case: ")
    print(set(jointIndex))
    #if we don't have super high overlap, we add additional characters based on their frequency of appearance.  I don't know the right number of additions.
    if max < 70:
        merged = itertools.chain.from_iterable(ordered)
        count = Counter(merged)
        count = count.most_common()
        #print(count)
        i = 0
        while i < 5: #we're doing 5 chars?
            jointIndex.append(list(count)[i][0])
            #print("added " + str(list(count)[i][0]))
            i+=1

        #print("Bigword Shift frequency: ")
        #print(count[:10])

    shift_counter = Counter()
    for words in dictionary:
        counting(words.upper(), ret, shift_counter)

    #print("Adding chars from the overall shift counter")
    #print(shift_counter.most_common())

    # #From the root common pair, add other keys as appropriate. In short, trying to improve accuracy here by checking for additional overlap and extending the possible key
    j = 0
    while j < len(word_index_info):
        #print("checking against: ")
        #print(set(word_index_info[j]))
        common = (set(jointIndex) & set(word_index_info[j]))
        #print("Common: " + str(common))
        distinct = newShifts(set(jointIndex), word_index_info[j])
          
        #check if there are triple the characters already accepted as compared to new characters.
        if len(distinct) != 0 and (len(common) / len(distinct)) > 3:
            jointIndex += set(word_index_info[j])
            #print("added " + str(set(distinct)))
        j+=1

    jointIndex = list(set(jointIndex))
    print("Final key guess if this is a test 2 case: ")
    print(set(jointIndex))

    return jointIndex

def newShifts(base, new):
    distinct = []
    for item in new:
        if item not in base:
            distinct.append(item)

    return set(distinct)

def forceDict(cipher_text, key_guess):
    dictionary2 = sorted(dictionary, key=len, reverse=True)
    found_counter = 0
    i = 0
    decrypted = ""
    while i < len(cipher_text):
        flow_control = 0
        for word in dictionary2:
            if testWord(word, cipher_text[i:(i+len(word)+1)], key_guess):
                decrypted+=(word + " ")
                found_counter += 1
                i+=(len(word)+1)
                flow_control = 1
        if flow_control == 0:
            decrypted+=cipher_text[i]
            i+=1

    return decrypted, found_counter

def subtract_letters(message_in, cipher_in):
    #using letter_key to save one stepp

    out_location = ((UPPER.find(cipher_in)-LOWER.find(message_in)) % 27)

    #wrapping around should the subtraction end up below zero
    return UPPER[out_location];

# Start Backup Test
def test_1_backup(plaintext, cipher):
    key_guess_out = "";
    #random_characters;
    k=len(cipher)-500;
    length=4;
    skip=-1
    skip2=-1
    key_iteration_results = test_1_backup_key_reveal_itteration(plaintext, cipher, length, skip, skip2);
    key_iteration_top = math.ceil(key_iteration_results[2]);
    #itterates through the potential plain texts to find results
    while key_iteration_top<=0 and length<25:
        if(skip2<length):
            skip2+=1;
        elif(skip<length):
            skip+=1
            skip2=skip+1;
        else:
            length+=1
            skip=-1
            skip2=-1;
        key_iteration_results = test_1_backup_key_reveal_itteration(plaintext, cipher, length, skip, skip2);
        key_iteration_top = math.ceil(key_iteration_results[2]);
        pass
    return key_iteration_results;

def test_1_backup_key_reveal_itteration(plaintext, cipher, length, skip, skip2):
    message_out = 0
    key_out = ""
    j=0;
    i=0;
    correct_guess = 0
    key_out = 0;
    while j<5:
        i=0;
        key_guess = [];
        counter = 0;
        letter_key_counter = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,"N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0," ":0}
        # new
        key_array = set()
        skip_shift=0;
        while i<500 and len(key_array)<length:
            if(skip == i):
                i+=1;
                skip_shift+=1;
            if(skip2 == i):
                i+=1;
                skip_shift+=1;
            potential_key = subtract_letters(plaintext[j][i-skip_shift],cipher[i]);
            if letter_key_counter[potential_key]==0:
                letter_key_counter[potential_key]+=1;
                key_array.add(potential_key)

            i+=1;

            pass
        key_verified = test_1_verify__key(cipher, plaintext[j], key_array)
        if key_verified>0:

            if correct_guess == 0:
                key_out = key_array
                message_out = j
                correct_guess = 1
            else:
                key_out = -1;
        skip_shift = 0;
        j+=1;
    pass
    if key_out == -1:
        correct_guess = 0;
    return [key_out, message_out, correct_guess];

def test_1_verify__key(cipher, plaintext_value, key_array):
    #key verification is done by calculating the number of random characters that are found using a giving key.  If the random characters is an exact match, the key is 100% accurate
    number_of_randoms_expected = len(cipher)-500;
    number_of_randoms_recieved = 0;
    length_of_cipher = len(cipher);

    #position in message
    i=0;
    #position in cipher
    j=0;
    letter_key_counter = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,"N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0," ":0}
    while j<length_of_cipher and i<500:
        potential_key_value = subtract_letters(plaintext_value[i],cipher[j]);
        letter_key_counter[potential_key_value]+=1;
        if potential_key_value in key_array:
            i+=1
            j+=1
        else:
            j+=1
            number_of_randoms_recieved+=1
    if number_of_randoms_recieved!=number_of_randoms_expected:
        return 0;
    elif(number_of_randoms_recieved == number_of_randoms_expected):
        return 1;






#This does a character by character analyis to see if the word can be formed from the probable key
def testWord(word, cipher_text, key_guess):
    validity_array = []
    random_used = False
    rand_value = int()
    i = 0
    word=word.upper()+" "
    if len(word) > len(cipher_text):
       #word=word[0:len(cipher_text)] #this doesn't appear to be working, instead we will just give up on partial words for now
       return False
    while i < (len(word)-1):
        reqValue = ((UPPER.find(cipher_text[i]) - UPPER.find(word[i])) % 27) 
        #print("cipher " + cipher_text[i]+ "and the word character " + word[i] + " looking for " + str(reqValue))
        #the best case is that the chars line up directly with a possible key value (no random injected characters. If they line up, add a 1 to the array.
        if reqValue in key_guess:
            validity_array.append(1)
        #This is a test case for dealing with randomness. Right now it doesn't work, as it lets way too many words in.
        #elif (i+1 < len(word)) and (((UPPER.find(cipher_text[i+1]) - UPPER.find(word[i])) % 27) in key_guess):
        #    j = i+2
        #    valid2 = []
        #    rand_value = (UPPER.find(cipher_text[i+1]) - UPPER.find(word[i]) % 27)
        #    while j<(len(word)-1):
        #        reqValue2 = ((UPPER.find(cipher_text[j]) - UPPER.find(word[j-1])) % 27)

        #        if reqValue2 in key_guess:
         #           valid2.append(1)
         #       else:
         #           valid2.append(0)
         #       j+=1
         #   if sum(valid2) == len(valid2):
         #       
         #       return True
         #   else:
         #       validity_array.append(0)
        else:
            validity_array.append(0)
        i+=1
    
    #We can look at how many valid chars we have and how many invalid chars we have. Not clear to me what the right number is here.
    if (len(word) - sum(validity_array)) > 2:
        return False
    else:
        return True

def counting(word, ciphertext, shift_counter):
    keySequence = []
    cipher_copy = ciphertext

    while len(cipher_copy) >= len(word):
        key_index = forceKey(word.upper(), cipher_copy.upper(), len(word))
        keySequence += key_index
        cipher_copy = cipher_copy[1:]

    shift_counter.update(keySequence)

#Here's our driver code
user_input = input("Insert ciphertext or enter 't' to go into testing mode: ")
ret = user_input
if user_input == "t":
    kp = input("Input your plaintext or enter 1-5 for a known plaintext: ")
    if kp == "1":
       kp = kp1
    if kp == "2":
       kp = kp2
    if kp == "3":
       kp = kp3
    if kp == "4":
       kp = kp4
    if kp == "5":
       kp = kp5
    x = str(input("Insert key: "))
    ret = encrypt(kp.upper(), x.upper())

confidence = 0

#print ("returned ciphertext is: \n" + ret)
prob_KP = iterateKPs(ret.upper(), confidence)
answer = ""
if prob_KP[0] == 0:
   answer = kp1
if prob_KP[0] == 1:
   answer = kp2
if prob_KP[0] == 2:
   answer = kp3
if prob_KP[0] == 3:
   answer = kp4
if prob_KP[0] == 4:
   answer = kp5

confidence = prob_KP[1]
#if the confidence is higher than 5, we have likely found a known plaintext. We can also return that answer and break before processing the case 2 stuff.
if confidence > 5:
    print("Probable known plaintext is case " + str(prob_KP[0]+1))
    print("That plaintext is: " + answer)
    print("The probable key is: ")
    print(test_1_backup([kp1,kp2,kp3,kp4,kp5], ret));
    sys.exit("Exiting. Thank you.")

backup_results = test_1_backup([kp1,kp2,kp3,kp4,kp5], ret)
if  backup_results[2]>0:
    print("Probable known plaintext is case " + str(backup_results[1]+1))
    print("Probable Key is ", end="")
    print(backup_results[0])
    sys.exit("Exiting. Thank you.")

#Start looking at the dictionary/begin case 2 analysis. Right now it has a few large words. I think a better approach may be to pick words with as many different chars as possible
bigwords = ["intuitiveness", "faultlessly", "hermeneutics", "unconvertible", "photocompose", "awesomeness", "attentional", "miserabilia"]

minWordKeys = []
for word in bigwords:
    findPossibileWords(word.upper(), ret.upper(), minWordKeys)

keyGuess = getCommonality(minWordKeys)

decryption = forceDict(ret, keyGuess)


if decryption[1] > 40 and backup_results[2]==0:
    print("We are guessing this is a case two text, and our decryption guess is: \n")
    print(decryption[0])

elif (decryption[1] < 25 and confidence > 2 ):
    print("We aren't really sure on this one, we are guessing a known plaintext, " + str(prob_KP[0]+1))
    print(answer)
else:
    print("You won this round, we don't know. In an attempt to salvage some credit, here are our guesses:")
    print("maybe known plaintext " + str(prob_KP[0]+1) + " or a case two text decrypted as follows: ")
    print(decryption[0])

