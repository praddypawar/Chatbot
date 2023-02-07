
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
# botname = "pradip"
# model = load_model(f'./{botname}_chatbot_model.h5')
import json
import random

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model,words,classes):##################  words   class
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

new_world = []
def chatbot_response(msg,intents,words,classes,model):  ############ intents 
    ints = predict_class(msg, model,words,classes)
    print("ints: ",ints)

    if ints[0]["intent"] =="confuse":
        new_world.append(msg)

    res = getResponse(ints, intents)

    return [ints[0]["intent"],res]



# def chatbot_response()
# intents = json.loads(open(r'C:\Users\Dell11\Desktop\python\New folder\chatbot\costomer support chatbot\New folder (2)\customer_support.json',encoding="utf-8").read())
# words = pickle.load(open(f'./{botname}_words.pkl','rb'))
# classes = pickle.load(open(f'./{botname}_classes.pkl','rb'))
        


