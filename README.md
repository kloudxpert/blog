# KloudXpert gcloud Command Reference

A practical companion to the KloudXpert article **"gcloud Commands: A Practical Google Cloud CLI Guide for Engineers."**

This repository keeps the long command inventory outside the article so the article stays readable and the reference can be refreshed as the Google Cloud CLI changes.

## Browse

- [Practical gcloud cheat sheet](gcloud-command-reference/cheatsheets/practical-gcloud-cheatsheet.md)
- [Complete GA command index](gcloud-command-reference/commands/gcloud-ga.md)
- [Complete Beta command index](gcloud-command-reference/commands/gcloud-beta.md)
- [Complete Alpha command index](gcloud-command-reference/commands/gcloud-alpha.md)
- [Blog article draft](gcloud-command-reference/article/gcloud-commands-guide.md)
- [Generator script](gcloud-command-reference/scripts/generate_gcloud_command_reference.py)

> The command indexes are generated snapshots, not a replacement for command-specific help. Run `gcloud COMMAND --help` for the exact CLI version installed on your machine.

## Why only GA, Beta and Alpha?

The gcloud CLI uses **GA, beta and alpha command tracks**. A Google Cloud product or feature might separately be described as Preview, but there is no general `gcloud preview ...` release track comparable to `gcloud beta ...` or `gcloud alpha ...`.

## Keeping the command list current

The workflow in `.github/workflows/update-gcloud-reference.yml` installs the current Google Cloud CLI, installs the Alpha and Beta components, and regenerates the indexes automatically.

You can also generate them locally:

```bash
python gcloud-command-reference/scripts/generate_gcloud_command_reference.py
```

The generator uses:

```bash
gcloud meta list-commands
```

so the inventory reflects the command tree available in the installed CLI.

## Official references

- Google Cloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
- gcloud command conventions: https://cloud.google.com/sdk/gcloud/reference/topic/command-conventions
- gcloud cheat sheet: https://cloud.google.com/sdk/docs/cheatsheet

Maintained for readers of [KloudXpert](https://blog.kloudxpert.com/).
