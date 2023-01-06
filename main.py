#
# Wordle Solver
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
        set_of_five = [wrd for wrd in listofremainingword if len(set(wrd)) == 5]
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
            listofremainingword = [wrd for wrd in listofremainingword if letter not in wrd]
        elif the_result[position].islower():
            listofremainingword = [wrd for wrd in listofremainingword if letter != wrd[position]]
            listofremainingword = [wrd for wrd in listofremainingword if letter in wrd]
        elif the_result[position].isupper():
            listofremainingword = [wrd for wrd in listofremainingword if letter == wrd[position]]
        position += 1

    return listofremainingword


if __name__ == '__main__':

    sys.stdout.reconfigure(encoding='utf-8')

    print('Wordle Solver')

    lang = input('ENTREZ : fr en es de it ? ')
    if lang == '':
        lang = 'fr'

    list_words = open_words('resources/words_' + lang + '.txt')
    print(f'Chargement du fichier {lang} :  {str(len(list_words))} mots disponibles')
    print('. : n''existe pas / minuscule : mal placé / majuscule : bien placé ')

    propositions = input('liste de mots à proposer  (séparés par un espace, vide sinon) : ?')
    propositions = [] if propositions.strip() == '' else propositions.strip().split(' ')
    first_round = True
    while True:
        if len(propositions) > 0:
            word = propositions.pop(0)
        else:
            word = propose_word(list_words, alea=first_round)
        result = input('Proposez le mot \'' + word + '\' -> résultat = ')
        list_words = filter_word(list_words, word, result)
        print('Il reste ' + str(len(list_words)) + ' mots disponibles')
        if 1 < len(list_words) <= 5:
            print(', '.join(list_words))
        first_round = False
