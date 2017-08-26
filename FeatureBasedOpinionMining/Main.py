import TextProcessor
import WordEmbeddings
import FeatureExtractor
import Linkage
import PhraseLevelOpinionPolarity
import FBOMsystem as FBOM
from WordEmbeddings import unique_list as unique

# global variables
rawReviewFileName = 'C:/Users/Norbert/Desktop/research2017/RawSpeakerReviews.csv'
word2vec_modelPath = 'C:/Users/Norbert/Desktop/GoogleNews-vectors-negative300.bin'
mainDirectory = 'C:/Users/Norbert/Desktop/research2017/'
SWN_FILENAME = 'C:/Users/Norbert/PycharmProjects/FeatureBasedOpinionMining/FeatureExtraction/SentiWordNet_3.0.0_20130122.txt'
featureThreshold = 10
productName = ""

def main_beforeR():
    # text pre-processing for feature extraction and dependency parsing
    softProcessedReviews, softProcessing_corpusPath = TextProcessor.soft_processing(fileName=rawReviewFileName,
                                                                                    colNum=2)

    # text pre-processing for word2vec
    hardProcessedReviews, hardProcessing_corpusPath = TextProcessor.hard_processing(fileName=rawReviewFileName,
                                                                                    colNum=2)

    # feature extraction, feature within review lookUp table building
    featureLookUpTable, productName = FeatureExtractor.main(reviewDataFile=rawReviewFileName,
                                                            mainDirectory=mainDirectory,
                                                            listOfProcessedReviews=softProcessedReviews,
                                                            SWN_FILENAME=SWN_FILENAME,
                                                            featureThreshold=featureThreshold)

    # embeddingsFile contains the 300 dimensional vector representation of every unique word from the corpus
    embeddingsFileDirectory = mainDirectory + productName + "_AllWords"
    WordEmbeddings.getWordEmbeddings(model_path=word2vec_modelPath,
                                                          corpusPath=hardProcessing_corpusPath,
                                                          TSV_filename=embeddingsFileDirectory)

    # fileName returned from csv file containing the linkage word-pair and the 300 dimensional relation vector
    relationLinkageFile = Linkage.main(reviewFeatures_LookUp=featureLookUpTable, corpusPath=softProcessing_corpusPath,
                                       mainDirectory=mainDirectory, productName=productName,
                                       embeddingsFileDirectory=embeddingsFileDirectory)

    print("Analyze the file named " + relationLinkageFile + " with the R script named FeatureDescriptorFiltering.R")
    print("The R script will create the file " + mainDirectory + "opinionFiltering.txt when any model is chosen to be the classifier.")

# work in R: Feature Descriptor Filtering
# input: relationLinkageFile: CSV file containing the linkage word-pairs with their 300 dimensional relation vector
# output: text file names opinionFiltering.txt: containing a list of valid opinion phrases (one opinion phrase/line)


def main_afterR():
    featureList = []
    opinionPhraseFile = mainDirectory + "opinionFiltering.txt"
    listOfPhrases = []
    with open(opinionPhraseFile, "r") as infile:
        for line in infile:
            wordPair = line.strip('\n')
            index = wordPair.find('_')
            featureList.append(wordPair[0:index])
            listOfPhrases.append(wordPair[index + 1:] + " " + wordPair[0:index])

    # get the opinion Polarity of the real feature-descriptors
    opinionPolarityLookUp = PhraseLevelOpinionPolarity.main(listOfPhrases=listOfPhrases)

    uniqueFeatureList = unique(featureList)
    outputFile = mainDirectory + 'Feature Based Opinion Mining System.txt'

    FBOM.main(outputFile, productName, uniqueFeatureList, listOfPhrases, opinionPolarityLookUp)


if __name__ == '__main__':
    main_beforeR()
    # run FeatureDescriptorFiltering.R
    main_afterR()
