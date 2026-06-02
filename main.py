#
# Wordle Solver
import random
import sys


def open_words(filename):
    f = open(filename, "r")
    return f.read().splitlines()


def find_best_word(listofwords):
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
        memletter = set()
        for letter in wrd:
            if letter not in memletter:
                score += dict_letter[letter]
                memletter.add(letter)
        if score > best:
            bestword = wrd
            best = score

    return bestword


def propose_word(listofremainingword, alea=False):
    if len(listofremainingword) >= 1:
        set_of_unik_letters = [wrd for wrd in listofremainingword if len(set(wrd)) == len(listofremainingword[0])]
        if len(set_of_unik_letters) >= 1:
            if not alea:
                return find_best_word(set_of_unik_letters)
            else:
                return set_of_unik_letters[random.randint(0, len(set_of_unik_letters) - 1)]
        else:
            return find_best_word(listofremainingword)
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

    lang = input('ENTREZ : fr4 fr5 fr6 en es de it ? ')
    if lang == '':
        lang = 'fr6'

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
