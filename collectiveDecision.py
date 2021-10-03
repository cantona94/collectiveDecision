import itertools
import math
import random
import string
import collections
import operator


def createAlternatives(countCandidates):
    listCandidates = list(
        itertools.permutations(list([(character) for character in string.ascii_uppercase][:countCandidates])))

    countAlternatives = range(0, (math.factorial(countCandidates)) - 1)
    randomAlternatives = random.sample(countAlternatives, 4)

    listAlternatives = []
    for i in range(len(randomAlternatives)):
        listAlternatives.append(listCandidates[randomAlternatives[i]])

    return listCandidates, listAlternatives


def simile(i, dictI, sign, j, dictJ):
    simile = i, dictI, sign, j, dictJ
    return " ".join(map(str, simile))


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


def condorcet(candidates, listAlternatives, votes):
    dictAlternatives = collections.defaultdict(dict)

    for candidate in candidates:
        for alternative in listAlternatives:
            for candidate2 in alternative:
                if candidate == candidate2:
                    continue
                dictAlternatives[candidate][candidate2] = 0

    for candidate in candidates:
        for i, alternative in enumerate(listAlternatives):
            for j, letter in enumerate(alternative):
                position = alternative.index(candidate)
                if letter == candidate:
                    continue
                if j > position:
                    dictAlternatives[candidate][letter] += votes[i]

    result = "Победителя нет"
    listSimile = []
    for i in dictAlternatives:
        x = 0
        for j in dictAlternatives:
            if i == j:
                continue
            if dictAlternatives[i][j] > dictAlternatives[j][i]:
                x += 1
                listSimile.append(simile(i, dictAlternatives[i][j], ">", j, dictAlternatives[j][i]))
            elif dictAlternatives[i][j] >= dictAlternatives[j][i]:
                listSimile.append(simile(i, dictAlternatives[i][j], ">=", j, dictAlternatives[j][i]))
        if x == len(dictAlternatives) - 1:
            result = ("Победитель: {0}".format(i))

    listSimile = f'\n'.join(listSimile)

    return listSimile, result


def copland(candidates, listAlternatives, votes):
    result = []
    listSimile = []
    for letter in candidates:
        x0 = 0
        for letter2 in candidates:
            if letter == letter2:
                continue

            x1, x2 = 0, 0
            for i, alternative in enumerate(listAlternatives):
                position1 = alternative.index(letter)
                position2 = alternative.index(letter2)

                if position2 < position1:
                    x1 += votes[i]
                if position2 > position1:
                    x2 += votes[i]

            if x1 < x2:
                x0 += 1
            if x1 > x2:
                x0 -= 1

        result.append(x0)

    for i, resultI in enumerate(result):
        desc = candidates[i], resultI
        listSimile.append(" ".join(map(str, desc)))

    listSimile = f'\n'.join(listSimile)
    winner = "Победитель: {0}".format(candidates[result.index(max(result))])

    return listSimile, winner


def simpson(candidates, listAlternatives, votes):
    result = []

    for letter in candidates:
        rating = []
        for letter2 in candidates:
            if letter == letter2:
                continue

            x = 0
            for i, a2 in enumerate(listAlternatives):
                position1 = a2.index(letter)
                position2 = a2.index(letter2)
                if position1 < position2:
                    x += votes[i]

            rating.append(x)
        result.append(rating)

    listMin = []
    textR = []
    for i, r in enumerate(result):
        textR1 = candidates[i], *r
        textR.append(f" ".join(map(str, textR1)))
        listMin.append(min(r))

    tableSimile = f'\n'.join(textR)
    textListMin = ' '.join(map(str, zip(candidates, listMin)))
    winner = "Победитель: {0}".format(candidates[listMin.index(max(listMin))])

    return tableSimile, textListMin, winner


def board(countCandidates, dictAlternatives, preferences):
    for preference in preferences:
        count = countCandidates - 1
        for i in preference:
            dictAlternatives[i] += count
            count -= 1

    textDict = "".join(str(dictAlternatives).replace("{", "").replace("}", ""))
    winner = "Победитель: {0}".format(max(dictAlternatives.items(), key=operator.itemgetter(1))[0])

    return textDict, winner


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

        elif numberModel == 2:
            listSimile, winner = condorcet(listCandidates[0], listAlternatives, votes)
            print(listSimile)
            print(winner)

        elif numberModel == 3:
            listSimile, winner = copland(listCandidates[0], listAlternatives, votes)
            print(listSimile)
            print(winner)

        elif numberModel == 4:
            tableSimile, textListMin, winner = simpson(listCandidates[0], listAlternatives, votes)
            print(tableSimile)
            print(textListMin)
            print(winner)

        elif numberModel == 5:
            countVoters = int(input("Введите количество выборщиков: "))
            dictAlternatives = dict([(character, 0) for character in string.ascii_uppercase][:countCandidates])

            preferences = []
            for i in range(countVoters):
                preference = list(input("Проранжируйте кандидатов от лучшего к худшему через пробеп: ").split())
                preferences.append(preference)
            textDict, winner = board(countCandidates, dictAlternatives, preferences)
            print(textDict)
            print(winner)

        elif numberModel == 6:
            break
