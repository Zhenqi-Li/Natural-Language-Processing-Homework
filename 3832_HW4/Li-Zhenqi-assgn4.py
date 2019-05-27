from __future__ import print_function
from seqlearn.datasets import load_conll
from seqlearn.perceptron import StructuredPerceptron


def features(sentence, i):
    word = sentence[i]

    yield "word:{}" + word.lower()

    if word[0].isupper():
        yield "CAP"

    if i > 0:
        yield "word-1:{}" + sentence[i - 1].lower()
        if i > 1:
            yield "word-2:{}" + str(len(sentence[i - 2].lower()))
            if i > 2:
                yield "word-3:{}" + sentence[i - 3].lower()
    if i + 1 < len(sentence):
        yield "word+1:{}" + sentence[i + 1].lower()
        if i + 2 < len(sentence):
            yield "word+2:{}" + str(len(sentence[i + 2].lower()))
            if i+3 < len(sentence):
                yield "word+3:{}" + sentence[i + 3].lower()
    '''
    word = sentence[i]

    token = nltk.word_tokenize(word)
    yield "word:{}" + nltk.pos_tag(token)[0][1]
    
    if i > 0:
        token = nltk.word_tokenize(sentence[i - 1])
        yield "word-1:{}" + nltk.pos_tag(token)[0][1]
        if i > 1:
            token = nltk.word_tokenize(sentence[i - 2])
            yield "word-2:{}" + nltk.pos_tag(token)[0][1]
    if i + 1 < len(sentence):
        token = nltk.word_tokenize(sentence[i + 1])
        yield "word+1:{}" + nltk.pos_tag(token)[0][1]
        if i + 2 < len(sentence):
            token = nltk.word_tokenize(sentence[i + 2])
            yield "word+2:{}" + nltk.pos_tag(token)[0][1]
    '''
def describe(X, lengths):
    print("{0} sequences, {1} tokens.".format(len(lengths), X.shape[0]))

def load_data():
    f = open('input_train.txt', 'w')
    for line in open('gene-trainF18.txt', 'r'):
        if line == '\n':
            f.write('\n')
        else:
            token_tag = line.split('\t')
            if len(token_tag) >= 3:
                f.write(token_tag[1] + '\t' + token_tag[2])

    f.close()

    f = open('input_test.txt', 'w')
    for line in open('F18-assgn4-test.txt', 'r'):
        if line == '\n':
            f.write('\n')
        else:
            token_tag = line.split('\t')
            if len(token_tag) >= 2:
                f.write(token_tag[1][:-1]+'\t'+'O'+'\n')
    '''
    f = open('input_keys.txt', 'w')
    for line in open('test-run-test-with-keys.txt', 'r'):
        if line == '\n':
            f.write('\n')
        else:
            token_tag = line.split('\t')
            if len(token_tag) >= 3:
                f.write(token_tag[1] + '\t' + token_tag[2])
    '''
if __name__ == "__main__":
    print(__doc__)
    load_data()
    print("Loading training data...", end=" ")
    X_train, y_train, lengths_train = load_conll('input_train.txt', features)
    describe(X_train, lengths_train)


    print("Loading test data...", end=" ")
    X_test, y_test, lengths_test = load_conll('input_test.txt', features)
    describe(X_test, lengths_test)

    clf = StructuredPerceptron(verbose=True, lr_exponent=0.1, max_iter=30)
    print("Training %s" % clf)
    clf.fit(X_train, y_train, lengths_train)

    y_pred = clf.predict(X_test, lengths_test)
    '''
    f = open('input_test_key.txt', 'w')
    for i in y_pred:
        f.write(str(i))
    '''
    f = open('Li-Zhenqi-assgn4-output.txt', 'w')
    i=0
    for line in open('F18-assgn4-test.txt', 'r'):
        if line == '\n':
            f.write('\n')
        else:
            token_tag = line.split('\t')
            if len(token_tag) >= 2:
                f.write(token_tag[0]+ '\t' + token_tag[1][:-1]+ ' \t' + y_pred[i] + '\n')
                i = i+1