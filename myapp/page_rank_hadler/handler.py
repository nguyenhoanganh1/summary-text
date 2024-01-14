import math
import numpy as np


def sentence_count(sentence1, sentence2, stopWords=None, stopNum=0):
    words1 = sentence1.text.lower().split()
    words2 = sentence2.text.lower().split()

    common_words = set(words1) & set(words2)

    if stopWords:
        common_words = [word for word in common_words if word not in stopWords]

    print(f"Từ = {common_words} - Số lần trùng = {max(len(common_words) - stopNum, 0)}")
    return max(len(common_words) - stopNum, 0)


def get_score_page_rank(matrix, d=0.85, max_iter=100, tolarance=1e-8):
    print(f"Tổng số node = {len(matrix)}")
    num_nodes = len(matrix)
    scores = np.ones(num_nodes) / num_nodes
    shadow_score_matrix = [0.0 for _ in range(num_nodes)]
    denominator = get_num_exists_word(matrix, num_nodes)
    # print(f"num_nodes = {num_nodes}, scores = {scores}, shadow_score_matrix = {shadow_score_matrix}, denominator = {denominator}")

    count = 0
    while different_score_matrix(scores, shadow_score_matrix, tolarance):
        for i in range(num_nodes):
            shadow_score_matrix[i] = scores[i]
            # print(f"num_nodes = {num_nodes}, scores = {scores}, shadow_score_matrix = {shadow_score_matrix}, denominator = {denominator}")

        for i in range(num_nodes):
            scores[i] = calculate_score(matrix, num_nodes, denominator, d, i)
            # print(f"num_nodes = {num_nodes}, scores = {scores}, shadow_score_matrix = {shadow_score_matrix}, denominator = {denominator}")
        count += 1
        if count > max_iter:
            break
    return scores


def different_score_matrix(scores, old_scores, tolarance):
    flag = False
    for i in range(len(scores)):
        if math.fabs(scores[i] - old_scores[i]) >= tolarance:
            flag = True
            break
    return flag


def get_num_exists_word(matrix, num_nodes):
    denominator = [0.0 for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            denominator[i] += matrix[i][j]
        if denominator[i] == 0:
            denominator[i] = 1.0
    return denominator


def calculate_score(maxtrix, num_nodes, denominator, d, i):
    deg = 0.0
    for j in range(num_nodes):
        fraction = maxtrix[j][i] * 1.0
        deg += fraction / denominator[j]
        # print(f"deg += fraction / denominator[{j}], {deg} += {fraction} / {denominator[j]}")

    # print(f"(1 - d) + d * deg, ({1} - {d}) + {d} * {deg} score = {score}")
    return (1 - d) + d * deg
