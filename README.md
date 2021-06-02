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
* `external_functions`: A dict of external functions to use in markdown. The
    dict's keys are the names under which the functions get loaded, and the value
    is a dictionary with the following key/values.
    * `file`: The path to the Python file to import from.
    * `name`: The name of the global function in `file` to import.

    So for example using
    ```
    ...,
    "external_functions": {
        "foo": {
            "file": "path/to/python/source.py",
            "name": "quux"
        }
    },
    ....
    ```
    will allow to use `{=foo(bar,baz)}` in markdown and would get replaced by
    the return value of running the global function `quux` from
    `path/to/python/source.py` with the parameters
    `(file_dict, state, ["bar", "baz"])`, where `file_dict` is the
    [file dict](#file) for the current file, and state is the current state for
    `ValueInjectorFileDecorator`.
* `macros`: A dict of macros. The keys are the macro names, and the values the
    substitution for the macro. In the macro value use:
    * `$1`, `$2`,… to refer to the first, second,… argument.
    * `$*` to refer to all arguments concatenated by `, `.
    * `\\n` to denote a line-break.

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
* `build_seconds_since_epoch`: The number of seconds passed since 1970-01-01
    until the build started.
* `build_day_iso`: The day when the build started, in ISO format.
* `build_git_description`: A description of the git repository when the build
    started.

## Data model

### Node

Each node is represented by a dictionary with the following key/values.

| key | creator | value |
| --- | ---     | ---   |
| `files` | DocumentNodeParser | A dictionary of [file dicts](#file). The keys are the file names (without path, without trailing `.md`. See [Node `files` keys](#node-files-keys) for more details) and the values are [file dicts](#file) for this language.
| `name` | DocumentNodeParser | The directory of this node |
| `subnodes` | DocumentNodeParser | The list of subnodes for this node ordered by the way they get rendered.|

### Node `files` keys

| key | creator | value |
| --- | ---     | ---   |
| (some language) | DocumentNodeParser | The file dict for this language |
| `default` | DefaultFileNodeDecorator | The file dict for the default language |


### File

Each file is represented by a dictionary with the following key/values.

| key | creator | value |
| --- | ---     | ---   |
| `content-properties` | Properties extracted from `raw-content` as string/string dictionary. |
| `file_name` | DocumentFileParser | The name of the file (with path) |
| `id` | IdDecorator | The `id` of the `default` file for this node.
| `is-default` | DefaultFileNodeDecorator | If present and `True`, this file represents the default file. This allows to detect the default file in `FileDecorator`s. |
| `key` | DocumentFileParser | The name (i.e.: language) of the file without the trailing `.md` |
| `level` | LevelDecorator | The depth in the node hierarchy of the node that this file belongs to. |
| `markdown` | MarkdownPropertyExtractorFileDecorator | The markdown part of `raw-content` as string. The `HeaderFileDecorator` adjusts the format of the first line. |
| `properties` | PropertyDecorator | A dictionary of properties for this file. This dictionary is seeded with the global properties (E.g.: `build_day_iso`). Then descending from the root node to the current node, each node updates (if necessary adds) properties. For each node, the following steps are taken. If the `properties.md` file exists for the node, its `content-properties` are added. Next, if the node has a file for the current language, its `content-properties` are added. If the node does not have a file for the current language, but has a file for the default language, the `content-properties` for the default language get added. Finally, `language` is set to the file's `key` |
| `raw-content` | DocumentFileParser | The raw file contents as string |


### Markdown mangling

A file's markdown gets mangled in a few ways.

1. Properties are cut off from the bottom of the contents. (See `MarkdownPropertyExtractorFileDecorator`)
1. Values are injected. (See the [Injected values section](#injected-values), and `ValueInjectorFileDecorator`)
1. The hierarchy level in the title is adjusted and the id is set (See `HeaderFileDecorator`)

#### Injected values

To inject a value into markdown, use `{=func(arg1,arg2, …)}`, where `func`
denotes the function to arrive at the injected values. Arguments `arg1`,
`arg2`,… have their wrapping whitespace stripped

| func | description |
| ---- | ---         |
| `property` | The property `arg1` from this file's properties gets injected |
| `macro` | The value of macro `arg1` (see [`macros` in `config.json`](#format-of-configjson) gets injected with args `(args2, args3,…)` as arguments. Note that `arg1` is the macro name, so `arg2` is the first argument to the macro, `arg3` the second, and so on. |
| `nodeTitle` | The title of the node with id `arg1` in the language `arg2` (or the language of the current file, if `arg2` is omitted). If the node does not have a title in that language, the title in the default language is used instead. |
| `substring` | All but the last two arguments get concatenated by `, `. And of that string, the substring `[argN:arg(N-1)]` is taken. So for example `{=substring(fooQUUXquuux, 3, 7)}` will inject `QUUX`. Both `argN` and `arg(N-1)` may be positive, negative, or missing and follow the usual conventions of Python's slice notation. This is especially useful to take substrings of arguments in macros.|
