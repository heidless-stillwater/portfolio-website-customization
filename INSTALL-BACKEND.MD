

# initialise resources

### configure GAE
```
gcloud init
--
pfolio-2
--

# initialise App Engine
gcloud app create

```

### set config/.env-vars
```
vi config/.env-vars
--
export GCP_PROJECT=pfolio-2
--

source ./config/.env-vars
source .env-vars

```

### initialise DB Instance
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

### storage bucket
```
# initialise BUCKET
gsutil mb -l europe-west2 gs://$GCP_BUCKET

```

####################### service account #########################

### service account(s)
```
'IAM & ADMIN'->Service Accounts

--
#$GCP_PROJECT@appspot.gserviceaccount.com
#pfolio-0@appspot.gserviceaccount.com

pfolio-1@appspot.gserviceaccount.com

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

### generate & install KEY file
```
'IAM & ADMIN'->Service Accounts->'3 dots'->Manage Keys
'ADD KEY'->JSON

# Download & install json file
' copy to local project/app/config directory'
/home/heidless/projects/backend-live/app/config

---
export GCP_CREDENTIALS=pfolio-3-bf9b63bdc839.json

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
echo FRONTEND_URL=https://pfolio-frontend-0-svc-5gkdtb2iha-nw.a.run.app/ >> .env

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

### disable local settings to force use of Google Secrets
```
mv config/.env config/.env-gcp
mv .env .env-gcp

```

## configure access
https://console.cloud.google.com/sql/instances/pfolio-instance-0/connections/networking?project=heidless-pfolio-deploy-9
```
pfolio-2-instance-0 -> Connections -> Networking -> Add a Network
--
rob-laptop
2.99.19.9

--
```

### enable cloud proxy
```
cd config

# init proxy
cd config
#curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64

chmod 777 cloud-sql-proxy

```

```
./cloud-sql-proxy --credentials-file ./$GCP_CREDENTIALS \
--port 1234 $GCP_PROJECT:$GCP_REGION:$GCP_INSTANCE

# kill & restart - IF address already in use
sudo lsof -i -P -n | grep LISTEN
kill -9 <PID>

```

### check if can access DB directly
```
#gcloud sql connect $GCP_INSTANCE --database $GCP_DB_NAME --user=$GCP_DB_USER --quiet

gcloud sql connect $GCP_INSTANCE --database $GCP_DB_NAME --user=postgres --quiet

--
password:
postgres

```

### ESSENTIAL: set CLOUD vars
source ./config/.env-vars
source ./.env-vars

## config/edit settings.py
```
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'config/pfolio-2-7794a9058f42.json')
)

GS_BUCKET_NAME = 'pfolio-2-bucket'

settings_name = os.environ.get('SETTINGS_NAME', 'pfolio-2-secret')

```

## deploy to app engine
```
gcloud app deploy

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











####################################
```
<!-- export GOOGLE_CLOUD_PROJECT=$GCP_PROJECT
export USE_CLOUD_SQL_AUTH_PROXY=true
export CLOUDRUN_SERVICE_URL=https://$GCP_SVC_ACCOUNT -->

```

# Restore BACKUP


## files
```
cd ./backend/BACKUPS/24-4-2024/pfolio-0-bucket
gsutil cp -r . gs://pfolio-1-bucket

```


## db - RESTORE from BACKUP
```
# backups stored at 'backend/BACKUPS'

# copy BACKUP to Downloads
cp \
/home/heidless/projects/PFOLIO/pfolio-exemplar/portfolio-website-customization/backend/BACKUPS/24-4-2024/pfolio-0-backup-2 \
/mnt/c/Users/heidless/Downloads/pfolio-0-backup-2 

# create new(blank) DB i.e. pfolio-restore-tst-0
#Database->Create->Database
#<DB_NAME>

# initiate DB RESTORE
pgadmin-><DB_NAME>->Tools->Restore
--
format: Custom
filename: .../upload -> Downloads/pfolio-0-backup-2
role name: pfolio-0-user-0
--

```


## restore to different project
- [Restore an instance](https://cloud.google.com/sql/docs/mysql/backup-recovery/restoring)


## deploy to app engine
```
gcloud app deploy

```

# [About Cloud SQL backups](https://cloud.google.com/sql/docs/postgres/backup-recovery/backups)
- ## [Create and manage on-demand and automatic backups](https://cloud.google.com/sql/docs/postgres/backup-recovery/backing-up)
    - ### create BACKUP
```
#gcloud sql backups create \
#--async \
#--instance=INSTANCE_NAME \
#--location=BACKUP_LOCATION

gcloud sql backups create \
--async \
--instance=pfolio-0-instance-0

gcloud sql backups list \
--instance pfolio-0-instance-0

gcloud sql backups describe 1713964343491 \
--instance pfolio-0-instance-0
    
```

- ## [Restore an instance](https://cloud.google.com/sql/docs/postgres/backup-recovery/restoring)
    - ### Restore to SAME instance
```
gcloud sql instances describe pfolio-0-instance-0

#Note any instances listed in replicaNames.
#gcloud sql instances delete REPLICA_NAME

gcloud sql backups list --instance pfolio-0-instance-0

gcloud sql backups restore 1713964343491 \
--restore-instance=pfolio-0-instance-0



```

# postgres installation
```
/etc/postgresql/14/main

--

--

```


