import random
from random import randrange
import math


dictionary_array = ["awesomeness", "hearkened", "aloneness", "beheld", "courtship", "swoops", "memphis", "attentional", "pintsized", "rustics", "hermeneutics", "dismissive",
              "delimiting", "proposes", "between", "postilion", "repress", "racecourse", "matures", "directions", "pressed", "miserabilia", "indelicacy", "faultlessly",
              "chuted", "shorelines", "irony", "intuitiveness", "cadgy", "ferries", "catcher", "wobbly", "protruded", "combusting", "unconvertible", "successors", "footfalls",
              "bursary", "myrtle", "photocompose"]



def count_letter_pairings():
    letter_pairs = {};
    global dictionary_array;
    letter_pairs;
    for dictionary_word in dictionary_array:
        dictionary_word = ' '+dictionary_word+' '
        i=0;
        last_letter = len(dictionary_word);
        while i<last_letter:
            letter_pairs[dictionary_word[i]]={};
        #    letter_pairs.add(new_addition);
            i+=1;
        pass

    for dictionary_word in dictionary_array:
        dictionary_word = ' '+dictionary_word+' '
        i=0;
        last_letter = len(dictionary_word)-1;
        while i< last_letter:
            #new_addition = dictionary_word[i] + dictionary_word[i+1]
            letter_pairs[dictionary_word[i]][dictionary_word[i+1]]= dictionary_word;

        #   letter_pairs.add(new_addition);
            i+=1;
        pass
    for dictionary_word in dictionary_array:
        dictionary_word = ' '+dictionary_word+' '
        i=0;
        while i<len(dictionary_word)-2:
            if(isinstance(letter_pairs[dictionary_word[i]][dictionary_word[i+1]], str)):
                letter_pairs[dictionary_word[i]][dictionary_word[i+1]]={};

            letter_pairs[dictionary_word[i]][dictionary_word[i+1]][dictionary_word[i+2]]=dictionary_word;
            #   letter_pairs.add(new_addition);
            i+=1;
        pass
    for dictionary_word in dictionary_array:
        dictionary_word = ' '+dictionary_word+' '
        i=0;
        while i<len(dictionary_word)-3:
            if(isinstance(letter_pairs[dictionary_word[i]][dictionary_word[i+1]][dictionary_word[i+2]], str)):
                letter_pairs[dictionary_word[i]][dictionary_word[i+1]][dictionary_word[i+2]]={};

            letter_pairs[dictionary_word[i]][dictionary_word[i+1]][dictionary_word[i+2]][dictionary_word[i+3]]=dictionary_word;
            #   letter_pairs.add(new_addition);
            i+=1;
        pass



    return letter_pairs;

l3tter_input = [];

quick_dictionary = count_letter_pairings()

first_letter  = input('Choose First Letter: ').lower();
if(first_letter not in quick_dictionary):
    print('Letter not found in dictionary');
    exit();

print('CMD: print(quick_dictionary[first_letter]);');
print(quick_dictionary[first_letter]);
second_letter = input('Choose Second Letter: ').lower();

if(second_letter not in quick_dictionary[first_letter]):
    print('Letter Pair Not Found in Dictionary');
    exit();

print(quick_dictionary[first_letter][second_letter]);


third_letter = input('Choose Third Letter: ').lower();

if(third_letter not in quick_dictionary[first_letter][second_letter]):
    print('Letter Pair Not Found in Dictionary');
    exit();
print(quick_dictionary[first_letter][second_letter][third_letter]);
