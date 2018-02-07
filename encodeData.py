import pickle
import hashlib
import os
import base64

from cryptography.fernet import Fernet
from ecdsa import SigningKey

def createPem():  
    priv_key = SigningKey.generate()
    pub_key = priv_key.get_verifying_key()
    open("private.pem","wb").write(priv_key.to_pem())
    open("public.pem","wb").write(pub_key.to_pem())
    return


def readPem():
    with open("private.pem","rb") as fileKeyPriv:
        key_priv = SigningKey.from_pem(fileKeyPriv.read())
    
    with open("prgmCrypt","rb") as msgCrypt:
        msg64 = msgCrypt.read()
        msg = base64.b64decode(msg64)
    sha = hashlib.sha256()
    sha.update(msg)
    shaHash = sha.hexdigest()
    sig = key_priv.sign(shaHash.encode("utf-8"))
    open("signaturePrgm","wb").write(sig)

    with open("dataCrypt","rb") as DCrypt:
        msgD64 = DCrypt.read()
        msgD = base64.b64decode(msgD64)
    shaD = hashlib.sha256()
    shaD.update(msg)
    shaDHash = shaD.hexdigest()
    sigD = key_priv.sign(shaDHash.encode("utf-8"))
    open("signatureData","wb").write(sigD)
    return

key = Fernet.generate_key()
encryptor = Fernet(key)
createPem()
with open("crypt.txt","wb") as fileKey:
    pick = pickle.Pickler(fileKey)
    pick.dump(key)

if not os.path.isfile("data.txt"):
    open("data.txt","w")
with open("data.txt","r") as fileData:
    datas = fileData.read()
    strOut = encryptor.encrypt(datas.encode())
    data64 = base64.b64encode(strOut)
    open("dataCrypt","wb").write(data64)

with open("Program.py","r") as filePrgm:
    datas = filePrgm.read()
    strOut = encryptor.encrypt(datas.encode())
    str64 = base64.b64encode(strOut)
    open("prgmCrypt","wb").write(str64)
    print(str64)
readPem()
os.remove("data.txt")
os.remove("Program.py")
