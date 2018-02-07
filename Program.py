import os
import pickle
import base64
import sys
import hashlib
import socket
import tweepy
import time

from cryptography.fernet import Fernet
from ecdsa import VerifyingKey, BadSignatureError
from time import sleep
# Import our Twitter credentials from credentials.py
from credentials import *

def verifyKey():
    with open("dataCrypt","rb") as msgCrypt:
        msg64 = msgCrypt.read()
        datasCrypt = base64.b64decode(msg64)
    pub=open("public.pem","r").read()
    print(pub)
    sha = hashlib.sha256()
    sha.update(datasCrypt)
    shaHash = sha.hexdigest()
    vk = VerifyingKey.from_pem(pub)
    sig = open("signatureData","rb").read()
    try:
        vk.verify(sig, shaHash.encode("utf-8"))
        print("good signature")
        return 0
    except BadSignatureError:
        print("Bad program Signature. STOP.")
        return -1
    
if verifyKey() == -1:
    #os.remove("dataCrypt")
    open("data.txt","w")
else:
    with open("dataCrypt","rb") as msgCrypt:
        msg64 = msgCrypt.read()
        print(msg64)
        datasCrypt = base64.b64decode(msg64)
    with open("data.txt","w") as fileOut:
        datas = decryptor.decrypt(datasCrypt)
        fileOut.write(datas.decode("utf-8"))
    os.remove("dataCrypt")
try:
    print("start")
    open("pidChild","w").write(str(os.getpid()))


    host = "localhost"
    #host = "5.196.94.78"
    port = 12000

    # Create client to send our data to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print ("Connection on {} ".format(port) + "with host " + host)

    # Ask for a movie
    request = "getMovie"
    client.send(request.encode("utf-8"))

    # Recieve the movie
    movie = client.recv(500)
    print (movie.decode("utf-8"))

    # Access and authorize our Twitter credentials from Data.py
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    # For loop to iterate over tweets with #TheMovieBot, limit to 10
    for tweet in tweepy.Cursor(api.search,q='#TheMovieBot').items(10):

    # Get usernames of the last 10 people to use #TheMovieBot and awnser to them
        target_users = tweet.user.screen_name
        try:
            api.update_status('@' + target_users + ' Hi ! Have you seen ' + movie.decode("utf-8") + ' ?', tweet.id)
            with open("data.txt", "w") as text_file:
                text_file.write("Awnsered userName: " + target_users + " the: " + time.strftime("%d/%m/%Y"))
        
        except tweepy.TweepError as e:
            print(e.reason)
except KeyboardInterrupt:
    client.close()
    print ("Close")
    sys.exit()

