from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import pickle
import pymongo
import io
from Crypto import Random

DECODER = "splead4852_!gg34"
DATABASE = "RESUME"
PASS_FILE = "connect.pass"


def decrypt_obj(key, filename):
    chunksize = 64 * 1024
    out=b""
    with open(filename,"rb") as infile:
        secret = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key,AES.MODE_CBC,IV)
        while True:
            chunk = infile.read(chunksize)
            if len(chunk)==0:
                break
            out+=decryptor.decrypt(chunk)
    result = pickle.loads(out)
    return result

def getKey(password):
    hasher=SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def decrypt_obj_b(key, bytestream):
    chunksize = 64 * 1024
    out=b""
    infile = io.BytesIO(bytestream)
    IV = infile.read(16)
    decryptor = AES.new(key,AES.MODE_CBC,IV)
    while True:
        chunk = infile.read(chunksize)
        if len(chunk)==0:
            break
        out+=decryptor.decrypt(chunk)
    infile.close()
    return out

def encrypt_obj_b(key,picklyobj):
    result = b""
    chunksize = 64 * 1024
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    infile = io.BytesIO(picklyobj)
    result+=IV
    while True:
        chuck = infile.read(chunksize)
        if len(chuck) == 0:
            break
        elif len(chuck) % 16 != 0:
            chuck += b' ' * (16 - len(chuck) % 16)
        result+=encryptor.encrypt(chuck)
    infile.close()
    return result


def e_obj(password,obj):
    return encrypt_obj_b(getKey(password), obj2Bytes(obj))


def d_obj(password,encode):
    return bytes2Obj(decrypt_obj_b(getKey(password), encode))


def obj2Bytes(obj):
    return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)


def bytes2Obj(bytestream):
    return pickle.loads(bytestream)


def get_data():
    f = open(PASS_FILE, "rb")
    connector_str = d_obj(DECODER, f.read())["connect"]
    f.close()
    client = pymongo.MongoClient(connector_str)
    db = client[DATABASE]
    result = {}
    buffer = {}
    for i,name in enumerate(db.collection_names()):
        result[name] = []
        col = db[name]
        query = col.find({})
        index = 0
        for q in query:
            q["uid"]=name+"_"+str(index)
            index+=1
            result[name].append(q)
            buffer[q["uid"]]=name
    client.close()

    resource_query = {
        "all_cata":set(),
        "all_item":[],
        "uid_img":{},
    }
    for item in result["resource"]:
        if item["UUID"] in buffer:
            resource_query["all_cata"].add(buffer[item["UUID"]])
            item["category"] = buffer[item["UUID"]]
            resource_query["all_item"].append(item)
            resource_query["uid_img"][item["UUID"]]=item["Img"]
        else:
            resource_query["all_cata"].add(item["UUID"])
            item["category"] = item["UUID"]
            resource_query["all_item"].append(item)
        # if buffer[item["UUID"]] not in resource_query:
        #     resource_query[buffer[item["UUID"]]]=[]
        # resource_query[buffer[item["UUID"]]].append(item)
    resource_query["all_cata"] = list(resource_query["all_cata"])
    return result,resource_query
