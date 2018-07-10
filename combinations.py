from itertools import combinations
import re

comb = combinations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 2)

#print(len(list(comb)))

# for i in list(comb):
    # print(i)

#test = combinations(list(comb), 5)

with open("fileGreedy.txt", "w") as f:
    for s in list(comb):
        print(s)
        f.write(re.sub("([(+,*)])", '', str(s)) + "\n")


print(len(list(comb)))

score = []


# with open("fileGreedy.txt", "r") as f:
#   for line in f:
#     score.append(line.replace("\n", "").split(" "))

