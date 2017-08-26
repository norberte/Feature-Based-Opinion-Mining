import numpy as np
import spacy
import pandas as pd
nlp = spacy.load('en')
from RelationVectorConnector import connectionVec, angle_between, cosine_distance, euclidean_distance
from DependencyParser import getWordDependencyTable_V4, unique_list

def buildReviewLookUp(corpusFile):
    lookUp = {}
    lineNum = 0
    with open(corpusFile, "r") as corpus:
        for lineNum, review in enumerate(corpus):
            lookUp[lineNum + 1] = review.strip('\n')
    return (lineNum + 1), lookUp  # offset of 1, because lineNum starts at 0, while the first line is review 1

def main(reviewFeatures_LookUp, corpusPath, mainDirectory, productName, embeddingsFileDirectory):
    wordListFile = embeddingsFileDirectory +  '_metadata.tsv'
    wordVectorFile = embeddingsFileDirectory + '_embeddings.csv'

    # import all the word embeddings as a NumPy array
    wordEmbeddings = np.genfromtxt(wordVectorFile, delimiter=",")

    # import all the words in the corpus
    wordList = []
    with open(wordListFile, "r") as infile:
        for line in infile:
            wordList.append(line.strip('\n'))

    # create word-vector lookUp dictionary
    vectorLookUp = {}
    for i in range(0, len(wordList)):
        vectorLookUp[wordList[i]] = wordEmbeddings[i]

    # build lookUp table for getting text contained in review i:
    # e.g. lookUp[1] would return the text as a string from the first review in the review Data file
    numberOfReviews, reviewLookUpTable = buildReviewLookUp(corpusFile = corpusPath)

    # estimating number of linkages
    relationVectors = np.zeros(shape=(numberOfReviews * 5, 300))
    wordPair = []

    index = 0
    listOfSentences = []
    linkage_sentence_lookUp = {}

    # semi-supervised feature - someWord Linkage
    for i in range(1, numberOfReviews + 1):
        try:
            featureList = reviewFeatures_LookUp[i]
        except:
            continue
        review = reviewLookUpTable[i]
        doc = nlp(u'' + review)
        for sent in doc.sents:
            linkageList = []
            listOfSentences.append(str(sent))
            wordDependencyTable = getWordDependencyTable_V4(sent)
            for feature in featureList:
                try:
                    reviewWords = wordDependencyTable[feature]
                except:
                    continue
                try:
                    fVec = vectorLookUp[feature]  # bigram vector not found ... KeyError
                except:
                    print("Something wrong with feature vector of: " , feature, '\n')
                    continue

                print(feature, ": ", reviewWords, '\n')
                for word in reviewWords:
                    if word != feature:
                        try:
                            vec_i = vectorLookUp[word]
                            relationVectors[index] = connectionVec(fVec, vec_i)
                            wordPair.append(str(feature + '_' + word))
                            linkageList.append(str(feature + '_' + word))
                            index += 1
                        except:
                            print("No vector available for :" + word)
                linkage_sentence_lookUp[sent] = linkageList

    outputFile = mainDirectory + productName + '_supervised_V4_listOfSentences.txt'
    with open(outputFile, 'w+') as file:
        for sentence in listOfSentences:
            file.write(sentence + '\n')

    header_str = ""
    for k in range(0, 300):
        if k == 299:
            header_str = header_str + 'dim' + str(k + 1) + '\n'
        else:
            header_str = header_str + 'dim' + str(k + 1) + ','

    relationVecLinkagesFile = mainDirectory + productName + '_supervised_V4_RelationVectors.csv'
    with open(relationVecLinkagesFile, 'w+') as file_vector:
        file_vector.write("feature_dependencyWord," + header_str)
        for i in range(0, len(wordPair)):
            tempStr = ""
            for j in range(0,300):
                if j == 299:
                    tempStr = tempStr + str(relationVectors[i][j]) + '\n'
                else:
                    tempStr = tempStr + str(relationVectors[i][j]) + ","
            file_vector.write(wordPair[i] + ',' +  tempStr)
    return relationVecLinkagesFile