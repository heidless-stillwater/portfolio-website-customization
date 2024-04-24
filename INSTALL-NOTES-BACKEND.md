

########################### NVM #################################

# NVM install
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

nvm ls-remote

nvm install 21.7.3

```

##################### project init ##############################

# gae deploy

## ENV Settings
source ./config/.env-vars
source ./.env-vars


## configure gae
```
gcloud init

# initialise App Engine
gcloud app create

```

######################### DB config #############################

#### initialise DB Instance (takes some time  - take a break and let it process)
```
gcloud sql instances create $GCP_INSTANCE \
    --project $GCP_PROJECT \
    --database-version $GCP_DB_VERSION \
    --tier db-f1-micro \
    --region $GCP_REGION

gcloud sql users set-password postgres \
--instance=$GCP_INSTANCE \
--password=postgres

gcloud sql databases create $GCP_DB_NAME \
    --instance $GCP_INSTANCE

gcloud sql users create $GCP_DB_USER \
    --instance $GCP_INSTANCE \
    --password $GCP_USER_PWD

# check status of instance
gcloud sql instances describe --project $GCP_PROJECT $GCP_INSTANCE

```
########################### bucket ##############################


## storage bucket
```
# initialise BUCKET
gsutil mb -l europe-west2 gs://$GCP_BUCKET

```

####################### service account #########################

### service account(s)
```
'IAM & ADMIN'->Service Accounts

--
pfolio-0@appspot.gserviceaccount.com

--

edit principal
--

# add ROLES to allow access to DB & 'secrets'
--
Secret Manager Secret Accessor
Cloud SQL Admin
Storage Admin
--
```

################### credentials - key file ######################

### generate & install KEY file
```
'IAM & ADMIN'->Service Accounts->'3 dots'->Manage Keys
'ADD KEY'->JSON

# Download & install json file
' copy to local project/app/config directory'
/home/heidless/projects/backend-live/app/config

---
export GCP_CREDENTIALS=pfolio-0-e947087b6cfe.json

---
```

########################### secrets #############################

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

gcloud sql connect $GCP_INSTANCE --database $GCP_DB_NAME --user=postgres --quiet

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

###################### cloud proxy ##############################

### enable cloud proxy
```
cd config

# init proxy
cd config
#curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64

chmod 777 cloud-sql-proxy

```

./cloud-sql-proxy --credentials-file ./$GCP_CREDENTIALS \
--port 1234 $GCP_PROJECT:$GCP_REGION:$GCP_INSTANCE

# kill & restart - IF address already in use
sudo lsof -i -P -n | grep LISTEN
kill -9 <PID>

```

############################# run local ##############################

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

########################### deploy ##############################

## Deploy the app to the App Engine standard environment

```
# initialze app.yaml
app.yaml

--
```


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

########################### pg admin ############################


## [pgAdmin 4 (APT)](https://www.pgadmin.org/download/pgadmin-4-apt/)
```
#
# Setup the repository
#

# Install the public key for the repository (if not done previously):
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg

# Create the repository configuration file:
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'

#
# Install pgAdmin
#

# Install for both desktop and web modes:
sudo apt install pgadmin4

# Install for desktop mode only:
sudo apt install pgadmin4-desktop

# Install for web mode only: 
sudo apt install pgadmin4-web 

# Configure the webserver, if you installed pgadmin4-web:
sudo /usr/pgadmin4/bin/setup-web.sh

```

## invoke pgadmin4
```
http://localhost/pgadmin4
--
rob.lockhart@yahoo.co.uk
postgres
--

```
## set postgres password 
gcloud sql users set-password postgres \
--instance=$GCP_INSTANCE \
--password=postgres

## configure pgadmin server
```
# ensure proxy is running
# PORT is 1234
Servers->Register->Deploy Cloud Instance

# General
name: pfolio-0-gcp

# Connection
Hostname: localhost
Port: 1234
Maintenance DB: pfolio-0-db-0
Username: pfolio-0-user-0
Password: Havana111965

```














## Backup

## [pgAdmin Backup Database in PostgreSQL Simplified 101](https://hevodata.com/learn/pgadmin-backup-database/#11)

## [Backup Dialog](https://www.pgadmin.org/docs/pgadmin4/development/backup_dialog.html)

## [Why pgAdmin 4 is so slow](https://stackoverflow.com/questions/62186945/why-pgadmin-4-is-so-slow)

#### LOGIN CREDENTIALS (See contents of Dockerfile)

## access locally
http://localhost/pgadmin4






- ### [Backup Dialog](https://www.pgadmin.org/docs/pgadmin4/8.4/backup_dialog.html#:~:text=You%20can%20backup%20a%20single,in%20the%20dialog%20title%20bar.)

```

```

- ## restore backup


# [PostgreSQL 15 : Install](https://www.server-world.info/en/note?os=Ubuntu_23.04&p=postgresql&f=1)

- ### [PostGres:upgrade-script](https://salsa.debian.org/postgresql/postgresql-common/raw/master/pgdg/apt.postgresql.org.sh)

```
sudo apt update

sudo apt install postgresql

```










## Create pgadmin dir

### [Deploy PGAdmin4 to Google Cloud Run](https://medium.com/@kobby.fletcher/deploy-pgadmin4-to-google-cloud-run-a5e5988784fb)

```
mkdir <project root>/pgadmin
cd !$
```

## Dockerfile
Create & initialise login credentials
```
FROM dpage/pgadmin4

ENV PGADMIN_DEFAULT_EMAIL=rob.lockhart@yahoo.co.uk

ENV PGADMIN_DEFAULT_PASSWORD=havana111965

ENV PGADMIN_LISTEN_PORT=8080
```

Builld
```
gcloud builds submit --tag=gcr.io/pfolio-0/pgadmin4 .

```

Deploy
```
gcloud run deploy --image=gcr.io/pfolio-0/pgadmin4 --platform=managed

```

## Access
https://pgadmin4-um4b6gn3cq-nw.a.run.app

--- 

## configure server

Servers->Register->Deploy Cloud Instance
```
Google Cloud SQL
```

POSTGRES_15
pfolio-0-instance-0
pfolio-0-db-0
pfolio-0-user-0
Havana111965

- ### [Setting up OAuth 2.0](https://support.google.com/cloud/answer/6158849?hl=en#userconsent&zippy=%2Cuser-consent%2Cpublic-and-internal-applications)





## [Connecting to GCP’s Cloud SQL (PostgresSQL) from PgAdmin — 3 simple steps](https://cshiva.medium.com/connecting-to-gcps-cloud-sql-postgressql-from-pgadmin-3-simple-steps-2f4530488a4c)

- ## Step 1: Set-up GCP and Create Database instance & Database on GCP
    - ### [Manage users with built-in authentication](https://cloud.google.com/sql/docs/mysql/create-manage-users)
```
gcloud sql users set-password postgres \
--instance=$GCP_INSTANCE \
--password=postgres

```

- ## STEP 2: Install PgAdmin on your computer
```
Download from: 
https://www.pgadmin.org/download/
```

- ## STEP 3: Connect to Database Instance from PgAdmin
```
https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html

docker pull dpage/pgadmin4:latest

docker run -p 8000:8000 \
    -e 'PGADMIN_DEFAULT_EMAIL=rob.lockhart@yahoo.co.uk' \
    -e 'PGADMIN_DEFAULT_PASSWORD=password' \
    -d dpage/pgadmin4


# intialize detail password file
touch .passwd

# define environment var
export PGADMIN_DEFAULT_EMAIL=rob.lockhart@yahoo.co.uk
export PGADMIN_DEFAULT_PASSWORD=password
export PGADMIN_DEFAULT_PASSWORD_FILE=./.passwd



```











# phpMyAdmin
https://cloud.google.com/sql/docs/mysql/phpmyadmin-on-app-engine

dropdb --if-exists --username postgres hpfolio

psql -U postgres postgres
CREATE DATABASE pfolio_db_local;
CREATE USER arjuna11 WITH SUPERUSER PASSWORD 'havana11';
\l
\du
\q




