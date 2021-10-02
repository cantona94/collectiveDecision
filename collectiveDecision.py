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


def votes(listAlternatives):
    votes = []
    for j in range(len(listAlternatives)):
        print(listAlternatives[j], end=' ')
        vote = int(input("Введите количество голосов за эту альтернативу: "))
        votes.append(vote)

    return votes


def relativeMajority(candidates, listAlternatives, votes):  # Относительное большинство
    rating = []
    for letter in candidates:
        ratingLetter = []
        for i, alternative in enumerate(listAlternatives):
            if alternative.index(letter) == 0:
                ratingLetter.append(votes[i])

        rating.append(ratingLetter)

    description = []
    winner = []
    for i, r in enumerate(rating):
        desc = candidates[i], sum(r)
        winner.append(sum(r))
        description.append(" ".join(map(str, desc)))

    winner = "Победитель: {0}".format(candidates[winner.index(max(winner))])
    description = f'\n'.join(description)

    return description, winner


if __name__ == '__main__':
    countCandidates = int(input("Введите количество кандидатов: "))

    listCandidates, listAlternatives = createAlternatives(countCandidates)
    votes = votes(listAlternatives)

    numberModel = 0
    while numberModel != 6:
        numberModel = int(input("1.Относительного большенства;\n"
                                "2.Модель Кондорсе (явный победитель);\n"
                                "3.Правило Копленда;\n"
                                "4.Правило Симпсона;\n"
                                "5.Модель Борда;\n"
                                "6.Выход.\n"
                                "Выберите модель: "))
        if numberModel == 1:
            rating, winner = relativeMajority(listCandidates[0], listAlternatives, votes)
            print(rating)
            print(winner)

        elif numberModel == 6:
            break
