import csv
from gensim import parsing
import gensim.models as phraseModel
import re, nltk
from autocorrect import spell
from nltk.corpus import stopwords
import string

# A custom stoplist
STOPLIST = list(stopwords.words('english') + ["n't", "'s", "'m", "ca", "'ve", "'ll", "'d"])
# Uppercase stop-word list
STOPS = list(' '.join(str(e).title() for e in STOPLIST))
# List of symbols we don't care about
symbols = ["-----", "---", "...", "“", "”", '-LRB-', '-RRB-', '_-', '-', '_',  '!!!', '``', '\/', '\*']
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-----", "---", "...", "“", "”", '-LRB-', '-RRB-', '_-', '-', '_',  '!!!', '``', '\/', '\*']
# list of punctuations
punctuation = [',', ';', '.', ':', '?', '!', "'", '"', '...', "''", '-', '`', '``', '(', ')']
# twitter @mentions
mentionFinder = re.compile(r"@[a-z0-9_]{1,15}", re.IGNORECASE)

# function that return a specific column of a CSV file as a list
def importColumnFromCSV(filePath, colNum):
    col = []
    #Process CSV file using csv module
    with open(filePath, "r") as infile:
        csvfile = csv.reader(infile, delimiter=',', quotechar='"')
        for row in csvfile:
            try:
                col.append(row[colNum])
            except:
                print("Column number ", str(colNum), " does not exist in the file ", filePath)
    return col

# function that removes numbers, whitespaces, tags, newlines and html symbols
def whiteSpaceAndNumericRemoval(text):
    cleanedText = parsing.preprocessing.strip_multiple_whitespaces(text)
    cleanedText = parsing.preprocessing.strip_numeric(cleanedText)
    cleanedText = parsing.preprocessing.strip_tags(cleanedText)

    # get rid of newlines
    cleanedText = cleanedText.strip().replace("\n", " ").replace("\r", " ")

    # replace twitter @mentions
    # text = mentionFinder.sub("@MENTION", cleanedText)

    # replace HTML symbols
    cleanedText = cleanedText.replace("&amp;", "and").replace("&gt;", ">").replace("&lt;", "<")
    return cleanedText

# function that detects phrases using bigrams and trigrams
def phraseFinder(text, bigram, trigram):
    trigrams = trigram[bigram[list(text.split())]]
    trigrams_str = ' '.join(str(x) for x in trigrams)
    return trigrams_str

# function that filters out symbols, punctuation and stopwords
def filter(listOfWords):
    punctuation_filtering = [w for w in listOfWords if not w in punctuation]
    symbols_filtered = [w for w in punctuation_filtering if not w in SYMBOLS]
    filtered_words = [w for w in symbols_filtered if not w in STOPLIST]
    double_filtered_words = [w for w in filtered_words if not w in STOPS]
    return double_filtered_words

# function for more drastic text processing
def hard_processing(fileName, colNum):
    # import reviews
    documents = importColumnFromCSV(fileName, colNum)

    # tokenization and review token cleaning
    cleanReviews = []
    for review in documents:
        tokens = nltk.word_tokenize(whiteSpaceAndNumericRemoval(review))
        stopWordAndPunctuationRemoved = filter(tokens)
        spellCheckedTokens = []
        # spellchecking with auto-correct
        for token in stopWordAndPunctuationRemoved:
            spellCheckedTokens.append(str(token))
        cleanReviews.append(spellCheckedTokens)

    # phrase detection model training
    bigramModel = phraseModel.Phrases(cleanReviews)
    trigramModel = phraseModel.Phrases(bigramModel[cleanReviews])

    # process all documents
    results = []
    listOfLetters = list(fileName)
    index = len(listOfLetters) - 1 - listOfLetters[::-1].index('/')
    corpusPath = fileName[0:index] + "/Corpus_HardProcessing.txt"
    with open(corpusPath, 'w') as f:
        f.truncate()
        for review in cleanReviews:
            review_str = ' '.join(str(x) for x in review)
            text = phraseFinder(review_str, bigramModel, trigramModel)
            f.write(text + '\n')
            results.append(text)
    return results, corpusPath

# function for easier text processing
def soft_processing(fileName, colNum):
    # import reviews
    documents = importColumnFromCSV(fileName, colNum)

    # tokenization and review token cleaning
    cleanReviews = []
    reviewWordsOnly = []
    for review in documents:
        tokens = nltk.word_tokenize(whiteSpaceAndNumericRemoval(review))
        symbolFiltered_tokens = [w for w in tokens if not w in symbols]
        spellCheckedTokens = []
        noPunctuationWords = []
        # spellchecking with auto-correct
        for token in symbolFiltered_tokens:
            if token not in punctuation:
                temp = str(spell(token))
                noPunctuationWords.append(temp)
                spellCheckedTokens.append(temp)
            else:
                spellCheckedTokens.append(str(token))   # punctuation
        reviewWordsOnly.append(noPunctuationWords)
        cleanReviews.append(spellCheckedTokens)

    # phrase detection model training
    # bigramModel = phraseModel.Phrases(reviewWordsOnly)
    # trigramModel = phraseModel.Phrases(bigramModel[reviewWordsOnly])

    # process all documents
    results = []
    listOfLetters = list(fileName)
    index = len(listOfLetters) - 1 - listOfLetters[::-1].index('/')
    corpusPath = fileName[0:index] + "/Corpus_SoftProcessing.txt"
    with open(corpusPath, 'w') as f:
        f.truncate()
        for review in cleanReviews:
            review_str = ' '.join(str(x) for x in review)
            #text = phraseFinder(review_str, bigramModel, trigramModel)
            f.write(review_str + '\n')
            results.append(review_str)
    return results, corpusPath


if __name__ == "__main__":
    fileName = 'C:/Users/Norbert/Desktop/research2017/RawSpeakerReviews.csv'

    soft_processing(fileName = fileName, colNum = 2)
    hard_processing(fileName = fileName, colNum = 2)