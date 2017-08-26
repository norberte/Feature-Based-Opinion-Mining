from textblob import TextBlob

def main(listOfPhrases):
    opinionPolarity = {}
    for wordPair in listOfPhrases:
        blob = TextBlob(wordPair)
        sentimentValue = blob.sentiment.polarity
        if sentimentValue >= 0.2:
            opinionPolarity[wordPair] = "positive"
        elif sentimentValue < 0.2 and sentimentValue > -0.2:
            opinionPolarity[wordPair] = "neutral"
        elif sentimentValue <= -0.2:
            opinionPolarity[wordPair] = "negative"
    return opinionPolarity
