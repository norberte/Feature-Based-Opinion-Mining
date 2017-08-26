from FeatureExtraction import opinion_fetcher as opinion
from FeatureExtraction import process_raw_review_data as process
from FeatureExtraction import pos_tag_reviews as POS_Tagging
from FeatureExtraction import feature_list_extraction as feature
from FeatureExtraction import analyse_processed_data as analysis
import csv

def getColumnValues(fileName, column):
    with open(fileName, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        tempList = list(reader)
    values = []
    for item in tempList:
        values.append(str(item[column]))  ### i-th column of the data set
    return values

def main(reviewDataFile, mainDirectory, listOfProcessedReviews, SWN_FILENAME, featureThreshold):
    # manipulation data to the proper format

    reviewIDs = getColumnValues(fileName=reviewDataFile, column=0)
    reviewName = getColumnValues(fileName=reviewDataFile, column=1)

    outputFile = mainDirectory + 'FeatureExtraction_' + reviewName[0] + '_CustomerReviews.txt'
    with open(outputFile, 'w+') as file_vector:
        if len(reviewIDs) == len(reviewName) == len(listOfProcessedReviews):
            for i in range(0, len(reviewIDs)):
                file_vector.write("product/productId:" + str(reviewIDs[i]) + '\n')
                file_vector.write("product/title:" + str(reviewName[i]) + '\n')
                file_vector.write("review/text: " + str(listOfProcessedReviews[i]) + '\n')

    # processing the data
    process.main(outputFile)

    # POS tagging
    POS_Tagging.main()

    # Feature Extraction
    feature.main(threshold = featureThreshold)

    # Analyze all the Features Extracted
    # analysis.main(SWN_FILENAME) ### no need to execute this, if opinion.main(SWN_FILENAME) is executed

    # Extract opinions from the Analysis Output file
    featureLookUp, featureNames = opinion.main(SWN_FILENAME)
    productName = reviewName[0]

    # Returns:
    # 1. dictionary of list of features contained in a specific review
    # e.g lookUp[i] = list of features contained in review number i
    # 2. name of the product that reviews are about
    return featureLookUp, productName