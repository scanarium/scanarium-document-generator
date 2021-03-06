#!/usr/bin/env python3

import argparse
import collections.abc
import json
import os
import sys

import document_generator


def parse_arguments(conf):
    parser = argparse.ArgumentParser(
        description='Generates documents from markdown')
    parser.add_argument(
        '--config',
        help='The name of a json file to load the configuration from'
        ' (default: None)')
    parser.add_argument(
        '--config-override',
        help='Overrides configuration settings. Each `CONFIG_OVERRIDE` has to '
        'be of the form `key.subkey.value...=subsubkey` (default: None)',
        nargs='+', default=[])
    parser.add_argument(
        '--source',
        help='The source directory for the help content'
        f' (default: {conf["source"]})')
    parser.add_argument(
        '--debug',
        help='If `yes`, enable debug mode (default: `no`)')
    parser.add_argument(
        '--target',
        help='The target directory in which to store the generated help files'
        f' (default: {conf["target"]})')
    parser.add_argument(
        '--default-localization',
        help='The default localization'
        f' (default: {conf["default_l10n"]})')
    parser.add_argument(
        '--additional-localizations',
        help='comma separated list of additional localizations to generate'
        f' (default: {conf["additional_l10ns"]})')

    return parser.parse_args()


def object_string_replace(obj, needle, replacement):
    if isinstance(obj, collections.abc.Mapping):
        ret = {}
        for key, value in obj.items():
            ret[key] = object_string_replace(value, needle, replacement)
    elif isinstance(obj, list):
        ret = [object_string_replace(x, needle, replacement) for x in obj]
    elif isinstance(obj, str):
        ret = obj.replace(needle, replacement)
    else:
        ret = obj
    return ret


def conf_to_boolean(string):
    return string and string.lower() in ['yes', 'y', 'true', 't']


if __name__ == "__main__":
    conf = {
        'source': '.',
        'target': 'output',
        'default_l10n': 'en',
        'additional_l10ns': '',
        'debug': 'no',
    }
    utils = document_generator.Utils()

    args = parse_arguments(conf)
    if args.config is not None:
        with open(args.config, 'rt') as f:
            config_text_content = f.read()
        extra_config = json.loads(config_text_content)
        conf = utils.update_dict(conf, extra_config)

        conf_dir = os.path.dirname(os.path.abspath(args.config))
        conf = object_string_replace(conf, '{conf_dir}', conf_dir)

    for field, value in [
        ['source', args.source],
        ['target', args.target],
        ['default_l10n', args.default_localization],
        ['additional_l10ns', args.additional_localizations],
        ['debug', args.debug],
    ]:
        if value is not None:
            conf[field] = value

    for config_override in args.config_override:
        d = conf
        dot_parts = config_override.split('.')
        for dot_part in dot_parts[:-1]:
            d = conf[dot_part.strip()]
        key, value = [x.strip() for x in dot_parts[-1].split('=', 1)]
        d[key] = value

    if not isinstance(conf['additional_l10ns'], list):
        if conf['additional_l10ns'].strip():
            conf['additional_l10ns'] = [
                x.strip() for x in conf['additional_l10ns'].split(',')]
        else:
            conf['additional_l10ns'] = []

    for key in [
                'debug'
            ]:
        conf[key] = conf_to_boolean(conf[key])

    generator = document_generator.DocumentGenerator()
    errors = generator.run(conf)

    exit_code = 1 if errors else 0
    sys.exit(exit_code)
