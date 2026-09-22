# Practical gcloud Cheat Sheet

This is the short version: commands worth keeping close while you work.

> Start with the [step-by-step blog guide](https://blog.kloudxpert.com/gcloud-commands-guide/). Use this file as a lookup, not a script to run from top to bottom. For the generated command/group indexes, see [snapshot details](../commands/README.md).

## Before you copy a command

- Use Bash (for example, Google Cloud Shell). Uppercase names such as `PROJECT_ID`, `REGION` and `SERVICE_NAME` are placeholders you must replace.
- Check `gcloud auth list` and `gcloud config list` first. Resource-changing commands need appropriate permissions and can incur charges.
- Commands using existing files, buckets, services or clusters require those resources to exist.
- Commands that remove objects, disable APIs, revoke credentials or delete services change your environment. Run them only when that is your intended action.
- Use `--help` for required arguments. `SOME_COMMAND` is not a real command.

## Authentication

```bash
gcloud auth login
gcloud auth list
gcloud auth revoke ACCOUNT
gcloud auth application-default login
```

## Configuration

Creating a named configuration activates it by default. Set its account using `gcloud config set account YOUR_EMAIL` and its project before working. The account must already be authenticated; configurations do not grant IAM permissions.

```bash
gcloud config list
gcloud config get-value project
gcloud config set project PROJECT_ID
gcloud config set compute/region REGION
gcloud config set compute/zone ZONE

gcloud config configurations list
gcloud config configurations create CONFIG_NAME
gcloud config configurations activate CONFIG_NAME
```

## Projects and APIs

```bash
gcloud projects list
gcloud projects describe PROJECT_ID

gcloud services list --enabled
gcloud services list --available
gcloud services enable SERVICE_NAME
gcloud services disable SERVICE_NAME
```

## IAM

```bash
gcloud projects get-iam-policy PROJECT_ID
gcloud iam service-accounts list
gcloud iam service-accounts describe SERVICE_ACCOUNT_EMAIL

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:user@example.com" \
  --role="roles/viewer"
```

## Compute Engine

```bash
gcloud compute instances list
gcloud compute instances describe INSTANCE_NAME --zone=ZONE
gcloud compute instances create INSTANCE_NAME --zone=ZONE --machine-type=e2-medium
gcloud compute instances start INSTANCE_NAME --zone=ZONE
gcloud compute instances stop INSTANCE_NAME --zone=ZONE
gcloud compute ssh INSTANCE_NAME --zone=ZONE

gcloud compute networks list
gcloud compute networks subnets list
gcloud compute firewall-rules list
gcloud compute routes list
gcloud compute addresses list
```

## Cloud Storage

```bash
gcloud storage buckets list
gcloud storage buckets create gs://BUCKET_NAME --location=REGION
gcloud storage ls gs://BUCKET_NAME
gcloud storage cp FILE gs://BUCKET_NAME/
gcloud storage cp gs://BUCKET_NAME/FILE .
gcloud storage rm gs://BUCKET_NAME/FILE
```

## Cloud Run

Source deployment requires a deployable app in the current directory, enabled billing/APIs and permissions for both the caller and build service account. Follow the [source-deployment setup](https://docs.cloud.google.com/run/docs/deploying-source-code) first. Deleting a service does not remove stored images or other build artifacts.

```bash
gcloud run services list
gcloud run deploy SERVICE_NAME --source=. --region=REGION
gcloud run services describe SERVICE_NAME --region=REGION
gcloud run revisions list --service=SERVICE_NAME --region=REGION
gcloud run services delete SERVICE_NAME --region=REGION
```

## GKE

Install `kubectl` and `gke-gcloud-auth-plugin` on local machines. `LOCATION` is the cluster's region or zone. The endpoint must be reachable and your account authorized. See [GKE client setup](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl).

```bash
gcloud container clusters list
gcloud container clusters describe CLUSTER_NAME --location=LOCATION
gcloud container clusters get-credentials CLUSTER_NAME --location=LOCATION
```

## Artifact Registry

```bash
gcloud artifacts repositories list
gcloud artifacts repositories create REPOSITORY \
  --repository-format=docker \
  --location=REGION

gcloud auth configure-docker REGION-docker.pkg.dev
gcloud artifacts docker images list REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY
```

## Cloud Build

A bare `gcloud builds submit` expects `cloudbuild.yaml` in the source directory. For a Dockerfile build, use the documented `--tag` option instead. See [build submission options](https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit).

```bash
gcloud builds submit
gcloud builds submit --config=cloudbuild.yaml
gcloud builds list
gcloud builds describe BUILD_ID
gcloud builds log BUILD_ID
```

## Secret Manager

The literal `secret-value` below is a dummy value. Do not paste a real credential into a typed command: it can remain in shell history. Accessing a secret prints its value, so avoid shared terminals and logs.

```bash
gcloud secrets list
gcloud secrets create SECRET_NAME --replication-policy=automatic
printf '%s' 'secret-value' | gcloud secrets versions add SECRET_NAME --data-file=-
gcloud secrets versions access latest --secret=SECRET_NAME
```

## Cloud SQL

```bash
gcloud sql instances list
gcloud sql instances describe INSTANCE_NAME
gcloud sql databases list --instance=INSTANCE_NAME
gcloud sql users list --instance=INSTANCE_NAME
```

## Logging

```bash
gcloud logging read 'severity>=ERROR' --limit=50
gcloud logging read 'resource.type="cloud_run_revision"' --limit=50
```

## Formatting and filtering

```bash
gcloud compute instances list --filter="status=RUNNING"
gcloud compute instances list --format=json
gcloud compute instances list --format=yaml
gcloud compute instances list --format="table(name,zone,status)"
gcloud compute instances list --format="csv(name,zone,status)"
```

## Troubleshooting

```bash
gcloud version
gcloud info
gcloud auth list
gcloud config list
gcloud SOME_COMMAND --verbosity=debug
gcloud SOME_COMMAND --log-http
```

## Help

```bash
gcloud help
gcloud compute --help
gcloud compute instances --help
gcloud compute instances create --help
```

## Scripting habits

Impersonation requires the Service Account Credentials API and token-generation permission on the target service account; the target account also needs permission for the operation. `--quiet` suppresses confirmation prompts, so review destructive commands before using it.

```bash
# Explicit project
gcloud compute instances list --project=PROJECT_ID

# Non-interactive automation
gcloud SOME_COMMAND --quiet

# Service-account impersonation
gcloud SOME_COMMAND \
  --impersonate-service-account=SERVICE_ACCOUNT_EMAIL

# One value for a script
gcloud run services describe SERVICE_NAME \
  --region=REGION \
  --format="value(status.url)"
```

Official reference: https://cloud.google.com/sdk/gcloud/reference
