import itertools
import math
import random
import string


def createAlternatives(countCandidates):
    listCandidates = list(
        itertools.permutations(list([(character) for character in string.ascii_uppercase][:countCandidates])))

    countAlternatives = range(0, (math.factorial(countCandidates)) - 1)
    randomAlternatives = random.sample(countAlternatives, 4)

    listAlternatives = []
    for i in range(len(randomAlternatives)):
        listAlternatives.append(listCandidates[randomAlternatives[i]])

    return listCandidates, listAlternatives


if __name__ == '__main__':
    countCandidates = int(input("Введите количество кандидатов: "))

    listCandidates, listAlternatives = createAlternatives(countCandidates)
