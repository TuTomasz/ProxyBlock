#  imports
import tensorflow
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow import keras
import pandas as pd
import sys
import os

# Get a prediction based on supplied message and model

def getPrediction(model,message, vectorizer):
  
    # message in vector form
    vector = vectorizer.transform([message]).toarray()

    #binary prediction
    prediction = model.predict_classes(vector)
    
    if prediction == 1:
        
        print("SPAM")

    else:
        print("NOT SPAM")

# Initialize vectorizer to process new messages.

def initVectorizer():
  
    # vector blueprint
    data = pd.read_csv('./ml_model/data/vector_blueprint.csv')
    # get labels
    labels = data["label"]
    # get messages
    messages = data["message"]

    numOfFeatures = 2000

    # initialize vectorizer
    vectorizer = TfidfVectorizer(max_features=numOfFeatures)

    # vectors created from input messages
    vectors = vectorizer.fit_transform(messages).toarray()

    return vectorizer



# minimize tensorflow warning logs
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# initialize vectorizer for making predictions
vectorizer = initVectorizer()

# inport trained model
model = keras.models.load_model('./ml_model/data/spamModel.h5')

# test message
messageInput = sys.argv[1]

getPrediction(model,messageInput,vectorizer)

