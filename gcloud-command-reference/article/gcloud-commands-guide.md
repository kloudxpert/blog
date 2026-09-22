# gcloud Commands: A Practical Google Cloud CLI Guide for Engineers

If you work with Google Cloud long enough, you end up using `gcloud` whether you planned to or not.

You use it to switch projects, deploy a Cloud Run service, connect to a GKE cluster, inspect IAM, check logs, enable an API, or figure out why something works in the console but not from your terminal.

Most engineers learn it the same way: one copied command at a time.

That works, but it leaves you with a pile of commands and no real mental model.

This guide takes a different approach. The goal is not to memorize hundreds of commands. It is to understand how `gcloud` is put together, learn the small set of commands you will use constantly, and know how to find the rest when you need them.

> **Complete command reference:** I keep the long, searchable command reference in GitHub so this article can stay readable. The GitHub version does more than list command names: every entry includes a short **"What it does"** explanation generated from that command's built-in `gcloud ... --help` text.  
> https://github.com/kloudxpert/blog/tree/main/gcloud-command-reference

For example, the reference is intended to read like this:

```text
gcloud compute instances list
What it does: Lists Compute Engine virtual machine instances.
Usage help: gcloud compute instances list --help
```

So there are really two pieces:

- **This article** explains the mental model, common workflows, and the commands engineers use most often.
- **The GitHub reference** is the complete command-by-command lookup, with a short explanation for each command.

That split is deliberate. A giant list is useful when you are searching for a command. It is not a good way to learn how `gcloud` actually fits together.

---

## 1. First, understand the shape of a gcloud command

A `gcloud` command usually reads left to right:

```bash
gcloud compute instances list
```

Think of that as:

```text
gcloud
  └── compute
       └── instances
            └── list
```

- `gcloud` — the CLI
- `compute` — the command group
- `instances` — the resource group
- `list` — the operation

Once you see this pattern, unfamiliar commands become much easier to guess.

For example:

```bash
gcloud run services list
gcloud artifacts repositories list
gcloud secrets versions access
gcloud container clusters describe
```

You do not need to remember every command. You need to understand the hierarchy.

Google's CLI also has **GA, beta, and alpha** command tracks. A command may appear as:

```bash
gcloud run services list
gcloud beta some-group some-command
gcloud alpha some-group some-command
```

For production scripts, prefer GA commands unless you deliberately need a beta or alpha feature.

---

## 2. Before doing anything, check who you are and where you are

A surprising number of CLI mistakes happen because the engineer is using the wrong account or the wrong project.

These are the commands I check first when something feels strange:

```bash
gcloud auth list
gcloud config list
gcloud config get-value project
gcloud config get-value account
```

To sign in:

```bash
gcloud auth login
```

For Application Default Credentials used by local application code:

```bash
gcloud auth application-default login
```

Those are different things. Your `gcloud` CLI credentials and the credentials your local application uses are related concepts, but they are not interchangeable.

To set a project:

```bash
gcloud config set project PROJECT_ID
```

To set defaults for region and zone:

```bash
gcloud config set compute/region REGION
gcloud config set compute/zone ZONE
```

For one-off commands, I often prefer being explicit:

```bash
gcloud compute instances list --project=PROJECT_ID
```

That is especially useful when you work across several environments.

---

## 3. Use named configurations for Dev, Test and Prod

If you constantly switch between projects, do not keep overwriting one global configuration.

Create separate configurations instead.

```bash
gcloud config configurations create dev
gcloud config set project DEV_PROJECT_ID

gcloud config configurations create prod
gcloud config set project PROD_PROJECT_ID
```

List them:

```bash
gcloud config configurations list
```

Switch between them:

```bash
gcloud config configurations activate dev
gcloud config configurations activate prod
```

Or use one for a single command:

```bash
gcloud --configuration=prod compute instances list
```

This is one of the simplest ways to reduce accidental cross-environment work.

---

## 4. Stop searching the web for every command

The CLI already knows how to explain itself.

Start here:

```bash
gcloud help
```

Then narrow down:

```bash
gcloud compute --help
gcloud compute instances --help
gcloud compute instances create --help
```

That last step matters because flags often change faster than your memory.

If I know the command family but not the exact syntax, I normally use `--help` before I search anywhere else.

You can also inspect your installed version:

```bash
gcloud version
```

And general environment information:

```bash
gcloud info
```

---

## 5. Projects and APIs

List projects you can access:

```bash
gcloud projects list
```

Describe one:

```bash
gcloud projects describe PROJECT_ID
```

A common setup task is enabling services:

```bash
gcloud services list --available
gcloud services list --enabled
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

Disable a service only when you understand the impact:

```bash
gcloud services disable SERVICE_NAME
```

For scripts, pass the project explicitly when the environment matters:

```bash
gcloud services enable run.googleapis.com --project=PROJECT_ID
```

---

## 6. IAM commands you will use often

See a project's IAM policy:

```bash
gcloud projects get-iam-policy PROJECT_ID
```

A more readable table:

```bash
gcloud projects get-iam-policy PROJECT_ID \
  --format="table(bindings.role,bindings.members)"
```

Add a role binding:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:user@example.com" \
  --role="roles/viewer"
```

Remove it:

```bash
gcloud projects remove-iam-policy-binding PROJECT_ID \
  --member="user:user@example.com" \
  --role="roles/viewer"
```

List service accounts:

```bash
gcloud iam service-accounts list
```

Describe one:

```bash
gcloud iam service-accounts describe SERVICE_ACCOUNT_EMAIL
```

For production automation, avoid reaching for service-account key files by default. Where your environment supports it, prefer short-lived credentials and service account impersonation.

For example:

```bash
gcloud projects describe PROJECT_ID \
  --impersonate-service-account=SERVICE_ACCOUNT_EMAIL
```

---

## 7. Compute Engine

List VMs:

```bash
gcloud compute instances list
```

Describe one:

```bash
gcloud compute instances describe INSTANCE_NAME --zone=ZONE
```

Create a VM:

```bash
gcloud compute instances create INSTANCE_NAME \
  --zone=ZONE \
  --machine-type=e2-medium
```

Start and stop:

```bash
gcloud compute instances start INSTANCE_NAME --zone=ZONE
gcloud compute instances stop INSTANCE_NAME --zone=ZONE
```

SSH:

```bash
gcloud compute ssh INSTANCE_NAME --zone=ZONE
```

Copy a file:

```bash
gcloud compute scp ./local-file.txt \
  INSTANCE_NAME:~/local-file.txt \
  --zone=ZONE
```

Networking commands are also under `gcloud compute`:

```bash
gcloud compute networks list
gcloud compute networks subnets list
gcloud compute firewall-rules list
gcloud compute addresses list
gcloud compute routes list
```

This is worth remembering because not everything under `compute` is a VM.

---

## 8. Cloud Storage: use gcloud storage

For current workflows, use the `gcloud storage` command group.

List buckets:

```bash
gcloud storage buckets list
```

Create a bucket:

```bash
gcloud storage buckets create gs://BUCKET_NAME \
  --location=REGION
```

List objects:

```bash
gcloud storage ls gs://BUCKET_NAME
```

Copy a file:

```bash
gcloud storage cp ./report.csv gs://BUCKET_NAME/
```

Copy a directory recursively:

```bash
gcloud storage cp --recursive ./data gs://BUCKET_NAME/
```

Download:

```bash
gcloud storage cp gs://BUCKET_NAME/report.csv .
```

Remove an object:

```bash
gcloud storage rm gs://BUCKET_NAME/report.csv
```

---

## 9. Cloud Run

List services:

```bash
gcloud run services list
```

Deploy from source:

```bash
gcloud run deploy SERVICE_NAME \
  --source=. \
  --region=REGION
```

Deploy an existing image:

```bash
gcloud run deploy SERVICE_NAME \
  --image=REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE:TAG \
  --region=REGION
```

Describe a service:

```bash
gcloud run services describe SERVICE_NAME --region=REGION
```

Get only the service URL:

```bash
gcloud run services describe SERVICE_NAME \
  --region=REGION \
  --format="value(status.url)"
```

List revisions:

```bash
gcloud run revisions list \
  --service=SERVICE_NAME \
  --region=REGION
```

Delete a service:

```bash
gcloud run services delete SERVICE_NAME --region=REGION
```

---

## 10. GKE

List clusters:

```bash
gcloud container clusters list
```

Describe a cluster:

```bash
gcloud container clusters describe CLUSTER_NAME \
  --location=LOCATION
```

Get Kubernetes credentials:

```bash
gcloud container clusters get-credentials CLUSTER_NAME \
  --location=LOCATION
```

After that, `kubectl` uses the generated kubeconfig context.

Create a cluster only after checking the current flags for the cluster mode you want:

```bash
gcloud container clusters create --help
```

GKE evolves quickly, so this is one area where blindly reusing an old command from a blog post is a bad habit.

---

## 11. Artifact Registry

List repositories:

```bash
gcloud artifacts repositories list
```

Create a Docker repository:

```bash
gcloud artifacts repositories create REPOSITORY \
  --repository-format=docker \
  --location=REGION
```

Configure Docker authentication:

```bash
gcloud auth configure-docker REGION-docker.pkg.dev
```

List Docker images:

```bash
gcloud artifacts docker images list \
  REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY
```

---

## 12. Cloud Build

Submit the current directory for a build:

```bash
gcloud builds submit
```

Submit with a configuration file:

```bash
gcloud builds submit --config=cloudbuild.yaml
```

List builds:

```bash
gcloud builds list
```

Describe a build:

```bash
gcloud builds describe BUILD_ID
```

Read build logs:

```bash
gcloud builds log BUILD_ID
```

Before a source-based deployment, it can also be useful to inspect what your `.gcloudignore` rules will upload:

```bash
gcloud meta list-files-for-upload
```

---

## 13. Secret Manager

List secrets:

```bash
gcloud secrets list
```

Create a secret:

```bash
gcloud secrets create SECRET_NAME \
  --replication-policy=automatic
```

Add a version from stdin:

```bash
printf '%s' 'secret-value' | \
  gcloud secrets versions add SECRET_NAME --data-file=-
```

Access the latest version:

```bash
gcloud secrets versions access latest \
  --secret=SECRET_NAME
```

In shell history and CI logs, be careful not to expose secrets just because a command makes it convenient to print them.

---

## 14. Cloud SQL

List instances:

```bash
gcloud sql instances list
```

Describe an instance:

```bash
gcloud sql instances describe INSTANCE_NAME
```

List databases:

```bash
gcloud sql databases list --instance=INSTANCE_NAME
```

List users:

```bash
gcloud sql users list --instance=INSTANCE_NAME
```

For creating or modifying production databases, check the current command help rather than copying an old set of flags:

```bash
gcloud sql instances create --help
```

Database defaults and supported flags are exactly the kind of thing you want to verify at execution time.

---

## 15. Logs: one of the most useful gcloud workflows

Read recent logs:

```bash
gcloud logging read \
  'severity>=ERROR' \
  --limit=50
```

Return JSON:

```bash
gcloud logging read \
  'severity>=ERROR' \
  --limit=50 \
  --format=json
```

Filter Cloud Run logs:

```bash
gcloud logging read \
  'resource.type="cloud_run_revision"' \
  --limit=50
```

The exact resource and log filters depend on the service, but `gcloud logging read` is worth learning because it lets you investigate from a terminal or script without switching to the console.

---

## 16. Filtering and formatting are where gcloud becomes really useful

This is the part many command lists skip.

A command that returns 500 resources is not very useful until you can narrow and shape the output.

### Filter

```bash
gcloud compute instances list \
  --filter="status=RUNNING"
```

Combine conditions:

```bash
gcloud compute instances list \
  --filter="status=RUNNING AND zone:us-central1"
```

### JSON

```bash
gcloud compute instances list --format=json
```

Great for scripts and tools such as `jq`.

### Value

```bash
gcloud config get-value project
```

Or:

```bash
gcloud run services describe SERVICE_NAME \
  --region=REGION \
  --format="value(status.url)"
```

This is ideal when a shell script needs exactly one value.

### Table

```bash
gcloud compute instances list \
  --format="table(name,zone,status)"
```

### CSV

```bash
gcloud compute instances list \
  --format="csv(name,zone,status)"
```

Once you learn `--filter` and `--format`, you stop treating `gcloud` as a collection of one-off terminal commands and start using it as an automation tool.

---

## 17. A safer way to use gcloud in scripts

A few habits make scripts easier to trust.

### Be explicit about project and location

```bash
gcloud run services list \
  --project=PROJECT_ID \
  --region=REGION
```

### Use machine-readable output

```bash
gcloud projects describe PROJECT_ID \
  --format=json
```

### Disable prompts when automation requires it

```bash
gcloud run services delete SERVICE_NAME \
  --region=REGION \
  --quiet
```

Do not add `--quiet` casually to destructive commands. In automation it is useful; interactively, the confirmation prompt can save you.

### Fail early in shell scripts

For Bash:

```bash
set -euo pipefail
```

Then check the exit status of commands that matter.

### Prefer impersonation over permanent key files

Where possible:

```bash
gcloud SOME_COMMAND \
  --impersonate-service-account=SERVICE_ACCOUNT_EMAIL
```

Short-lived credentials are easier to control than long-lived downloaded keys.

---

## 18. Troubleshooting gcloud itself

When something fails, start simple.

Check the version:

```bash
gcloud version
```

Check configuration:

```bash
gcloud config list
```

Check authentication:

```bash
gcloud auth list
```

Check environment information:

```bash
gcloud info
```

Increase logging:

```bash
gcloud SOME_COMMAND --verbosity=debug
```

For HTTP-level troubleshooting:

```bash
gcloud SOME_COMMAND --log-http
```

Be careful with verbose HTTP logs in shared terminals or CI systems because request and response data may contain information you do not want stored permanently.

---

## 19. A practical example: from terminal to Cloud Run

Here is a small flow that ties several commands together.

### Step 1: Sign in

```bash
gcloud auth login
```

### Step 2: Set the project

```bash
gcloud config set project PROJECT_ID
```

### Step 3: Confirm it

```bash
gcloud config get-value project
```

### Step 4: Enable the services you need

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 5: Deploy

```bash
gcloud run deploy SERVICE_NAME \
  --source=. \
  --region=REGION
```

### Step 6: Get the URL

```bash
gcloud run services describe SERVICE_NAME \
  --region=REGION \
  --format="value(status.url)"
```

### Step 7: Check the service

```bash
gcloud run services describe SERVICE_NAME \
  --region=REGION
```

### Step 8: Read recent logs if something is wrong

```bash
gcloud logging read \
  'resource.type="cloud_run_revision"' \
  --limit=50
```

That is the kind of workflow worth learning. You are not memorizing eight isolated commands. You are following the lifecycle of a real task.

---

## 20. What about the complete list of gcloud commands?

It does not belong in a normal blog article.

The CLI has a large and changing command tree, and Alpha/Beta commands move more often than GA commands.

So I keep the long list in GitHub instead:

**Complete gcloud command reference:**  
https://github.com/kloudxpert/blog/tree/main/gcloud-command-reference

The repository contains generated indexes for:

- GA commands
- Beta commands
- Alpha commands
- a shorter practical cheat sheet
- a regeneration script so the index can be refreshed against a newer Cloud SDK

That is a better fit than turning this page into thousands of lines of command names.

---

## 21. The commands I would actually memorize

If I had to reduce this whole guide to a small working set, it would be these:

```bash
gcloud auth login
gcloud auth list
gcloud config list
gcloud config set project PROJECT_ID
gcloud config configurations list
gcloud projects list
gcloud services list --enabled
gcloud services enable SERVICE_NAME
gcloud compute instances list
gcloud run services list
gcloud container clusters list
gcloud artifacts repositories list
gcloud secrets list
gcloud logging read FILTER
gcloud info
gcloud version
```

And one habit:

```bash
gcloud SOME_COMMAND --help
```

That habit is more useful than memorizing another hundred commands.

---

## Final thought

The best way to learn `gcloud` is not to read a giant command list from top to bottom.

Learn the shape of the CLI. Know which account and project you are using. Get comfortable with `--help`, `--filter`, and `--format`. Then learn commands as real problems give you a reason to use them.

Keep the complete reference nearby for the rest.

**GitHub command reference:**  
https://github.com/kloudxpert/blog/tree/main/gcloud-command-reference

**Official Google Cloud CLI reference:**  
https://cloud.google.com/sdk/gcloud/reference
