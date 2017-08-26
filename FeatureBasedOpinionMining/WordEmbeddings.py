import logging
import sys
import gensim
import spacy

nlp = spacy.load('en')

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.setLevel(level=logging.INFO)
logger.info("running %s", ' '.join(sys.argv))

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def word2vec2tensor(word2vec_model, myListOfWords, tensor_filename):
    '''
    Convert Word2Vec mode to 2D tensor TSV file and metadata file
    Args:
        param1 (gensim.models): word2vec model
        param2 (list): words to put inside the model
        param3 (str): filename prefix
    '''
    outfiletsv = tensor_filename + '_tensor.tsv'
    outfiletsvmeta = tensor_filename + '_metadata.tsv'
    outfileEmbeddings = tensor_filename + '_embeddings.csv'

    logger.info("Running word embedding to TSV process")

    with open(outfiletsv, 'w+') as file_vector:
        with open(outfiletsvmeta, 'w+') as file_metadata:
            with open(outfileEmbeddings, 'w+') as file_embeddings:
                for word in myListOfWords:
                    try:
                        vector = word2vec_model[word]
                        vector_row = '\t'.join(map(str, vector))
                        file_metadata.write(word + '\n')
                        file_vector.write(vector_row + '\n')
                        file_embeddings.write(','.join(map(str, vector)) + '\n')
                    except:
                         print("No vector for the word: ",word)

    print()
    logger.info("2D tensor file saved to %s" % outfiletsv)
    logger.info("Tensor metadata file saved to %s" % outfiletsvmeta)
    logger.info("Word embedding file saved to %s" % outfileEmbeddings)
    return outfileEmbeddings

def corpus2ListOfWords(corpusPath):
    wordList = []
    with open(corpusPath, "r") as infile:
        for line in infile:
            doc = nlp(u'' + line.strip('\n'))
            for token in doc:
                if token.is_punct != True and token.is_stop != True:
                    wordList.append(token.orth_)
    return wordList


def getWordEmbeddings(model_path, corpusPath, TSV_filename):
    # load in word2vec model
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)

    # import all the words in the corpus
    wordList = unique_list(corpus2ListOfWords(corpusPath))

    logger.info("Corpus Words Model look-up")
    embeddingsFilePath = word2vec2tensor(word2vec_model=model, myListOfWords=wordList, tensor_filename=TSV_filename)
    logger.info("Corpus Words Vectors finished running...")
    return embeddingsFilePath

if __name__ == "__main__":
    model_path = 'C:/Users/Norbert/Desktop/GoogleNews-vectors-negative300.bin'
    TSV_filename = 'C:/Users/Norbert/Desktop/research2017/computer_AllWords'
    corpusPath = 'C:/Users/Norbert/Desktop/research2017/computer_cleanWords.txt'

    embeddings = getWordEmbeddings(model_path, corpusPath, TSV_filename)