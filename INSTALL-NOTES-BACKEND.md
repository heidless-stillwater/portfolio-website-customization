

# NVM install
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

nvm ls-remote

nvm install 21.7.3
```

# gae deploy

## ENV Settings
```
GCP_PROJECT=pfolio-0
GCP_REGION=europe-west2

GCP_DB_VERSION=POSTGRES_15
GCP_INSTANCE=$GCP_PROJECT-instance-0
GCP_DB_NAME=$GCP_PROJECT-db-0
GCP_DB_USER=$GCP_PROJECT-user-0
GCP_USER_PWD=Havana111965
GCP_DB_URL=postgres://$GCP_DB_USER:Havana111965@//cloudsql/GCP_PROJECT:europe-west2:$GCP_INSTANCE/$GCP_DB_NAME

GCP_BUCKET=$GCP_PROJECT-bucket
GCP_SECRET_SETTINGS=$GCP_PROJECT-secret
GCP_SVC_ACCOUNT=GCP_PROJECT-svc@appspot.gserviceaccount.com

```

## configure gae
```
gcloud init

# initialise App Engine
gcloud app create

```
#### initialise DB Instance (takes some time  - take a break and let it process)
```
gcloud sql instances create $GCP_INSTANCE \
    --project $GCP_PROJECT \
    --database-version $GCP_DB_VERSION \
    --tier db-f1-micro \
    --region $GCP_REGION

gcloud sql databases create $GCP_DB_NAME \
    --instance $GCP_INSTANCE

gcloud sql users create $GCP_DB_USER \
    --instance $GCP_INSTANCE \
    --password $GCP_USER_PWD

# check status of instance
gcloud sql instances describe --project $GCP_PROJECT $GCP_INSTANCE

```

## storage bucket
```
# initialise BUCKET
gsutil mb -l europe-west2 gs://$GCP_BUCKET

```

### service account(s)
```
'IAM & ADMIN'->Service Accounts

--
pfolio-0@appspot.gserviceaccount.com

--

edit principal
-

# add ROLES to allow access to DB & 'secrets'
--
Secret Manager Secret Accessor
Cloud SQL Admin
Storage Admin
--
```

### generate & install KEY file
```
'IAM & ADMIN'->Service Accounts->'3 dots'->Manage Keys
'ADD KEY'->JSON

# Download & install json file
' copy to local project/app/config directory'
/home/heidless/projects/backend-live/app/config

---
export GCP_CREDENTIALS=pfolio-0-c4f9c177186a.json
---

```


## secrets setup
```
# setup local environment

cd config

echo DEBUG=True > .env
echo DATABASE_URL=$GCP_DB_URL >> .env
echo GS_BUCKET_NAME=$GCP_BUCKET >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env

echo FRONTEND_URL=https://pfolio-frontend-0-ks4eq7xt3a-nw.a.run.app/ >> .env


# store in secret manager
# enable secretmanager.googleapis.com if asked
gcloud secrets delete $GCP_SECRET_SETTINGS

gcloud secrets create $GCP_SECRET_SETTINGS --data-file .env

gcloud secrets describe $GCP_SECRET_SETTINGS

# Grant access to the secret to the App Engine standard service account
gcloud secrets add-iam-policy-binding $GCP_SECRET_SETTINGS \
    --member serviceAccount:$GCP_SVC_ACCOUNT \
    --role roles/secretmanager.secretAccessor

# test - retrieve content of '$GCP_SECRET_SETTINGS'
gcloud secrets versions access latest --secret $GCP_SECRET_SETTINGS && echo ""

```





