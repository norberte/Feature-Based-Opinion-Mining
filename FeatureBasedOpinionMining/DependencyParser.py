import spacy
from nltk import Tree
nlp = spacy.load('en')

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def shortSentence(doc, listOfWords):
    lookUp = {}
    for word in listOfWords:
        temp = []
        for token in doc:
            if token.orth_ != word:
                if token.is_stop != True:
                    if token.is_punct != True:
                        temp.append(token.orth_)
        lookUp[word] = temp
    return lookUp

def getWordDependencyTable_V7(doc):
    dict = {}
    if len(doc) > 10:
        for token in doc:
            if token.is_punct != True:
                temp = []
                if token.head.is_stop != True:              # parent
                    temp.append(token.head.orth_)

                if token.head.head.is_stop != True:         # grandparent
                    temp.append(token.head.head.orth_)

                for uncle in token.head.head.children:      # uncle/aunt
                    if uncle != token.head:
                        if uncle.is_punct != True:
                            if uncle.is_stop != True:
                                temp.append(uncle.orth_)
                            for cousin in uncle.children:  # cousins
                                if cousin.is_stop != True:
                                    if cousin.is_punct != True:
                                        temp.append(cousin.orth_)

                for siblings in token.head.children:        # siblings
                    if siblings != token:
                        if siblings.is_punct != True:
                            if siblings.is_stop != True:
                                temp.append(siblings.orth_)
                            for niece in siblings.children:  # niece/nephew
                                if niece.is_stop != True:
                                    if niece.is_punct != True:
                                        temp.append(niece.orth_)

                for child in token.children:                # children
                    if child.is_punct != True:
                        if child.is_stop != True:
                            temp.append(child.orth_)
                    #if (child.is_punct == True) or (child.is_stop == True) or (child.pos_ == 'DET') or (child.pos_ == 'CCONJ'):
                    #if (child.is_stop == True) or (child.pos_ == 'DET') or (child.pos_ == 'CCONJ'):
                        for grandchild in child.children:   # grandchildren
                            if grandchild.is_punct != True:
                                if grandchild.is_stop != True:
                                    temp.append(grandchild.orth_)
                                for grandgrand in grandchild.children:  # grand-grandchildren
                                    if grandgrand.is_punct != True:
                                        if grandgrand.is_stop != True:
                                            temp.append(grandgrand.orth_)

                if token.orth_ in dict:
                    dict[token.orth_] = unique_list(dict[token.orth_] + temp)
                else:
                    dict[token.orth_] = unique_list(temp)
    else:
        temp = []
        for token in doc:
            temp.append(token.orth_)
        dict = shortSentence(doc, listOfWords= temp)
    return dict


def getWordDependencyTable_V4(doc):
    dict = {}
    if len(doc) > 10:
        for token in doc:
            if token.is_punct != True:
                temp = []
                if token.head.is_stop != True:              # parent
                    temp.append(token.head.orth_)

                if token.head.head.is_stop != True:         # grandparent
                    temp.append(token.head.head.orth_)

                for siblings in token.head.children:        # siblings
                    if siblings != token:
                        if siblings.is_punct != True:
                            if siblings.is_stop != True:
                                temp.append(siblings.orth_)

                for child in token.children:                # children
                    if child.is_punct != True:
                        if child.is_stop != True:
                            temp.append(child.orth_)
                    #if (child.is_punct == True) or (child.is_stop == True) or (child.pos_ == 'DET') or (child.pos_ == 'CCONJ'):
                    #if (child.is_stop == True) or (child.pos_ == 'DET') or (child.pos_ == 'CCONJ'):
                        for grandchild in child.children:   # grandchildren
                            if grandchild.is_punct != True:
                                if grandchild.is_stop != True:
                                    temp.append(grandchild.orth_)

                if token.orth_ in dict:
                    dict[token.orth_] = unique_list(dict[token.orth_] + temp)
                else:
                    dict[token.orth_] = unique_list(temp)
    else:
        temp = []
        for token in doc:
            temp.append(token.orth_)
        dict = shortSentence(doc, listOfWords= temp)
    return dict

def getWordDependencyTable2(doc):
    dep = {}
    for token in doc:
        if token.is_punct != True:
            temp = []
            temp.append(token.head.orth_)   # get parents
            for child in token.children:    # get children
                if child.is_stop != True:
                    if child.is_punct != True:
                        temp.append(child.orth_)
            if token.orth_ in dep:         # join dependency of words showing up more than once
                dep[token.orth_] = unique_list(dep[token.orth_] + temp)
            else:
                dep[token.orth_] = unique_list(temp)
    for token in doc:
        if token.orth_ in dep:
            grandparents_siblings = dep[token.head.orth_]       # get grandparents and siblings
            dep[token.orth_] = unique_list(dep[token.orth_] + grandparents_siblings)
    return dep

'''
sentence = "Staff were extremely helpful, professional and knowledgeable about the area."
doc = nlp(u'' + sentence)
dict = getWordDependencyTable(doc)

print("Dependency Table:")
for key in dict:
    print(key, ": ", dict[key])

print()

for word in doc:
    print(word.text, word.lemma_, word.tag_, word.pos_)

[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
'''