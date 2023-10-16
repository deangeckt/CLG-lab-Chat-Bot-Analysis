import numpy as np

map1 = [{'r': 2, 'c': 23}, {'r': 2, 'c': 22}, {'r': 2, 'c': 21}, {'r': 3, 'c': 21}, {'r': 3, 'c': 20}, {'r': 3, 'c': 19}, {'r': 3, 'c': 18}, {'r': 4, 'c': 18}, {'r': 4, 'c': 17}, {'r': 4, 'c': 16}, {'r': 4, 'c': 15}, {'r': 5, 'c': 15}, {'r': 5, 'c': 14}, {'r': 5, 'c': 13}, {'r': 4, 'c': 13}, {'r': 4, 'c': 12}, {'r': 3, 'c': 12}, {'r': 3, 'c': 11}, {'r': 3, 'c': 10}, {'r': 4, 'c': 10}, {'r': 4, 'c': 9}, {'r': 5, 'c': 9}, {'r': 6, 'c': 9}, {'r': 7, 'c': 9}, {'r': 8, 'c': 9}, {'r': 8, 'c': 10}, {'r': 8, 'c': 11}, {'r': 8, 'c': 12}, {'r': 8, 'c': 13}, {'r': 7, 'c': 13}, {'r': 7, 'c': 14}, {'r': 8, 'c': 14}, {'r': 8, 'c': 15}, {'r': 9, 'c': 15}, {'r': 9, 'c': 16}, {'r': 10, 'c': 16}, {'r': 10, 'c': 17}, {'r': 11, 'c': 17}, {'r': 11, 'c': 18}, {'r': 12, 'c': 18}, {'r': 12, 'c': 19}, {'r': 12, 'c': 20}, {'r': 13, 'c': 20}, {'r': 14, 'c': 20}, {'r': 14, 'c': 19}, {'r': 13, 'c': 19}, {'r': 13, 'c': 18}, {'r': 13, 'c': 17}, {'r': 13, 'c': 16}, {'r': 12, 'c': 16}, {'r': 12, 'c': 15}, {'r': 12, 'c': 14}, {'r': 12, 'c': 13}, {'r': 12, 'c': 12}, {'r': 12, 'c': 11}, {'r': 12, 'c': 10}, {'r': 12, 'c': 9}, {'r': 11, 'c': 9}, {'r': 11, 'c': 8}, {'r': 11, 'c': 7}, {'r': 10, 'c': 7}, {'r': 10, 'c': 6}, {'r': 9, 'c': 6}, {'r': 9, 'c': 5}, {'r': 9, 'c': 4}, {'r': 10, 'c': 4}, {'r': 10, 'c': 3}, {'r': 10, 'c': 2}, {'r': 10, 'c': 1}, {'r': 11, 'c': 1}, {'r': 11, 'c': 0}, {'r': 12, 'c': 0}, {'r': 13, 'c': 0}, {'r': 13, 'c': 1}, {'r': 14, 'c': 1}, {'r': 14, 'c': 2}, {'r': 15, 'c': 2}, {'r': 15, 'c': 3}, {'r': 16, 'c': 3}, {'r': 16, 'c': 4}, {'r': 16, 'c': 5}, {'r': 16, 'c': 6}]
map2 = [{'r': 2, 'c': 20}, {'r': 2, 'c': 19}, {'r': 2, 'c': 18}, {'r': 2, 'c': 17}, {'r': 2, 'c': 16}, {'r': 2, 'c': 15}, {'r': 3, 'c': 15}, {'r': 4, 'c': 15}, {'r': 4, 'c': 16}, {'r': 4, 'c': 17}, {'r': 3, 'c': 17}, {'r': 3, 'c': 18}, {'r': 3, 'c': 19}, {'r': 4, 'c': 19}, {'r': 4, 'c': 20}, {'r': 5, 'c': 20}, {'r': 6, 'c': 20}, {'r': 7, 'c': 20}, {'r': 8, 'c': 20}, {'r': 9, 'c': 20}, {'r': 10, 'c': 20}, {'r': 11, 'c': 20}, {'r': 12, 'c': 20}, {'r': 13, 'c': 20}, {'r': 14, 'c': 20}, {'r': 14, 'c': 19}, {'r': 15, 'c': 19}, {'r': 15, 'c': 18}, {'r': 15, 'c': 17}, {'r': 15, 'c': 16}, {'r': 15, 'c': 15}, {'r': 15, 'c': 14}, {'r': 14, 'c': 14}, {'r': 14, 'c': 13}, {'r': 13, 'c': 13}, {'r': 12, 'c': 13}, {'r': 11, 'c': 13}, {'r': 11, 'c': 12}, {'r': 10, 'c': 12}, {'r': 10, 'c': 13}, {'r': 10, 'c': 14}, {'r': 10, 'c': 15}, {'r': 9, 'c': 15}, {'r': 8, 'c': 15}, {'r': 7, 'c': 15}, {'r': 7, 'c': 14}, {'r': 6, 'c': 14}, {'r': 6, 'c': 13}, {'r': 7, 'c': 13}, {'r': 7, 'c': 12}, {'r': 7, 'c': 11}, {'r': 7, 'c': 10}, {'r': 7, 'c': 9}, {'r': 7, 'c': 8}, {'r': 7, 'c': 7}, {'r': 7, 'c': 6}, {'r': 7, 'c': 5}, {'r': 7, 'c': 4}, {'r': 8, 'c': 4}, {'r': 8, 'c': 3}, {'r': 9, 'c': 3}, {'r': 10, 'c': 3}, {'r': 11, 'c': 3}, {'r': 12, 'c': 3}, {'r': 12, 'c': 2}, {'r': 13, 'c': 2}, {'r': 13, 'c': 3}, {'r': 13, 'c': 4}, {'r': 13, 'c': 5}]
map3 = [{'r': 3, 'c': 9}, {'r': 4, 'c': 9}, {'r': 5, 'c': 9}, {'r': 5, 'c': 8}, {'r': 6, 'c': 8}, {'r': 7, 'c': 8}, {'r': 8, 'c': 8}, {'r': 8, 'c': 9}, {'r': 8, 'c': 10}, {'r': 8, 'c': 11}, {'r': 8, 'c': 12}, {'r': 7, 'c': 12}, {'r': 7, 'c': 13}, {'r': 6, 'c': 13}, {'r': 6, 'c': 14}, {'r': 6, 'c': 15}, {'r': 6, 'c': 16}, {'r': 6, 'c': 17}, {'r': 7, 'c': 17}, {'r': 8, 'c': 17}, {'r': 8, 'c': 18}, {'r': 8, 'c': 19}, {'r': 9, 'c': 19}, {'r': 9, 'c': 18}, {'r': 9, 'c': 17}, {'r': 9, 'c': 16}, {'r': 10, 'c': 16}, {'r': 11, 'c': 16}, {'r': 12, 'c': 16}, {'r': 12, 'c': 17}, {'r': 12, 'c': 18}, {'r': 13, 'c': 18}, {'r': 14, 'c': 18}, {'r': 14, 'c': 17}, {'r': 15, 'c': 17}, {'r': 16, 'c': 17}, {'r': 16, 'c': 16}, {'r': 16, 'c': 15}, {'r': 16, 'c': 14}, {'r': 16, 'c': 13}, {'r': 16, 'c': 12}, {'r': 15, 'c': 12}, {'r': 14, 'c': 12}, {'r': 14, 'c': 11}, {'r': 14, 'c': 10}]
map4 = [{'r': 3, 'c': 23}, {'r': 3, 'c': 22}, {'r': 4, 'c': 22}, {'r': 5, 'c': 22}, {'r': 5, 'c': 21}, {'r': 4, 'c': 21}, {'r': 4, 'c': 20}, {'r': 4, 'c': 19}, {'r': 5, 'c': 19}, {'r': 6, 'c': 19}, {'r': 7, 'c': 19}, {'r': 8, 'c': 19}, {'r': 9, 'c': 19}, {'r': 9, 'c': 20}, {'r': 10, 'c': 20}, {'r': 10, 'c': 21}, {'r': 11, 'c': 21}, {'r': 12, 'c': 21}, {'r': 13, 'c': 21}, {'r': 14, 'c': 21}, {'r': 14, 'c': 20}, {'r': 14, 'c': 19}, {'r': 15, 'c': 19}, {'r': 15, 'c': 18}, {'r': 15, 'c': 17}, {'r': 15, 'c': 16}, {'r': 15, 'c': 15}, {'r': 14, 'c': 15}, {'r': 14, 'c': 14}, {'r': 14, 'c': 13}, {'r': 14, 'c': 12}, {'r': 14, 'c': 11}, {'r': 13, 'c': 11}, {'r': 13, 'c': 10}, {'r': 12, 'c': 10}, {'r': 11, 'c': 10}, {'r': 11, 'c': 11}, {'r': 10, 'c': 11}, {'r': 10, 'c': 12}, {'r': 9, 'c': 12}, {'r': 8, 'c': 12}, {'r': 7, 'c': 12}, {'r': 7, 'c': 11}, {'r': 6, 'c': 11}, {'r': 6, 'c': 10}, {'r': 5, 'c': 10}, {'r': 4, 'c': 10}, {'r': 4, 'c': 9}, {'r': 3, 'c': 9}, {'r': 2, 'c': 9}, {'r': 2, 'c': 8}, {'r': 2, 'c': 7}, {'r': 3, 'c': 7}, {'r': 3, 'c': 6}, {'r': 4, 'c': 6}, {'r': 5, 'c': 6}, {'r': 6, 'c': 6}, {'r': 7, 'c': 6}, {'r': 7, 'c': 5}, {'r': 8, 'c': 5}, {'r': 9, 'c': 5}, {'r': 10, 'c': 5}, {'r': 10, 'c': 4}, {'r': 11, 'c': 4}, {'r': 11, 'c': 3}, {'r': 12, 'c': 3}, {'r': 13, 'c': 3}, {'r': 13, 'c': 2}, {'r': 13, 'c': 1}, {'r': 13, 'c': 0}, {'r': 12, 'c': 0}, {'r': 11, 'c': 0}, {'r': 10, 'c': 0}, {'r': 9, 'c': 0}, {'r': 8, 'c': 0}]
map5 = [{'r': 1, 'c': 1}, {'r': 1, 'c': 2}, {'r': 0, 'c': 2}, {'r': 0, 'c': 3}, {'r': 0, 'c': 4}, {'r': 1, 'c': 4}, {'r': 1, 'c': 5}, {'r': 1, 'c': 6}, {'r': 2, 'c': 6}, {'r': 2, 'c': 7}, {'r': 3, 'c': 7}, {'r': 4, 'c': 7}, {'r': 5, 'c': 7}, {'r': 6, 'c': 7}, {'r': 6, 'c': 6}, {'r': 7, 'c': 6}, {'r': 8, 'c': 6}, {'r': 9, 'c': 6}, {'r': 9, 'c': 7}, {'r': 10, 'c': 7}, {'r': 11, 'c': 7}, {'r': 11, 'c': 8}, {'r': 12, 'c': 8}, {'r': 12, 'c': 9}, {'r': 12, 'c': 10}, {'r': 12, 'c': 11}, {'r': 12, 'c': 12}, {'r': 12, 'c': 13}, {'r': 12, 'c': 14}, {'r': 11, 'c': 14}, {'r': 11, 'c': 15}, {'r': 10, 'c': 15}, {'r': 10, 'c': 16}, {'r': 9, 'c': 16}, {'r': 8, 'c': 16}, {'r': 8, 'c': 17}, {'r': 7, 'c': 17}, {'r': 6, 'c': 17}, {'r': 6, 'c': 18}, {'r': 5, 'c': 18}, {'r': 5, 'c': 19}, {'r': 4, 'c': 19}, {'r': 3, 'c': 19}, {'r': 3, 'c': 20}, {'r': 2, 'c': 20}, {'r': 1, 'c': 20}, {'r': 1, 'c': 21}, {'r': 1, 'c': 22}, {'r': 1, 'c': 23}, {'r': 2, 'c': 23}, {'r': 3, 'c': 23}, {'r': 4, 'c': 23}, {'r': 5, 'c': 23}, {'r': 6, 'c': 23}, {'r': 7, 'c': 23}, {'r': 7, 'c': 22}, {'r': 7, 'c': 21}, {'r': 7, 'c': 20}, {'r': 8, 'c': 20}, {'r': 8, 'c': 19}, {'r': 8, 'c': 18}, {'r': 9, 'c': 18}, {'r': 9, 'c': 17}, {'r': 10, 'c': 17}, {'r': 11, 'c': 17}, {'r': 12, 'c': 17}, {'r': 12, 'c': 18}, {'r': 12, 'c': 19}, {'r': 13, 'c': 19}, {'r': 14, 'c': 19}, {'r': 14, 'c': 18}, {'r': 15, 'c': 18}, {'r': 15, 'c': 17}, {'r': 14, 'c': 17}, {'r': 14, 'c': 16}, {'r': 13, 'c': 16}, {'r': 13, 'c': 15}, {'r': 14, 'c': 15}, {'r': 14, 'c': 14}, {'r': 15, 'c': 14}, {'r': 16, 'c': 14}, {'r': 16, 'c': 13}, {'r': 16, 'c': 12}, {'r': 16, 'c': 11}, {'r': 16, 'c': 10}]
map6 = [{'r': 8, 'c': 7}, {'r': 7, 'c': 7}, {'r': 6, 'c': 7}, {'r': 5, 'c': 7}, {'r': 4, 'c': 7}, {'r': 3, 'c': 7}, {'r': 2, 'c': 7}, {'r': 1, 'c': 7}, {'r': 0, 'c': 7}, {'r': 0, 'c': 8}, {'r': 0, 'c': 9}, {'r': 0, 'c': 10}, {'r': 0, 'c': 11}, {'r': 0, 'c': 12}, {'r': 1, 'c': 12}, {'r': 2, 'c': 12}, {'r': 3, 'c': 12}, {'r': 4, 'c': 12}, {'r': 5, 'c': 12}, {'r': 6, 'c': 12}, {'r': 6, 'c': 13}, {'r': 6, 'c': 14}, {'r': 6, 'c': 15}, {'r': 6, 'c': 16}, {'r': 6, 'c': 17}, {'r': 6, 'c': 18}, {'r': 6, 'c': 19}, {'r': 6, 'c': 20}, {'r': 6, 'c': 21}, {'r': 6, 'c': 22}, {'r': 6, 'c': 23}, {'r': 7, 'c': 23}, {'r': 8, 'c': 23}, {'r': 9, 'c': 23}, {'r': 10, 'c': 23}, {'r': 11, 'c': 23}, {'r': 11, 'c': 22}, {'r': 11, 'c': 21}, {'r': 11, 'c': 20}, {'r': 11, 'c': 19}, {'r': 11, 'c': 18}, {'r': 11, 'c': 17}, {'r': 12, 'c': 17}, {'r': 13, 'c': 17}, {'r': 14, 'c': 17}, {'r': 15, 'c': 17}, {'r': 16, 'c': 17}, {'r': 16, 'c': 16}, {'r': 16, 'c': 15}, {'r': 16, 'c': 14}, {'r': 16, 'c': 13}, {'r': 15, 'c': 13}, {'r': 14, 'c': 13}, {'r': 13, 'c': 13}, {'r': 12, 'c': 13}, {'r': 12, 'c': 12}, {'r': 12, 'c': 11}, {'r': 12, 'c': 10}, {'r': 13, 'c': 10}, {'r': 14, 'c': 10}, {'r': 15, 'c': 10}, {'r': 16, 'c': 10}, {'r': 16, 'c': 9}, {'r': 16, 'c': 8}, {'r': 16, 'c': 7}, {'r': 16, 'c': 6}, {'r': 16, 'c': 5}, {'r': 16, 'c': 4}, {'r': 16, 'c': 3}, {'r': 16, 'c': 2}, {'r': 16, 'c': 1}, {'r': 15, 'c': 1}, {'r': 14, 'c': 1}, {'r': 13, 'c': 1}, {'r': 12, 'c': 1}, {'r': 11, 'c': 1}, {'r': 10, 'c': 1}, {'r': 9, 'c': 1}, {'r': 8, 'c': 1}, {'r': 7, 'c': 1}]

gt_maps = [map1, map2, map3, map4, map5, map6]


def tuple_distance(tuple1, tuple2):
    # Calculate the Euclidean distance between two tuples
    return ((tuple1[0] - tuple2[0]) ** 2 + (tuple1[1] - tuple2[1]) ** 2) ** 0.5


def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def levenshtein_distance(map_idx: int, pred: list):

    gt = gt_maps[map_idx]
    path1 = [(g['r'], g['c']) for g in gt]
    path2 = [(p['r'], p['c']) for p in pred]

    m = len(path1)
    n = len(path2)

    # Create a matrix to store the edit distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and column of the matrix
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Calculate the edit distances
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the cost of the current edit operation
            cost = manhattan(path1[i - 1], path2[j - 1])

            # Calculate the minimum edit distance
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # Deletion
                dp[i][j - 1] + 1,  # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )

    # Return the edit distance between the two paths
    return dp[m][n] / len(gt)


if __name__ == '__main__':
    print(levenshtein_distance(0, gt_maps[0]))
    print(levenshtein_distance(0, []))
    print(levenshtein_distance(0, gt_maps[1]))
