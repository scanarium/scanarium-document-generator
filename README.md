# Scanarium Document Generator

This repo contains the scripts/code needed to generate Scanarium
documentation. For the actual documentation content, see the other Scanarium
repos, e.g.: https://github.com/scanarium/scanarium-handbook contains the
content for the „Scanarium Handbook”.

## Usage

1. Clone this repo and a content_repo.
1. `$PATH_TO_THIS_REPO/generator.py --config "$PATH_TO_CONTENT_REPO/config.json" --target foo`
1. Done. The generated document(s) can be found in the directory `foo`

## Format of `config.json`

A content repo's `config.json` is a JSON dictionary with the following key/values:
* `source`: the directory for the markdown files. (Default: `.`)
* `target`: the directory to store the generated files in. (Default: `output`)
* `default_l10n`: The default localization to use. (Default: `en`)
* `additional_l10ns`: A list of localizations to build in addition to the
    `default_l10n`. (Default: `[]`)
* `resources`: A list of directories to copy into the target directory.
    (Default: [])
* `exporter`: A dict of settings for exporters. (Default: {}) The following
    key/values are supported:
    * `html-footer-file`: If set, the contents of this file are used as footer
        for html files. (Default: None)
    * `html-header-file`: If set, the contents of this file are used as header
        for html files. (Default: None)
    * `html-template-file`: If set, the contents of this file up to a line
        `<!-- HEADER-END -->` is used as header, and contents belowe a line
        `<!-- FOOTER-START -->` are used as footer. (Default: None)

Directories are relative to the current working directory. E.g.: If the
generator is started from directory `.../foo`, the config file is
`.../bar/config.json` and `target` is set to `baz`, then the documentation will
get written to `.../foo/baz`.

In all string values, `{conf_dir}` gets replaced with the absolute name of the
directory containing the `config.json` file. This allows formulate `source` etc
relative to this directory (e.g.: `{conf_dir}/markdown`).

## Writing documents

A document is written as a collection of Markdown files.

A document is a hierarchy nodes (think: Chapter of a book, or item in a FAQ),
starting at a single root node. Each node can (but need not) have content (text,
images) in multiple languages. And each node can (but need not) have subnodes
(which are regular nodes again).

In the file system, a node is a directory. The name of the directory only serves
to give document authors a clue and gets used for sorting, but the name is
otherwise not important.

Files in that directory that end in `.md` are considered content in the file
name's language. E.g.: `en.md` holds the English content for this node, `de.md`
the German content. If a directory has a `.md` file, it (also) needs to have a
`.md` file for the default language. If the `.md` file for an additional
language is missing, content from the default language is substituted.

Each sub-directory is considered a sub-node. Sub-nodes are used in alphabetic
order, so one can prefix them with zero-left-padded numbers to control the sort
order. E.g.: `01-foo`, `02-bar`, ... .

### Format of content Markdown files

The content files of a node are plain Markdown, with optional properties at the
bottom of the file. Property lines are lines of the format `key:value` and they
are parsed and stripped from the file before rendering the file. The property
`key`s can only contain lowercase, latin letters and dashes (`-`).

Common properties are:

* `id`: This value gets used as `id` attribute this node to in HTML. This allows
    to format stable anchors in HTML. It suffices to set `id` in the default
    language. Other languages inhert it from there.
* `version`: A number that describes the version of the content. For updates
    that change the content, increase this number, so tooling can identify that
    translations of the content need to get updated as well. For typo fixes,
    increase the number's decimal places, so tooling can see that translations
    do not need to get updated. If a file is missing the `version` tag, it is
    assumed to be `1`.
