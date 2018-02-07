import pickle

from cryptography.fernet import Fernet

try:
    with open("crypt.txt","rb") as fileKey:
        unPick = pickle.Unpickler(fileKey)
        key = unPick.load()
        decryptor = Fernet(key)  

    with open("dataCrypt","rb") as dataCrypt:
        unPickData = pickle.Unpickler(dataCrypt)
        datasCrypt = unPickData.load()

    with open("dataDec.txt","w") as fileOut:
        datas = decryptor.decrypt(datasCrypt)
        fileOut.write(datas.decode("utf-8"))


except KeyboardInterrupt:

    sys.exit()
