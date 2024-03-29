from minio import Minio
import json
import uuid
import os, sys

def handle(body):
    secure = True if os.getenv("s3_secure", "false") == "true" else False
    bucket_name = os.getenv("s3_bucket_name")

    access_key = get_secret("access-key")
    secret_key = get_secret("secret-key")

    mc = Minio(os.environ["s3_hostname"],
                  access_key = access_key,
                  secret_key = secret_key,
                  secure = secure)

    sys.stderr.write("Endpoint: {}, secure: {}\n".format(os.environ["s3_hostname"], secure))
    file_out = download_push(body.encode(), bucket_name, mc)
    res = {"file": file_out}
    return json.dumps(res)

def get_secret(key):
    val = ""
    with open("/var/openfaas/secrets/" + key) as f:
        val = f.read()
    return val

def download_push(body, bucket_name, mc):
    # write to temporary file
    file_name = get_temp_file()
    f = open("/tmp/" + file_name, "wb")
    f.write(body)
    f.close()

    # sync to Minio
    mc.fput_object(bucket_name, file_name, "/tmp/" + file_name)

    return file_name

def get_temp_file():
    uuid_value = str(uuid.uuid4())

    return uuid_value

