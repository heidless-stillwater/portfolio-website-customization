# TAKE BACKUP
- ### DB
    - ### [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
    - ### [Export and import using pg_dump, pg_dumpall, and pg_restore](https://cloud.google.com/sql/docs/postgres/import-export/import-export-dmp)

```
pgadmin4->pfoli0-0-gcp->pfolio-0-db-0->Tools->Backup
--
filename: backups/<BACKUP NAME>
format: Custom
encoding: UTF8
role name: pfolio-0-user-0
--

# writes backup file to pgadmin->Tools->Storage Manager
##  download & store 'backend/BACKUPS/<BACKUP_NAME>'

# store in LINUX instance
cp /mnt/c/Users/heidless/Downloads/pfolio-0-backup-2 /home/heidless/projects/PFOLIO/pfolio-exemplar/portfolio-website-customization/backend/BACKUPS

```

- ### FILES
    - ### [gcloud storage cp](https://cloud.google.com/sdk/gcloud/reference/storage/cp)

```
#gsutil cp -r gs://bucket/folder .

gsutil cp -r gs://pfolio-0-bucket .

```

## RESTORE BACKUP
```
# backups stored at 'backend/BACKUPS'

# copy BACKUP to Downloads
cp \
/home/heidless/projects/PFOLIO/pfolio-exemplar/portfolio-website-customization/backend/BACKUPS/pfolio-0-backup-2 \
/mnt/c/Users/heidless/Downloads/pfolio-0-backup-2 

# create new(blank) DB i.e. pfolio-restore-tst-0
Database->Create->Database
<DB_NAME>

# initiate backups
pgadmin-><DB_NAME>->Tools->Restore
--
format: Custom
filename: .../upload -> Downloads/pfolio-0-backup-2
role name: pfolio-0-user-0
--

```

## Restore to New Project

```
# create new Project
```
pfolio-1

```

# initialise resources


```





