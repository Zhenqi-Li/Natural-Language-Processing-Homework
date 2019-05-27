import math
import string


def tokenize(sentence):
    return sentence.lower().translate(str.maketrans('','',string.punctuation)).split()[1:]


dictforvac = {}

posf = open("hotelPosT-train.txt", encoding="utf8")
count_total_pos = 0
for line in posf:
    count_total_pos += 1
posf.close()

posf = open("hotelPosT-train.txt", encoding="utf8")
tokens = tokenize(posf.read())
#print(tokens)
dict_pos = {}
for token in tokens:
    token = token.strip()
    if token not in dict_pos.keys():
        dict_pos[token] = 0
        if token not in dictforvac.keys():
            dictforvac[token] = 1
    dict_pos[token] += 1
posf.close()

negf = open("hotelNegT-train.txt", encoding="utf8")
count_total_neg = 0
for line in negf:
    count_total_neg += 1
negf.close()

negf = open("hotelNegT-train.txt", encoding="utf8")
tokens = tokenize(negf.read())
dict_neg = {}
for token in tokens:
    token = token.strip()
    if token not in dict_neg.keys():
        dict_neg[token] = 0
        if token not in dictforvac.keys():
            dictforvac[token] = 1
    dict_neg[token] += 1
negf.close()

final = open("Li-Zhenqi-assgn3-out.txt", "w")
for line in open("HW3-testset.txt", encoding="utf8"):
    ids = line.split()[0]

    ProbofPos = (math.log(float(count_total_pos)/float(count_total_pos + count_total_neg)))
    ProbofNeg = (math.log(float(count_total_neg)/float(count_total_pos + count_total_neg)))

    tokens = tokenize(line)

    for token in tokens:
        pos_sum = sum(dict_pos.values())
        neg_sum = sum(dict_neg.values())
        pos_bottom = math.log(float(pos_sum + len(dictforvac)))
        neg_bottom = math.log(float(neg_sum + len(dictforvac)))
        if token in dict_pos.keys():
            ProbofPos += (math.log(float(dict_pos[token] + 1))/pos_bottom)
        else:
            ProbofPos += (math.log(float(1))/pos_bottom)
        if token in dict_neg.keys():
            ProbofNeg += (math.log(float(dict_neg[token] + 1))/neg_bottom)
        else:
            ProbofNeg += (math.log(float(1))/neg_bottom)
    if ProbofPos > ProbofNeg:
        final.write(ids + "\tPOS\n")
    else:
        final.write(ids + "\tNEG\n")

final.close()