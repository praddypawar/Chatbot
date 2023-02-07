from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from appclient.models import ClientRegistration,ChatbotRegister
import json
from . import generator
from . import chatingbot
#--------------------
import nltk
# nltk.download('punkt')  ##optional
# nltk.download('wordnet')  ##optional
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
from keras.models import load_model
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import string
#--------------------
# Create your views here.
def index(request):
    if "email" not in request.session and "type" not in request.session and "id" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "client":
        messages.error(request, "User not allow")
        return redirect("sign-in")

    client_data = ClientRegistration.objects.get(pk=request.session["id"])

    context = {
        "footer": {"url": "https://colorlib.com", 
        "name": "cloud4code", 
        "year": datetime.now().year, 
        "extra_name": "chatbot"},
        "client_data":client_data,
        "title":"Client-Dashboard"
        }
    return render(request, "client_temp/index.html", context)


def bot_builder(request):  # sourcery skip: low-code-quality
    if "email" not in request.session and "type" not in request.session and "id" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "client":
        messages.error(request, "User not allow")
        return redirect("sign-in")
    # D:\Chatbot\CHATBOT\clientdb\demo.json
    _register_data = ClientRegistration.objects.get(pk=request.session["id"])
    with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","r") as rdata:
        data = json.load(rdata)
    # print(data)
    if request.method == "POST":
        try:

            if "all_data_submit" in request.POST:
                urlObject = request.get_host()
                botname= request.POST.get("botname")
                bottype= request.POST.get("bottype")
                botlogo= request.FILES.get("botlogo")
                bottype = bottype.replace(" ", "_")
                _chatbotregister = ChatbotRegister(client_id=_register_data,chatbot_name=botname,category=bottype,logo=botlogo)
                _chatbotregister.save()

                print("---------------client",botname,bottype,botlogo)

                print("_chatbotregister.pk:",_chatbotregister.pk)
                _chatbotregister.url_link  = "http://"+urlObject +"/client-app/chat-bot-" +generator.encrypt(_register_data.pk) +"-"+ generator.encrypt(_chatbotregister.pk)+"/"#for urls generates
                _chatbotregister.save()

                words=[]
                classes = []
                documents = []
                ignore_words = ['?', '!']

                with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","r") as rd:
                    intents = json.load(rd)
                # intents = json.loads(data_file)
                ###end ------------------------------------------------------------
                for intent in intents['intents']:
                    for pattern in intent['patterns']:

                        # take each word and tokenize it
                        w = nltk.word_tokenize(pattern)
                        words.extend(w)
                        # adding documents
                        documents.append((w, intent['tag']))

                        # adding classes to our class list
                        if intent['tag'] not in classes:
                            classes.append(intent['tag'])

                words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
                words = sorted(list(set(words)))

                classes = sorted(list(set(classes)))

                print (len(documents), "documents")

                print (len(classes), "classes", classes)

                print (len(words), "unique lemmatized words", words)
                os.makedirs(f"./clientdb/{_register_data.fname}_{_register_data.pk}", exist_ok=True)

                pickle.dump(words,open(f'./clientdb/{_register_data.fname}_{_register_data.pk}/{_chatbotregister.chatbot_name}-{_chatbotregister.pk}_words.pkl','wb'))
                pickle.dump(classes,open(f'./clientdb/{_register_data.fname}_{_register_data.pk}/{_chatbotregister.chatbot_name}-{_chatbotregister.pk}_classes.pkl','wb'))
                
                with open(f"./clientdb/{_register_data.fname}_{_register_data.pk}/{_chatbotregister.chatbot_name}-{_chatbotregister.pk}_{bottype}.json","w") as wd:
                    json.dump(intents,wd,indent=4)

                # initializing training data
                training = []
                output_empty = [0] * len(classes)
                for doc in documents:
                    # initializing bag of words
                    bag = []
                    # list of tokenized words for the pattern
                    pattern_words = doc[0]
                    # lemmatize each word - create base word, in attempt to represent related words
                    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
                    # create our bag of words array with 1, if word match found in current pattern
                    for w in words:
                        bag.append(1) if w in pattern_words else bag.append(0)

                    # output is a '0' for each tag and '1' for current tag (for each pattern)
                    output_row = list(output_empty)
                    output_row[classes.index(doc[1])] = 1

                    training.append([bag, output_row])
                # shuffle our features and turn into np.array
                random.shuffle(training)
                training = np.array(training)
                # create train and test lists. X - patterns, Y - intents
                train_x = list(training[:,0])
                train_y = list(training[:,1])
                print("Training data created")

                # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
                # equal to number of intents to predict output intent with softmax
                model = Sequential()
                model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
                model.add(Dropout(0.5))
                model.add(Dense(64, activation='relu'))
                model.add(Dropout(0.5))
                model.add(Dense(len(train_y[0]), activation='softmax'))

                # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
                sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
                model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

                #fitting and saving the model
                hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
                model.save(f'./clientdb/{_register_data.fname}_{_register_data.pk}/{_chatbotregister.chatbot_name}-{_chatbotregister.pk}_chatbot_model.h5', hist)

                print("model created")
                intents["intents"]  =[]
                with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","w") as updated:
                    json.dump(intents,updated,indent=4)

                ##---------end
                return redirect("appclient:bot_builder")
            else:

                if "clearjson" in request.POST:
                    print("clearjsonclearjsonclearjsonclearjsonclearjson")
                    with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","w") as wdata:
                        data["intents"]=[]
                        json.dump(data,wdata,indent=4)

                    return render(request,"client_temp/ajaxforbuilderjson.html",{"data":json.dumps(data, indent=4)})
                

                tag = request.POST.get("tag")
                patterns = request.POST.getlist("patterns[]")
                print("tag: ",tag)
                print("patterns: ",patterns)


                btnlabel = request.POST.getlist("btnlabel[]")
                btnname = request.POST.getlist("btnname[]")
                btntheme = request.POST.getlist("btntheme[]")
                restype = request.POST.getlist("restype[]")
                print("-----------",request.POST.get("othertag"))
                if tag == "Other":
                    tag = request.POST.get("othertag")

                red_data = {
                    "tag":str(tag).lower(),
                    "patterns":patterns,
                    "responses":[]
                }
                res_data = ''
                # print(restype,"-----------")
                for i in range(len(restype)):
                    print("i:",i)
                    
                    if restype[i] == "btn":
                        print("btnlabel: ",btnlabel[i])
                        print("btnname: ",btnname[i])
                        print("btntheme: ",btntheme[i])

                        res_data += f"""<div class=\"container text-start\"><div class=\"row justify-content-start form-input-wrap\"><div class=\"col-lg-12\"><button type=\"button\" id=\"dynamicbtn\" onClick=\"GFG_click(this.value)\" value=\"{btnlabel[i]}\" class=\"btn form-input\">{btnlabel[i]}</button></div></div></div>"""

                    if restype[i] == "lbl":
                        print("lbllabel: ",btnlabel[i])
                        print("lblname: ",btnname[i])
                        print("lbltheme: ",btntheme[i])
                        res_data += f"""<div class=\"text-area-wrap\"><div class=\"row\"> <div class=\"col-lg-12\"> <p class=\"bot-chat botside-message\" id=\"bot-msg\">{btnlabel[i]}</p></div> </div></div>"""
                    
                    if restype[i] == "lnk":
                        print("lnklabel: ",btnlabel[i])
                        print("lnkname: ",btnname[i])
                        print("lnktheme: ",btntheme[i])
                        res_data += f"""<div class=\"text-area-wrap\"> <div class=\"row\"><div class=\"col-lg-12\"><p class=\"bot-chat botside-message\" id=\"bot-msg\"> <a target=\"_blank\" href=\"{btnlabel[i]}\">{btnname[i]}</a></p></div></div></div>"""
                    

                red_data["responses"].append(res_data)
                print(red_data,"---------------------------client")
                data["intents"].append(red_data)

                with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","w") as wdata:
                    json.dump(data,wdata,indent=4)

                return render(request,"client_temp/ajaxforbuilderjson.html",{"data":json.dumps(data, indent=4)})

            
        except Exception as e:
            print(e)      
    context = {"footer": {"url": "https://colorlib.com", "name": "cloud4code", "year": datetime.now().year, "extra_name": "chatbot"}, "title": "Client-build-bot"}
    return render(request,"client_temp/builder.html",context)



def clientchatboturl(request,c_id,ch_id):
    print(c_id,ch_id)
    c_id = generator.decrypt(c_id)
    ch_id = generator.decrypt(ch_id)
    print(c_id,ch_id)
    _client_data = ClientRegistration.objects.get(pk=int(c_id))
    _chatbot_data = ChatbotRegister.objects.get(pk=int(ch_id))
    # res = ''
    # msg=''
    # intents = json.loads(open(f'./chatbots_files/{_chatbot_data.chatbot_name}-{_chatbot_data.pk}/customer_support.json',encoding="utf-8").read())
    intents = open(f"./clientdb/{_client_data.fname}_{_client_data.pk}/{_chatbot_data.chatbot_name}-{_chatbot_data.pk}_{_chatbot_data.category}.json",encoding="utf-8").read()
    
    intents = json.loads(intents)
    words = pickle.load(open(f'./clientdb/{_client_data.fname}_{_client_data.pk}/{_chatbot_data.chatbot_name}-{_chatbot_data.pk}_words.pkl','rb'))

    classes = pickle.load(open(f'./clientdb/{_client_data.fname}_{_client_data.pk}/{_chatbot_data.chatbot_name}-{_chatbot_data.pk}_classes.pkl','rb'))
    model = load_model(f'./clientdb/{_client_data.fname}_{_client_data.pk}/{_chatbot_data.chatbot_name}-{_chatbot_data.pk}_chatbot_model.h5')
    
    if request.method == "POST":
        msg= request.POST.get("msg")
        print(msg,"-----------------------------------------------------------------:::::")
        # msg = ''
        res = chatingbot.chatbot_response(msg,intents,words,classes,model)
        print(res)
        ch = random.choice(string.ascii_letters)
        no = random. randint(0,100)
        str_ch = ch+str(no)
        context = {
            "res":res[1],
            "msg":msg,
            "title":"Bot",
            "div_id":str_ch
        }
        print(context)
        return render(request,"client_temp/ajax_data.html",context)

    context = {
        "client_data":_client_data,
        "chatbot_data":_chatbot_data,
        "title":"Bot"
    }
    return render(request,"chatbot.html",context)


def clientchatbotlist(request):
    if "email" not in request.session and "type" not in request.session and "id" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "client":
        messages.error(request, "User not allow")
        return redirect("sign-in")

    client_data = ClientRegistration.objects.get(pk=request.session["id"])
    ### for Creating Urls link  ####
    _chatbotregister_data  = ChatbotRegister.objects.filter(client_id=client_data)
    
    context = {
        "footer": {"url": "https://colorlib.com", 
        "name": "cloud4code", 
        "year": datetime.now().year, 
        "extra_name": "chatbot"},
        "client_data":client_data,
        "title":"Client-Dashboard",
        "chatbotregister":_chatbotregister_data,
        }
    return render(request,"client_temp/chatbot_list.html",context)


def clientdeletechatbot(request,pk):
    if "email" not in request.session and "type" not in request.session and "id" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "client":
        messages.error(request, "User not allow")
        return redirect("sign-in")

    _delete_data = ChatbotRegister.objects.get(pk=pk)
    _delete_data.delete()
    return redirect("appclient:clientchatbotlist")