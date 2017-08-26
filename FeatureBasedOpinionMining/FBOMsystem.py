def main(outputFile, productName, uniqueFeatureList, listOfPhrases, opinionPolarityLookUp):
    with open(outputFile, 'w+') as file:
        file.write("Product Name:" + productName + '\n')
        for feature in uniqueFeatureList:
            file.write("\tFeature: " + feature + '\n')
            positive = []
            negative = []
            neutral = []
            for opinionPhrase in listOfPhrases:
                if feature in opinionPhrase:
                    polarity = opinionPolarityLookUp[opinionPhrase]
                    if polarity == "positive":
                        positive.append(opinionPhrase)
                    elif polarity == "neutral":
                        neutral.append(opinionPhrase)
                    elif polarity == "negative":
                        negative.append(opinionPhrase)
            if len(positive) > 0:
                file.write("\t\tPositive opinions: " + '\n')
                for opinion in positive:
                    file.write("\t\t\t" + opinion + '\n')

            if len(neutral) > 0:
                file.write("\t\tNeutral opinions: " + '\n')
                for opinion in neutral:
                    file.write("\t\t\t" + opinion + '\n')

            if len(negative) > 0:
                file.write("\t\tNegative opinions: " + '\n')
                for opinion in negative:
                    file.write("\t\t\t" + opinion + '\n')

            file.write('\n')