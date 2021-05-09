#!/usr/bin/env python3

import argparse

import help_generator


def parse_arguments(conf):
    parser = argparse.ArgumentParser(
        description='Generates help pages from markdown')
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
        '--additional-localizations', default='',
        help='comma separated list of additional localizations to generate'
        f' (default: {conf["additional_l10ns"]})')

    return parser.parse_args()


if __name__ == "__main__":
    conf = {
        'source': '.',
        'target': 'output',
        'default_l10n': 'en',
        'additional_l10ns': '',
    }
    args = parse_arguments(conf)

    for field, value in [
        ['source', args.source],
        ['target', args.target],
        ['default_l10n', args.default_localization],
        ['additional_l10ns', args.additional_localizations],
    ]:
        if value is not None:
            conf[field] = value

    if conf['additional_l10ns'].strip():
        conf['additional_l10ns'] = [
            x.strip() for x in conf['additional_l10ns'].split(',')]
    else:
        conf['additional_l10ns'] = []

    generator = help_generator.HelpGenerator()
    generator.run(conf['source'], conf['target'], conf['default_l10n'],
                  conf['additional_l10ns'])
