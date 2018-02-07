import pickle
import base64
import sys
import hashlib
import os
import time
import subprocess as s

from cryptography.fernet import Fernet
from ecdsa import VerifyingKey, BadSignatureError

def killProcess(pid):
    s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
def verifyKey():
    with open("prgmCrypt","rb") as msgCrypt:
        msg64 = msgCrypt.read()
        datasCrypt = base64.b64decode(msg64)
    pub=open("public.pem","r").read()
    print(pub)
    sha = hashlib.sha256()
    sha.update(datasCrypt)
    shaHash = sha.hexdigest()
    vk = VerifyingKey.from_pem(pub)
    sig = open("signaturePrgm","rb").read()
    try:
        vk.verify(sig, shaHash.encode("utf-8"))
        print("good signature")
        return 0
    except BadSignatureError:
        return -1
try:
    with open("crypt.txt","rb") as fileKey:
        unPick = pickle.Unpickler(fileKey)
        key = unPick.load()
    decryptor = Fernet(key)
    with open("prgmCrypt","rb") as msgCrypt:
        msg64 = msgCrypt.read()
        print(msg64)
        datasCrypt = base64.b64decode(msg64)
    if verifyKey() == -1:
        # print("Bad program Signature. STOP.")
        sys.exit()
    
    with open("Program.py","w") as fileOut:
        datas = decryptor.decrypt(datasCrypt)
        fileOut.write(datas.decode("utf-8"))
    os.system("python program.py -i")
    while(1):
        time.sleep(0.5)
except KeyboardInterrupt:
    pid = int(open("pidChild","r").read())
    killProcess(pid)
    with open("crypt.txt","rb") as fileKey:
        unPick = pickle.Unpickler(fileKey)
        keyD = unPick.load()
    encryptor = Fernet(keyD)
    with open("data.txt","r") as fileData:
        datas = fileData.read()
        strOut = encryptor.encrypt(datas.encode())
        data64 = base64.b64encode(strOut)
        open("dataCrypt","wb").write(data64)

        
    os.remove("data.txt")
    os.remove("Program.py")
    sys.exit()
