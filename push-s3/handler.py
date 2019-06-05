from minio import Minio
import json
import uuid
import os

def handle(st):
    req = json.loads(st)

    secure = True if os.getenv('s3_tls', "false") == "true" else False

    access_key = get_secret("access-key")
    secret_key = get_secret("secret-key")

    mc = Minio(os.environ['s3_hostname'],
                  access_key = access_key,
                  secret_key = secret_key,
                  secure = secure)

    download_push(st, mc)

def get_secret(key):
    val = ""
    with open("/var/openfaas/secrets/" + key) as f:
        val = f.read()
    return val

def download_push(st, mc):
    # write to temporary file
    file_name = get_temp_file()
    f = open("/tmp/" + file_name, "wb")
    f.write(r.content)
    f.close()

    # sync to Minio
    mc.fput_object("incoming", file_name, "/tmp/" + file_name)

    return file_name

def get_temp_file():
    uuid_value = str(uuid.uuid4())

    return uuid_value

