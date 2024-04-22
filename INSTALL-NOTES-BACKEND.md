

# NVM install
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

nvm ls-remote

nvm install 21.7.3

```

# gae deploy

## ENV Settings
source ./config/.env-vars
source ./.env-vars

<!-- 
```
GCP_PROJECT=pfolio-0
GCP_REGION=europe-west2

GCP_DB_VERSION=POSTGRES_15
GCP_INSTANCE=$GCP_PROJECT-instance-0
GCP_DB_NAME=$GCP_PROJECT-db-0
GCP_DB_USER=$GCP_PROJECT-user-0
GCP_USER_PWD=Havana111965
GCP_DB_URL=postgres://$GCP_DB_USER:Havana111965@//cloudsql/$GCP_PROJECT:europe-west2:$GCP_INSTANCE/$GCP_DB_NAME

GCP_BUCKET=$GCP_PROJECT-bucket
GCP_SECRET_SETTINGS=$GCP_PROJECT-secret
GCP_SVC_ACCOUNT=$GCP_PROJECT@appspot.gserviceaccount.com

``` -->

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
export GCP_CREDENTIALS=pfolio-0-d8fe64938af3.json

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
echo FRONTEND_URL=https://pfolio-frontend-0-6untcb67la-nw.a.run.app/ >> .env

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

## DB URL
```
# assemble link from the above info
#postgres://<USER>:<PWD>@//cloudsql/<PROJECT ID>:<REGION>:<INSTANCE>/<DB>

--
#postgres://pfolio-0-user-0:Havana111965@//cloudsql/pfolio-0-secret:europe-west2:pfolio-0-instance-0/pfolio-0-user-9

--
```

### disable local settings to force use of Google Secrets
```
mv config/.env config/.env-gcp

mv .env .env-gcp


## configure access
https://console.cloud.google.com/sql/instances/pfolio-instance-0/connections/networking?project=heidless-pfolio-deploy-9
```
pfolio-0-instance-0 -> Connections -> Networking -> Add a Network
--
rob-laptop
2.99.19.9

--
```

### check if can access DB directly
```
gcloud sql connect $GCP_INSTANCE --database $GCP_DB_NAME --user=$GCP_DB_USER --quiet

--
password:
Havana111965

```

### ESSENTIAL: set CLOUD vars
source ./config/.env-vars
source ./.env-vars

```
<!-- export GOOGLE_CLOUD_PROJECT=$GCP_PROJECT
export USE_CLOUD_SQL_AUTH_PROXY=true
export CLOUDRUN_SERVICE_URL=https://$GCP_SVC_ACCOUNT -->

```

### enable cloud proxy
```
cd config

# init proxy
cd config
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64

chmod 777 cloud-sql-proxy

```

./cloud-sql-proxy --credentials-file ./$GCP_CREDENTIALS \
--port 1234 $GCP_PROJECT:$GCP_REGION:$GCP_INSTANCE

# kill & restart - IF address already in use
sudo lsof -i -P -n | grep LISTEN
kill -9 <PID>

```

### init & run backend
```
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
-
heidless
rob.lockhart@yahoo.co.uk
sdfsdgasgTHW66GDGdfdff
-

# init 'static' directory
mkdir app/build/static
python manage.py collectstatic

python manage.py runserver 8080

# view site
http://localhost:8080

# view site/admin
http://localhost:8080/admin
```

## Deploy the app to the App Engine standard environment

```
# initialze app.yaml
app.yaml

--

```

################################################
## deploy to app engine
```
gcloud app deploy

```

## display APP URL
```
gcloud app describe --format "value(defaultHostname)"
--
https://heidless-pfolio-deploy-9.nw.r.appspot.com

--

```

## monitor logs
```
gcloud app logs tail -s default
-
target url: https://pfolio-backend-2.ew.r.appspot.com
target service account: pfolio-backend-2@appspot.gserviceaccount.com
-

```

## Open app.yaml and update the value of APPENGINE_URL with your deployed URL:
```
vi app.yaml
--
env_variables:
	APPENGINE_URL: https://pfolio-backend-2.ew.r.appspot.com/

--

```

## BACKUPS
```
pg_dump \
-U pfolio-user-0	 \
--format=custom \
--no-owner \
--no-acl \
pfolio-db-0	 > pfolio-db-0.dmp

```

## re-deploy
```
gcloud app deploy

```



# pgadmin

## Create pgadmin dir
```
mkdir <project root>/pgadmin
cd !$
```

## Dockerfile
Create
```
FROM dpage/pgadmin4

ENV PGADMIN_DEFAULT_EMAIL=rob.lockhart@yahoo.co.uk

ENV PGADMIN_DEFAULT_PASSWORD=havana111965

ENV PGADMIN_LISTEN_PORT=8080
```


Builld
```
gcloud builds submit --tag=gcr.io/heidless-pfolio-deploy-4/pgadmin4
```

Deploy
```
gcloud run deploy --image=gcr.io/heidless-pfolio-deploy-4/pgadmin4 --platform=managed
```

## Access
https://pgadmin4-um4b6gn3cq-nw.a.run.app

## [Connecting to GCP’s Cloud SQL (PostgresSQL) from PgAdmin — 3 simple steps](https://cshiva.medium.com/connecting-to-gcps-cloud-sql-postgressql-from-pgadmin-3-simple-steps-2f4530488a4c)

## [pgAdmin Backup Database in PostgreSQL Simplified 101](https://hevodata.com/learn/pgadmin-backup-database/#11)

## [Backup Dialog](https://www.pgadmin.org/docs/pgadmin4/development/backup_dialog.html)

## [Why pgAdmin 4 is so slow](https://stackoverflow.com/questions/62186945/why-pgadmin-4-is-so-slow)

#### LOGIN CREDENTIALS (See contents of Dockerfile)

## access locally
http://127.0.0.1/pgadmin4

# phpMyAdmin
https://cloud.google.com/sql/docs/mysql/phpmyadmin-on-app-engine

dropdb --if-exists --username postgres hpfolio

psql -U postgres postgres
CREATE DATABASE pfolio_db_local;
CREATE USER arjuna11 WITH SUPERUSER PASSWORD 'havana11';
\l
\du
\q








