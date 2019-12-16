from random import randint
from itertools import combinations
import xlsxwriter


card_types = ['G', 'B', 'Y', 'P', 'R']
cards = ['B', 'B', 'B', 'B', 'B', 'G', 'G', 'G', 'G', 'P', 'P', 'P', 'R', 'R', 'Y']
bonus_2 = 2
bonus_3 = 4
bonus_4 = 10
bonus_5 = 14



def define_possible_outcomes():
    possible_sets = []
    for i in range(1,7):
        possible_sets += list(set(combinations(cards, i)))
        possible_sets.sort()
    return possible_sets


def calculate_bonus(card):
    bonus = 0
    number = set.count(card)
    if number == 2:
        bonus += bonus_2
    elif number == 3:
        bonus += bonus_3
    elif number == 4:
        bonus += bonus_4
    elif number == 5:
        bonus += bonus_5
    return bonus


def calculate_score(set):
    score = 0
    bonus = 0
    for card in set:
        if card == "B":
            score += 1
        elif card == "G":
            score += 2
        elif card == "P":
            score += 3
        elif card == "R":
            score += 4
        elif card == "Y":
            score += 5
    for type in card_types:
        bonus_to_add = calculate_bonus(type)
        bonus += bonus_to_add
        score += bonus_to_add
    result = {}
    result['bonus'] = bonus
    result['score'] = score
    return result

workbook = xlsxwriter.Workbook('scores3.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold' : True})
worksheet.write(0, 0, 'Set', bold)
worksheet.write(0, 1, 'Base score', bold)
worksheet.write(0, 2, 'Bonus', bold)
worksheet.write(0, 3, 'Final score', bold)
i = 0

for set in define_possible_outcomes():
    i += 1 
    set_score = calculate_score(set)
    set_string = ''.join(set)
    worksheet.write(i, 0, set_string)
    worksheet.write(i, 1, set_score['score']-set_score['bonus']) # Base score
    worksheet.write(i, 2, set_score['bonus']) # Bonus
    worksheet.write(i, 3, set_score['score']) # Final score

workbook.close()
