# KloudXpert gcloud Command Reference

A practical companion to the KloudXpert article **"gcloud Commands: A Practical Google Cloud CLI Guide for Engineers."**

This repository keeps two things separate:

- **The article** explains how to use `gcloud` in real work.
- **The command index** is generated from the installed Google Cloud CLI so it can be refreshed as the CLI changes.

## Browse

- [Practical gcloud cheat sheet](gcloud-command-reference/cheatsheets/practical-gcloud-cheatsheet.md)
- [Complete GA command index](gcloud-command-reference/commands/gcloud-ga.md)
- [Complete Beta command index](gcloud-command-reference/commands/gcloud-beta.md)
- [Complete Alpha command index](gcloud-command-reference/commands/gcloud-alpha.md)
- [Complete Preview command index](gcloud-command-reference/commands/gcloud-preview.md)
- [Blog article draft](gcloud-command-reference/article/gcloud-commands-guide.md)

> The generated indexes are snapshots, not a substitute for command-specific help. Run `gcloud COMMAND --help` for the version installed on your machine.

## Keeping the command list current

The workflow in `.github/workflows/update-gcloud-reference.yml` installs the current Google Cloud CLI, installs the Alpha/Beta/Preview components when available, and regenerates the indexes.

You can also generate them locally:

```bash
python gcloud-command-reference/scripts/generate_gcloud_command_reference.py
```

## Official references

- Google Cloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
- gcloud command conventions: https://cloud.google.com/sdk/gcloud/reference/topic/command-conventions
- gcloud cheat sheet: https://cloud.google.com/sdk/docs/cheatsheet

Maintained for readers of [KloudXpert](https://blog.kloudxpert.com/).
