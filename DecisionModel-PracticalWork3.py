import csv
import math
import operator

import numpy as np

votes = []
with open("data.csv", newline='') as csvFile:
    data = csv.reader(csvFile, delimiter=',')
    for row in data:
        row[4] = int(row[4])
        votes.append(row)


# Compare the ranking of 2 candidates
def MajorityRule(c1, c2):
    ans1 = 0
    ans2 = 0
    for vote in votes:
        for v in vote:
            if v == c1:
                ans1 += vote[4]
                break

            elif v == c2:
                ans2 += vote[4]
                break

    if ans1 > ans2:
        return c1
    else:
        return c2


MajorityRule('a', 'b')
print("(a) MajorityRule: winner is", MajorityRule('a', 'b'))


# Plurality: only check the first preference, the maximum number of voting win

def Plurality(c1, c2, c3, c4):
    cal_a = cal_b = cal_c = cal_d = 0
    for vote in votes:
        if vote[0] == c1:
            cal_a += vote[4]
        elif vote[0] == c2:
            cal_b += vote[4]
        elif vote[0] == c3:
            cal_c += vote[4]
        elif vote[0] == c4:
            cal_d += vote[4]

    dictionary = {cal_a: 'a', cal_b: 'b', cal_c: 'c', cal_d: 'd'}
    answer = dictionary.get(max(cal_a, cal_b, cal_c, cal_d))
    print("(b) Plurality: winner is", answer, "(", " a:", cal_a, " b:", cal_b, " c:", cal_c, " d:", cal_d, ")")


Plurality('a', 'b', 'c', 'd')


# PluralityRunoff:
def PluralityRunoff(c1, c2, c3, c4):
    sum = 0
    cal_a = cal_b = cal_c = cal_d = 0
    "Check if any candidate get voted more than absolute_majority "
    for vote in votes:
        sum += vote[4]
        if vote[0] == c1:
            cal_a += vote[4]
        elif vote[0] == c2:
            cal_b += vote[4]
        elif vote[0] == c3:
            cal_c += vote[4]
        elif vote[0] == c4:
            cal_d += vote[4]

    absolute_majority = math.ceil(sum / 2)
    dict = {'a': cal_a, 'b': cal_b, 'c': cal_c, 'd': cal_d}

    if cal_a > absolute_majority:
        return 'a'
    elif cal_b > absolute_majority:
        return 'b'
    elif cal_c > absolute_majority:
        return 'c'
    elif cal_d > absolute_majority:
        return 'd'
    else:
        "If no candidate get votes greater than absolute majority, then need to do the second run"
        second_run_candidates = []
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        second_run_candidates.append(dict[0][0])
        second_run_candidates.append(dict[1][0])
        # print("sec round with 2 candidates: ", ans)
        answer = MajorityRule(second_run_candidates[0], second_run_candidates[1])
        print("(c) Plurality: winner is", answer, "(second round candidates are", second_run_candidates, ")")


PluralityRunoff('a', 'b', 'c', 'd')


# BordaVoting: the minimum win
def BordaVoting(c1, c2, c3, c4):
    cal_a = 0
    cal_b = 0
    cal_c = 0
    cal_d = 0
    for vote in votes:
        i = 1
        for v in vote:
            if v == c1:
                cal_a += vote[4] * i
            elif v == c2:
                cal_b += vote[4] * i
            elif v == c3:
                cal_c += vote[4] * i
            elif v == c4:
                cal_d += vote[4] * i
            i += 1
    dictionary = {cal_a: 'a', cal_b: 'b', cal_c: 'c', cal_d: 'd'}
    answer = dictionary.get(min(cal_a, cal_b, cal_c, cal_d))
    print("(d) BordaVoting: winner is", answer, "(", " a:", cal_a, " b:", cal_b, " c:", cal_c, " d:", cal_d, ")")


BordaVoting('a', 'b', 'c', 'd')


def CondorcetVoting(c1, c2, c3, c4):
    candidates = [c1, c2, c3, c4]
    matrix = np.zeros((4, 4))
    sum_of_row = []
    d = {}
    for i in range(len(candidates)):
        if MajorityRule(candidates[i], candidates[0]) == candidates[i]:
            matrix[i][0] = 1
        if MajorityRule(candidates[i], candidates[1]) == candidates[i]:
            matrix[i][1] = 1
        if MajorityRule(candidates[i], candidates[2]) == candidates[i]:
            matrix[i][2] = 1
        if MajorityRule(candidates[i], candidates[3]) == candidates[i]:
            matrix[i][3] = 1
        sum_of_row.append(matrix[i].sum())
    for i in range(len(candidates)):
        d[candidates[i]] = sum_of_row[i]
    answer = max(d.items(), key=operator.itemgetter(1))[0]
    print("(e) CondorcetVoting: winner is", answer, "\n", matrix)


CondorcetVoting('a', 'b', 'c', 'd')
