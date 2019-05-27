from collections import Counter

def unigram(filename):
    text = open(filename).read()
    words = text.split()
    freqs = Counter(words)
    freqs["<unk>"] = 0
    for key in freqs.keys():
        if freqs[key] == 1:
            freqs["<unk>"] = freqs["<unk>"]+1
    return freqs
freqs = unigram("berp-training.txt")
def uniprob(word):
    return freqs[word]/sum(freqs.values())
def unigramModel(sentence):
    p = 1
    words = sentence.split()
    for word in words:
        if freqs[word] == 1 or (word not in freqs.keys()):
            p = p*uniprob("<unk>")
        else:
            p = p*uniprob(word)
    return p


def bigramfreq(filename):
    text = open(filename).read()
    words = text.split()
    freqs = Counter(words)
    freqs["<unk>"] = 0
    for key in freqs.keys():
        if freqs[key] < 2:
            freqs["<unk>"] = freqs["<unk>"]+1
    return freqs
bifreqs = bigramfreq("berp-training.txt")
def bigram(filename):
    biwords = []
    text = open(filename, 'r')
    for line in text.readlines():
        words = line.split()
        length = len(words)
        for i in range(length-1):
            if bifreqs[words[i]] < 2 and bifreqs[words[i+1]] <2:
                biwords.append("<unk>" + " " + "<unk>")
            elif bifreqs[words[i]] >= 2 and bifreqs[words[i+1]] <2:
                biwords.append(words[i] + " " + "<unk>")
            elif bifreqs[words[i]] < 2 and bifreqs[words[i + 1]] >= 2:
                biwords.append("<unk>" + " " + words[i+1])
            else:
                biwords.append(words[i] + " " + words[i + 1])
    finalbifreq = Counter(biwords)
    return finalbifreq
finalbifreq = bigram("berp-training.txt")
def smoothbiprob(words):
    vac = len(bifreqs)
    word = words.split()
    y = (freqs[word[0]]+vac) / sum(freqs.values())
    x = (finalbifreq[words]+1) / sum(finalbifreq.values())
    #return (finalbifreq[words]+1)/(freqs[word[0]]+ vac)
    return x/y
def bigramModel(sentence):
    p = 1
    words = sentence.split()
    for i in range(len(words)-1):
        testbiword = words[i] + " " + words[i+1]
        if testbiword not in finalbifreq:
            p = p * smoothbiprob("<unk>" + " " + "<unk>")
        else:
            p = p * smoothbiprob(testbiword)
    return p



N = sum(finalbifreq.values())

biprodic = {}
for key in finalbifreq.keys():
    biprodic[key] = finalbifreq[key]/N

import numpy as np
def findone(start):
    biword = []
    bins = []
    for key in biprodic.keys():
        words = key.split()
        if words[0] == start:
            biword.append(words[1])
            bins.append(biprodic[key])
    probbin = []
    for i in bins:
        probbin.append(i/sum(bins))
    return np.random.choice(biword, 1, p=probbin)

def findsentence():
    start = "<s>"
    end = "</s>"
    sentence = "<s>"
    x = findone(start)[0]
    while x != "</s>":
        sentence = sentence + " " + x
        x = findone(x)[0]
    sentence = sentence+" "+"</s>"
    return sentence

def main():
    file = open("berp-100-test.txt", 'r')
    fileuni = open("Li-Zhenqi-assgn2-unigram-out.txt", 'a')
    filebi = open("Li-Zhenqi-assgn2-bigram-out.txt", 'a')
    filesentence = open("Li-Zhenqi-assgn2-bigram-rand-corpus.txt", 'a')
    for line in file.readlines():
        fileuni.write(str(unigramModel(line))+'\n')
        filebi.write(str(bigramModel(line))+'\n')
    for i in range(100):
        filesentence.write(findsentence()+'\n')
main()


