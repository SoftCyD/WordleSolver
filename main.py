#
# Wordle Solver
import os
import random
import sys


def open_words(filename):
    f = open(filename, "r")
    return f.read().splitlines()


def most_letters(listofwords):
    dict_letter = {}
    # count letters
    for wrd in listofwords:
        for letter in wrd:
            if letter in dict_letter:
                dict_letter[letter] += 1
            else:
                dict_letter[letter] = 1
    # give best word
    bestword = ''
    best = 0

    for wrd in listofwords:
        score = 0
        for letter in wrd:
            score += dict_letter[letter]
        if score > best:
            bestword = wrd
            best = score

    return bestword


def propose_word(listofremainingword, alea=False):
    if len(listofremainingword) >= 1:

        set_of_five = []
        for wrd in listofremainingword:
            if len(set(wrd)) == 5:
                set_of_five.append(wrd)
        if len(set_of_five) >= 1:
            if not alea:
                return most_letters(set_of_five)
            else:
                return set_of_five[random.randint(0, len(set_of_five) - 1)]
        else:
            return most_letters(listofremainingword)
    else:
        raise Exception('plus de mot disponible')


def filter_word(listofremainingword, a_word, the_result):
    position = 0
    for letter in a_word:
        if the_result[position] == '.':
            new_list = []
            for wrd in listofremainingword:
                if letter not in wrd:
                    new_list.append(wrd)
            listofremainingword = new_list
        elif the_result[position].islower():
            new_list = []
            for wrd in listofremainingword:
                if letter != wrd[position]:
                    new_list.append(wrd)
            listofremainingword = new_list
            new_list = []
            for wrd in listofremainingword:
                if letter in wrd:
                    new_list.append(wrd)
            listofremainingword = new_list
        elif the_result[position].isupper():
            new_list = []
            for wrd in listofremainingword:
                if letter == wrd[position]:
                    new_list.append(wrd)
            listofremainingword = new_list

        position += 1

    return listofremainingword


if __name__ == '__main__':
    print('Wordle Solver')

    list_words = open_words('resources/words_en.txt')
    print('Chargement du fichier : ' + str(len(list_words)) + ' mots disponibles')
    print('. : n''existe pas / minuscule : mal placé / majuscule : bien placé ')
    first_round = True
    while True:
        word = propose_word(list_words, alea=first_round)
        print('Proposez le mot : ' + word)
        result = input('Résultat : ')
        list_words = filter_word(list_words, word, result)
        print('Il reste ' + str(len(list_words)) + ' mots disponibles')
        if len(list_words) <= 5:
            print(', '.join(list_words))
        first_round = False
