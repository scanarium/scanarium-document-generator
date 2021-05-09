#!/usr/bin/env python3

import argparse
import collections.abc
import json

import help_generator


def parse_arguments(conf):
    parser = argparse.ArgumentParser(
        description='Generates help pages from markdown')
    parser.add_argument(
        '--config',
        help='The name of a json file to load the configuration from'
        ' (default: None)')
    parser.add_argument(
        '--source',
        help='The source directory for the help content'
        f' (default: {conf["source"]})')
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


def update_dict(target, source, merge_lists=False):
    for key, value in source.items():
        if isinstance(value, collections.abc.Mapping):
            repl = update_dict(target.get(key, {}), value)
            target[key] = repl
        elif merge_lists and isinstance(value, list) \
                and isinstance(target.get(key, 0), list):
            target[key] += value
        else:
            target[key] = source[key]
    return target

if __name__ == "__main__":
    conf = {
        'source': '.',
        'target': 'output',
        'default_l10n': 'en',
        'additional_l10ns': '',
    }

    args = parse_arguments(conf)

    if args.config is not None:
        with open(args.config, 'rt') as f:
            config_text_content = f.read()
        extra_config = json.loads(config_text_content)
        conf = update_dict(conf, extra_config)

    for field, value in [
        ['source', args.source],
        ['target', args.target],
        ['default_l10n', args.default_localization],
        ['additional_l10ns', args.additional_localizations],
    ]:
        if value is not None:
            conf[field] = value

    if not isinstance(conf['additional_l10ns'], list):
        if conf['additional_l10ns'].strip():
            conf['additional_l10ns'] = [
                x.strip() for x in conf['additional_l10ns'].split(',')]
        else:
            conf['additional_l10ns'] = []

    generator = help_generator.HelpGenerator()
    generator.run(conf)
