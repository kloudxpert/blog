# KloudXpert gcloud Command Reference

A practical companion to the KloudXpert article **"gcloud Commands: A Practical Google Cloud CLI Guide for Engineers."**

This is not meant to be a dump of command names.

The generated reference reads the command tree from the installed Google Cloud CLI and then reads each command's built-in help text. Every command entry is written in this format:

    gcloud compute instances list
    What it does: Lists Compute Engine virtual machine instances.
    Usage help: gcloud compute instances list --help

That gives readers two levels of help:

- the **KloudXpert article** explains how to think about and use gcloud in real engineering work;
- the **GitHub reference** gives a searchable command-by-command index with a short explanation of what each command does.

## Browse

- [Practical gcloud cheat sheet](gcloud-command-reference/cheatsheets/practical-gcloud-cheatsheet.md)
- [Complete GA command reference](gcloud-command-reference/commands/gcloud-ga.md)
- [Complete Beta command reference](gcloud-command-reference/commands/gcloud-beta.md)
- [Complete Alpha command reference](gcloud-command-reference/commands/gcloud-alpha.md)
- [Complete Preview command reference](gcloud-command-reference/commands/gcloud-preview.md)
- [Full blog article draft](gcloud-command-reference/article/gcloud-commands-guide.md)
- [Reference generator](gcloud-command-reference/scripts/generate_gcloud_command_reference.py)

> The descriptions come from the built-in help of the same CLI release used to generate the command list. Run `gcloud COMMAND --help` for complete arguments, flags and examples.

## Release tracks

The Google Cloud CLI currently documents **GA, Beta, Alpha and Preview** release levels/components. The generator keeps those tracks separate so readers can see the stability level of the command they are looking at.

## Keeping the reference current

The GitHub Actions workflow in `.github/workflows/update-gcloud-reference.yml` installs the current CLI, installs the Alpha, Beta and Preview components, generates the command list, reads the help text for each command, and refreshes the Markdown reference automatically.

You can generate the reference locally too:

```bash
python gcloud-command-reference/scripts/generate_gcloud_command_reference.py
```

## Official references

- Google Cloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
- gcloud CLI overview: https://cloud.google.com/sdk/gcloud
- gcloud cheat sheet: https://cloud.google.com/sdk/docs/cheatsheet

Maintained for readers of [KloudXpert](https://blog.kloudxpert.com/).
