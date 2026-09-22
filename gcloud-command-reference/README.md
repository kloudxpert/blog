# gcloud Command Reference

Read the explanation and practical workflows in the [KloudXpert gcloud Commands guide](https://blog.kloudxpert.com/gcloud-commands-guide/).

Use this folder when you need a quick lookup:

| Resource | Purpose |
| --- | --- |
| [Practical cheat sheet](cheatsheets/practical-gcloud-cheatsheet.md) | Common commands organized by task |
| [GA index](commands/gcloud-ga.md) | Generally available command and group names |
| [Beta index](commands/gcloud-beta.md) | Beta command and group names |
| [Alpha index](commands/gcloud-alpha.md) | Alpha command and group names |
| [Snapshot details](commands/README.md) | CLI version, generation date, and entry counts |
| [Generator](scripts/generate_gcloud_command_reference.py) | Script for refreshing the reference |

The current indexes list names. For a command's description and syntax, run:

```bash
gcloud compute instances list --help
```

The reference is a versioned snapshot, not a substitute for current [official documentation](https://cloud.google.com/sdk/gcloud/reference). The tutorial itself lives on the blog.
