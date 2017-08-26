library(caret)
library(MASS)
library(randomForest)
library(glmnet)
library('e1071')
library(gbm)
library(readr)
library(stringr)

# to be changed for the user's own main directory
mainDirectory = "C:/Users/Norbert/Desktop/FeatureBasedOpinionMining/"

# load in all the models
lassoModel1 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/lasso1.rds"))
lassoModel2 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/lasso2.rds"))

svmModel1 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/svm1.rds"))
svmModel2 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/svm2.rds"))

ldaModel1 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/lda1.rds"))
ldaModel2 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/lda2.rds"))

randomForestModel1 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/randomForest1.rds"))
randomForestModel2 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/randomForest2.rds"))

baggingModel1 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/bagging1.rds"))
baggingModel2 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/bagging2.rds"))

grBoostingModel1 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/grBoosting1.rds"))
grBoostingModel2 <- readRDS(str_c(mainDirectory, "Relation Vector Classification Models/grBoosting2.rds"))


# load in the candidate feature dependency-word relation vectors -------------
RelationVectors <- read_csv(str_c(mainDirectory,"supervisedLinkage_RelationVectors.csv"))
relationVec <- as.data.frame(RelationVectors[,-1])
wordPairs <- RelationVectors[,1]

# run one of the following models
# Lasso---------------------------
pred_Lasso_1 <- predict(lassoModel1, newx= as.matrix(relationVec), s = lassoModel1$lambda, type="class")
indeces <- which(pred_Lasso_1 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

pred_Lasso_2 <- predict(lassoModel2, newx= as.matrix(relationVec), s = lassoModel2$lambda, type="class")
indeces <- which(pred_Lasso_2 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

# SVM-------------
pred_svm_1 <- predict(svmModel1, relationVec)
indeces <- which(pred_svm_1 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

pred_svm_2 <- predict(svmModel2, relationVec)
indeces <- which(pred_svm_2 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

# LDA ----------------
pred_lda_1 <- predict(ldaModel1, newdata = relationVec)
indeces <- which(pred_lda_1 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

pred_lda_2 <- predict(ldaModel2, newdata = relationVec)
indeces <- which(pred_lda_2 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

# Random Forest --------
pred_RF1 <- predict(randomForestModel1, relationVec)
indeces <- which(pred_RF1 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

pred_RF2 <- predict(randomForestModel2, relationVec)
indeces <- which(pred_RF2 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

# Bagging--------------
pred_bag1 <- predict(baggingModel1, relationVec)
indeces <- which(pred_bag1 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

pred_bag2 <- predict(baggingModel2, relationVec)
indeces <- which(pred_bag2 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

# Gradient Boosting -----------
pred_boost1 <- round(predict(grBoostingModel1, relationVec, type= "prob"))[,2]
indeces <- which(pred_boost1 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')

pred_boost2 <- round(predict(grBoostingModel2, relationVec, type= "prob"))[,2]
indeces <- which(pred_boost2 %in% "1")
FDonly <- wordPairs[indeces,]
write(FDonly$feature_dependencyWord, file = str_c(mainDirectory,"opinionFiltering.txt"), sep = '\n')



