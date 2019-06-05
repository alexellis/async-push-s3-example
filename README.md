# async-push-s3-example

Example of invoking a function and putting the result into S3

## Get started

* Provision an S3 bucket with a cloud such as DigitalOcean, or with Minio and its helm chart

* Configure `stack.yml` with the `hostname` and `bucket_name`

```yaml
    environment:
      s3_hostname: kubecon.fra1.digitaloceanspaces.com
      s3_secure: true
      s3_bucket_name: kubecon
```

* Create your secrets

```sh
# Create an access key for these

export ACCESS_KEY=""
export SECRET_KEY=""

echo -n "${ACCESS_KEY}" | faas-cli secret create access-key
echo -n "${SECRET_KEY}" | faas-cli secret create secret-key
```

* Now deploy a function from the store, which takes some time to execute

```sh
faas-cli store deploy inception
```

Check for the function to download and become ready:

```sh
faas-cli describe inception
```

* Check the function is working

```
# Find an image to analyze from https://commons.wikimedia.org/wiki/Main_Page
export URL="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Kizhi_06-2017_img11_Lazarus_Resurrection_Church.jpg/1000px-Kizhi_06-2017_img11_Lazarus_Resurrection_Church.jpg"

echo -n "${URL}" | faas-cli invoke inception
```

```json
[{"name": "church", "score": 0.43802326917648315}, {"name": "bell cote", "score": 0.40113094449043274}, {"name": "palace", "score": 0.025248214602470398}, {"name": "worm fence", "score": 0.008437118493020535}, {"name": "monastery", "score": 0.006785948295146227}, {"name": "boathouse", "score": 0.0067488932982087135}, {"name": "lakeside", "score": 0.006559893023222685}, {"name": "stupa", "score": 0.005963603965938091}, {"name": "picket fence", "score": 0.005611276254057884}, {"name": "barn", "score": 0.005575225688517094}]
```

* Now we'll execute it asynchronously and have the result stored in our s3 bucket.

You can pick a random image from [this link](https://commons.wikimedia.org/wiki/Special:Random/File)

```sh
export URL="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Haut_Santenay_Vue_d%27ensemble_18.jpg/1600px-Haut_Santenay_Vue_d%27ensemble_18.jpg"

echo -n "${URL}" | faas-cli invoke --async inception -H "X-Callback-Url=http://gateway.openfaas:8080/function/push-s3"
```

> Note: if using Swarm, then change `http://gateway.openfaas:8080` to `http://gateway:8080`.

* Head over to your s3 bucket, and you'll see the result available for download

You can also find the filename from the logs of the function, or the queue-worker.

```sh
2019/06/05 08:48:59 stderr: Endpoint: fra1.digitaloceanspaces.com, secure: True
2019/06/05 08:48:59 Duration: 0.699364 seconds
{"file": "8eb7e2c1-6a62-49b7-976e-a097b73141eb"}
```
