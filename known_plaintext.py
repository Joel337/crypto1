import random

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

    print("The keystream, based on \'" + key + "\' is: \n")
    print(index_cipher)
    
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

    return index_key

#Checks all plaintexts to look for something that resembles a key
def iterateKPs(c_string):
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

    #The ciphertext is most likely from the plaintext where the key has the least entropy. e.g. if the key is "MARY", each shift can only be by one of 4 values.  
    #The minimum count finds this reliably until the key is the length of the alphabet.  At that point we would need to add some features. 
    return counts.index(min(counts))


#
kp = kp4
print("This is a test. Change the kp value to switch to another known plaintext")
x = str(input("Insert key: "))
ret = encrypt(kp.upper(), x.upper())
#print ("returned ciphertext is: \n" + ret)
prob_KP = iterateKPs(ret.upper())
answer = ""
if prob_KP == 0:
   answer = kp1
if prob_KP == 1:
   answer = kp2
if prob_KP == 2:
   answer = kp3
if prob_KP == 3:
   answer = kp4
if prob_KP == 4:
   answer = kp5

print("Probable known plaintext is case " + str(prob_KP+1))
print("That plaintext is: " + answer)
