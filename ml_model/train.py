# main imports
import tensorflow
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from tensorflow import keras

# helper libraries
import copy 
import io
import os
import numpy as np
import pandas as pd

# Hide tensorflow warnings
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# read data from dataset
data = pd.read_csv('data/spam-utf-8.csv')

# drop unused columns
data = data.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)

# rename columns labals and sms
data = data.rename(columns={"v1":'label', "v2":'message'})

# transform labels into binary format 
tags = {'spam': 1,'ham': 0}

data.label = [tags[item] for item in data.label]

# set labels
labels = data["label"]

# set messages
messages = data["message"]

# adjust number of features
numOfFeatures = 2000

# initialize vectorizer
vectorizer = TfidfVectorizer(max_features=numOfFeatures)

# vectors created from input messages
vectors = vectorizer.fit_transform(messages).toarray()

# Split training data set random states and test size.
X_train,X_test,Y_train,Y_test = train_test_split(vectors,labels,random_state=30,test_size=0.4)


# Keras model
model = keras.models.Sequential()

model.add(keras.layers.Dense(500,activation='sigmoid',input_shape=(numOfFeatures,)))
model.add(keras.layers.Dropout(0.2, input_shape=(numOfFeatures,)))
model.add(keras.layers.Dense(250,activation='sigmoid'))
model.add(keras.layers.Dropout(0.2, input_shape=(numOfFeatures,)))
model.add(keras.layers.Dense(1,activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

# Set model parameters and train
model.fit(X_train,Y_train,epochs=20,batch_size=50,validation_split=0.3)

# Test model performance on test data
model.evaluate(X_test,Y_test)

# save trained model to file
model.save('data/spamModel.h5')



def testNN_Model(model,message):

  """
  Description: Test trained model with test messages
  :return String Spam or Not Spam
  """
  
  # vectorize message string
  vector = vectorizer.transform([message]).toarray()
  
  # make a prediction
  prediction = model.predict_classes(vector)
  
  #display result
  if prediction == 1:
    
    print("SPAM")
    
  else:
    
    print("NOT SPAM")





