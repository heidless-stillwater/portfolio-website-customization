

############################################
# ENV
```
GCP_PROJECT=pfolio-0
GCP_APP_NAME=pfolio-frontend-0
GCP_BUCKET=$GCP_PROJECT-bucket

```

### build | run
```
docker build . -t $GCP_APP_NAME
docker run -p 3000:3000 -e=PORT=3000 $GCP_APP_NAME
```

## storage bucket
```
# initialise BUCKET
#gsutil mb -l europe-west2 gs://$GCP_BUCKET

```

## push to repository
```
gcloud builds submit --tag gcr.io/$GCP_PROJECT/$GCP_APP_NAME .

## create Serice
-> deploy uploaded Container Registry
-> i.e  NOT continuous deployment

https://console.cloud.google.com/run?referrer=search&cloudshell=false&project=heidless-pfolio-deploy-9
-
'create service'

-
```

# link to app
https://pfolio-frontend-v2xr7nz45q-nw.a.run.app/


