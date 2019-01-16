import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.postiveReviewCount = 0
        self.negativeReviewCount = 0 
        self.positiveWordsWithCount = {}
        self.negativeWordsWithCount = {}

    def train(self, lines):
        for line in lines:
            eachFields = line.split('|')
            s = re.sub(r'[^\w\s]','',eachFields[2])
            words = s.rstrip("\n\r").lower()
            if eachFields[0] == '1':
                self.negativeReviewCount += 1
            else:
                self.postiveReviewCount += 1
            for eachWord in words.split():
                if eachFields[0] == '1':
                    self.negativeWordsWithCount = self.calculateCount(eachWord.strip(), self.negativeWordsWithCount)
                else:
                    self.positiveWordsWithCount = self.calculateCount(eachWord.strip(), self.positiveWordsWithCount)

    def classify(self, lines):
        stopwords = self.getStopWords()
        predict = []
        for line in lines:
            words = re.sub(r'[^\w\s]','',line.split('|')[2]).rstrip("\n\r").lower()
            probOfGoodWord = 0.0
            probOfBadWord= 0.0
            for eachWord in words.split():
                eachWord = eachWord.strip()
                if eachWord not in stopwords:
                    probOfGoodWord += self.calculateProbaility(eachWord, self.postiveReviewCount, self.positiveWordsWithCount)                    
                    probOfBadWord += self.calculateProbaility(eachWord, self.negativeReviewCount, self.negativeWordsWithCount)	
            if probOfGoodWord < probOfBadWord:
                predict.append('1')
            else:
                predict.append('5')
        return predict
    
    def getStopWords(self):
        stopwords = []
        for each in self.negativeWordsWithCount:
            if each in self.positiveWordsWithCount and self.positiveWordsWithCount[each]/(self.negativeWordsWithCount[each]*self.postiveReviewCount/self.negativeReviewCount)<=1.6 and self.positiveWordsWithCount[each]/(self.negativeWordsWithCount[each]*self.postiveReviewCount/self.negativeReviewCount)>=0.72: 
                stopwords.append(each)
        return stopwords

    def calculateCount(self, word, wordCountDic):
        if word in wordCountDic:
            wordCountDic[word] += 1
        else:
            wordCountDic[word] = 1
        return wordCountDic
    
    def calculateProbaility(self, eachWord, reviewsCount, words):
        if eachWord in words:
            return math.log(float(words[eachWord]+1)/float(reviewsCount + len(words)))
        else:
            return math.log(1/float(reviewsCount + len(words)))