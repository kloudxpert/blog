# KloudXpert gcloud Command Reference

Companion command indexes, a practical cheat sheet, and a regeneration script for the [gcloud Commands guide](https://blog.kloudxpert.com/gcloud-commands-guide/).

**Read the tutorial on the KloudXpert blog.** This repository holds supporting reference material, not a second copy of the article.

## Browse the reference

- [Reference home](gcloud-command-reference/README.md)
- [Practical cheat sheet](gcloud-command-reference/cheatsheets/practical-gcloud-cheatsheet.md)
- [GA command index](gcloud-command-reference/commands/gcloud-ga.md)
- [Beta command index](gcloud-command-reference/commands/gcloud-beta.md)
- [Alpha command index](gcloud-command-reference/commands/gcloud-alpha.md)
- [Reference generator](gcloud-command-reference/scripts/generate_gcloud_command_reference.py)

## What is available now

The checked-in indexes are a snapshot of the Google Cloud CLI command tree from **Google Cloud SDK 568.0.0**, generated on **2026-09-22**. They list command and group names; they do not currently include per-command descriptions. Use `gcloud COMMAND --help` for arguments, explanations, and examples.

The generator supports collecting built-in help summaries for a future refresh. That is separate from the content currently committed here. Preview output is not currently included.

## Refreshing the reference

The existing GitHub Actions workflow supports scheduled and manual generation. To run the generator locally with the Google Cloud CLI installed:

```bash
python gcloud-command-reference/scripts/generate_gcloud_command_reference.py
```

Check generated files and workflow results before relying on a new snapshot. This reference does not guarantee every command available in future CLI releases.

## Official documentation

- [Google Cloud CLI reference](https://cloud.google.com/sdk/gcloud/reference)
- [Google Cloud CLI cheat sheet](https://cloud.google.com/sdk/docs/cheatsheet)

Maintained for readers of [KloudXpert](https://blog.kloudxpert.com/gcloud-commands-guide/). Google Cloud is a trademark of Google LLC; this is an independent resource.
