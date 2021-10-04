import string

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

import collectiveDecision


class Example(QMainWindow):
    def __init__(self, voting, explanations, winner, tableSimile=0):
        super().__init__()
        self.voting = voting
        self.explanations = explanations
        self.winner = winner
        self.tableSimile = tableSimile

        self.initUI()

    def initUI(self):
        lbl0 = QLabel('{}'.format(self.winner), self)
        lbl0.move(10, 10)
        lbl0.adjustSize()

        lbl1 = QLabel('{}'.format(self.voting), self)
        lbl1.move(10, 45)
        lbl1.adjustSize()

        lbl2 = QLabel('{}'.format(self.explanations), self)
        lbl2.move(10, 170)
        lbl2.adjustSize()

        if self.tableSimile:
            lbl2.move(10, 280)

            lbl3 = QLabel('{}'.format(self.tableSimile), self)
            lbl3.move(10, 150)
            lbl3.adjustSize()

        self.setGeometry(250, 250, 450, 450)
        self.setWindowTitle('Результат')
        self.show()


if __name__ == '__main__':
    app = QApplication([])

    font = QFont()
    dialogFont = QFont()
    font.setFamily("Helvetica")
    font.setPointSize(16)
    QApplication.setFont(font)
    dialogFont.setPointSize(12)
    QApplication.setFont(dialogFont)

    countCandidates, ok = QInputDialog.getInt(None, 'Количество кандидатов', 'Введите количество кандидатов: ', min=3,
                                              max=5)

    listCandidates, listAlternatives = collectiveDecision.createAlternatives(countCandidates)

    votes = []
    outputVotes = []
    for j, alternative in enumerate(listAlternatives):
        a = ">".join(listAlternatives[j])
        vote, ok = QInputDialog.getInt(None, 'Количество выборщиков',
                                       f'{a}\nВведите количество голосов за эту альтернативу:')
        s = f">".join(map(str, alternative))
        textR1 = str(vote) + ": " + s
        outputVotes.append(textR1)
        votes.append(vote)
    voting = f'\n'.join(outputVotes)

    numberModel = 0
    while numberModel != 6:
        numberModel, ok = QInputDialog.getInt(None, 'Выбор модели',
                                              "1.Относительного большенства;\n"
                                              "2.Модель Кондорсе (явный победитель);\n"
                                              "3.Правило Копленда;\n"
                                              "4.Правило Симпсона;\n"
                                              "5.Модель Борда;\n"
                                              "6.Выход.\n"
                                              "\n"
                                              "Выберите модель: ", min=1, max=6)
        if numberModel == 1:
            rating, winner = collectiveDecision.relativeMajority(listCandidates[0], listAlternatives, votes)
            w = Example(voting, rating, winner)
            w.show()
            app.exec_()

        elif numberModel == 2:
            listSimile, winner = collectiveDecision.condorcet(listCandidates[0], listAlternatives, votes)
            w = Example(voting, listSimile, winner)
            w.show()
            app.exec_()

        elif numberModel == 3:
            listSimile, winner = collectiveDecision.copland(listCandidates[0], listAlternatives, votes)
            w = Example(voting, listSimile, winner)
            w.show()
            app.exec_()

        elif numberModel == 4:
            tableSimile, textListMin, winner = collectiveDecision.simpson(listCandidates[0], listAlternatives, votes)
            w = Example(voting, textListMin, winner, tableSimile)
            w.show()
            app.exec_()

        elif numberModel == 5:
            countVoters, ok = QInputDialog.getInt(None, 'Количество выборщиков', 'Введите количество выборщиков: ',
                                                  min=2, max=5)
            dictAlternatives = dict([(character, 0) for character in string.ascii_uppercase][:countCandidates])

            preferences = []
            textPreferences = []
            for i in range(countVoters):
                preference, ok = QInputDialog.getText(None, 'Упорядочивание', 'Проранжируйте кандидатов от лучшего к '
                                                                              'худшему через пробел: ')
                preference = list(preference.split())
                preferences.append(preference)
                textPreferences.append(" ".join(map(str, preference)))

            textPreferences = f'\n'.join(textPreferences)
            textDict, winner = collectiveDecision.board(countCandidates, dictAlternatives, preferences)
            w = Example(textPreferences, textDict, winner)
            w.show()
            app.exec_()

        elif numberModel == 6:
            break
