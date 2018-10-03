from itertools import combinations
import re



x1 = 8
x2 = 4

comb = combinations([0, 1, 2, 3, 4, 5, 6, 7], x2)

#print(len(list(comb)))

# for i in list(comb):
    # print(i)

#test = combinations(list(comb), 5)

with open('seeds/' + str(x1) + '_' + str(x2) +"_seeds.txt", "w") as f:
    for s in list(comb):
        print(s)
        f.write(re.sub("([(+,*)])", '', str(s)) + "\n")


print(len(list(comb)))

score = []


# with open("fileGreedy.txt", "r") as f:
#   for line in f:
#     score.append(line.replace("\n", "").split(" "))

