import os

from .environment import DocumentPageTestCase
from document_generator import AllInOneExporter
from document_generator.decorators import ValueInjectorFileDecorator

FIXTURE_DIR = os.path.join('tests', 'fixtures', 'document-node-parser')


class AllInOneExporterTest(DocumentPageTestCase):
    def test_simple(self):
        node111 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'de': {
                    'markdown': 'fooDe',
                    'properties': {},
                    },
                'fr': {
                    'markdown': 'fooFr',
                    'properties': {},
                    },
            },
            'name': 'node111',
            'subnodes': [],
        }
        node11 = {
            'files': {},
            'name': 'node11',
            'subnodes': [node111],
        }
        node1 = {
            'files': {
                'en': {
                    'markdown': 'barEn',
                    'properties': {},
                    },
                'eo': {
                    'markdown': 'barEo',
                    'properties': {},
                    },
                'default': {
                    'markdown': 'barDefault',
                    'properties': {},
                    },
            },
            'name': 'node1',
            'subnodes': [node11],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', ['de'])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))
            self.assertStartsWith(contents, '<html')
            self.assertIn('fooEn', contents)
            self.assertIn('barEn', contents)
            self.assertEndsWith(contents, '</html>')

            contents = self.get_file_contents(os.path.join(dir, 'all.html.de'))
            self.assertStartsWith(contents, '<html')
            self.assertIn('fooDe', contents)
            self.assertIn('barEn', contents)
            self.assertEndsWith(contents, '</html>')

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            self.assertStartsWith(contents, 'barEn')
            self.assertEndsWith(contents, 'fooEn')

            contents = self.get_file_contents(os.path.join(dir, 'all.md.de'))
            self.assertStartsWith(contents, 'barEn')
            self.assertEndsWith(contents, 'fooDe')

    def test_template_header(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'default': {
                    'markdown': '',
                    'properties': {},
                    },
                },
            'name': 'node1',
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = 'HEADER'
            template_file = os.path.join(dir, 'template-header')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-header-file': template_file,
                }

            exporter = AllInOneExporter(node1, dir, 'en', [], conf)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, 'HEADER')
            self.assertIn('fooEn', contents)
            self.assertEndsWith(contents, '</html>')

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_template_footer(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'default': {
                    'markdown': '',
                    'properties': {},
                    },
                },
            'name': 'node1',
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = 'FOOTER'
            template_file = os.path.join(dir, 'template-footer')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-footer-file': template_file,
                }

            exporter = AllInOneExporter(node1, dir, 'en', [], conf)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, '<html')
            self.assertIn('fooEn', contents)
            self.assertEndsWith(contents, 'FOOTER')

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_template_file(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                'default': {
                    'markdown': 'fooEn',
                    'properties': {},
                    },
                },
            'name': 'node1',
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = '\n'.join([
                    'HEADER1',
                    'HEADER2',
                    '<!-- HEADER-END -->',
                    'OMITTED1',
                    'OMITTED2',
                    '<!-- FOOTER-START -->',
                    'FOOTER1',
                    'FOOTER2',
                    ])
            template_file = os.path.join(dir, 'template')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-template-file': template_file,
                }

            exporter = AllInOneExporter(node1, dir, 'en', [], conf)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, 'HEADER1')
            self.assertIn('HEADER2', contents)
            self.assertIn('fooEn', contents)
            self.assertIn('FOOTER1', contents)
            self.assertEndsWith(contents, 'FOOTER2')

            self.assertNotIn('OMITTED', contents)

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_properties(self):
        node1 = {
            'files': {
                'en': {
                    'markdown': 'fooEn',
                    'properties': {
                        'foo': 'bar',
                        },
                    },
                'default': {
                    'markdown': '',
                    'properties': {},
                    },
                },
            'name': 'node1',
            'subnodes': [],
            }

        with self.tempDir() as dir:
            template = '\n'.join([
                    'HEADER1{=property(foo)}',
                    'HEADER2',
                    '<!-- HEADER-END -->',
                    'OMITTED1',
                    'OMITTED2',
                    '<!-- FOOTER-START -->',
                    'FOOTER1{=property(foo)}',
                    'FOOTER2',
                    ])
            template_file = os.path.join(dir, 'template')
            with open(template_file, 'w+') as f:
                f.write(template)

            conf = {
                'html-template-file': template_file,
                }

            value_injector = ValueInjectorFileDecorator()
            value_injector_state = value_injector.init_state(node1)
            exporter = AllInOneExporter(
                node1, dir, 'en', [], conf, value_injector=value_injector,
                value_injector_state=value_injector_state)
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.html.en'))

            self.assertStartsWith(contents, 'HEADER1bar')
            self.assertIn('HEADER2', contents)
            self.assertIn('fooEn', contents)
            self.assertIn('FOOTER1bar', contents)
            self.assertEndsWith(contents, 'FOOTER2')

            self.assertNotIn('OMITTED', contents)

            self.assertFileContents(os.path.join(dir, 'all.md.en'), 'fooEn')

    def test_sorting_default_key(self):
        node11 = {
            'files': {'en': {'markdown': 'NODE11', 'properties': {}}},
            'name': 'Z',
            'subnodes': [],
        }
        node12 = {
            'files': {'en': {'markdown': 'NODE12', 'properties': {}}},
            'name': 'A',
            'subnodes': [],
        }
        node13 = {
            'files': {'en': {'markdown': 'NODE13', 'properties': {}}},
            'name': 'b',
            'subnodes': [],
        }
        node1 = {
            'files': {
                'en': {'markdown': 'RootEn', 'properties': {}},
                'default': {'markdown': 'RootDefault', 'properties': {}},
                },
            'name': 'node1',
            'subnodes': [node11, node12, node13],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', [])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            self.assertIn('RootEn\n\nNODE12\n\nNODE13\n\nNODE11', contents)

    def test_sorting_fixed_key(self):
        node11 = {
            'files': {'en': {'markdown': 'NODE11', 'properties': {
                        'sort-key': 'Z'}}},
            'name': 'node11',
            'subnodes': [],
        }
        node12 = {
            'files': {'en': {'markdown': 'NODE12', 'properties': {
                        'sort-key': 'A'}}},
            'name': 'node12',
            'subnodes': [],
        }
        node13 = {
            'files': {'en': {'markdown': 'NODE13', 'properties': {
                        'sort-key': 'b'}}},
            'name': 'node13',
            'subnodes': [],
        }
        node1 = {
            'files': {
                'en': {'markdown': 'RootEn', 'properties': {}},
                'default': {'markdown': 'RootDefault', 'properties': {}},
                },
            'name': 'node1',
            'subnodes': [node11, node12, node13],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', [])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            # NODE11 before NODE13 as keys are compared case sensitive
            self.assertIn('RootEn\n\nNODE12\n\nNODE11\n\nNODE13', contents)

    def test_sorting_node_dir_name(self):
        node11 = {
            'files': {'en': {'markdown': 'NODE11', 'properties': {
                        'sort-key': '{node-dir-name}'}}},
            'name': 'Z',
            'subnodes': [],
        }
        node12 = {
            'files': {'en': {'markdown': 'NODE12', 'properties': {
                        'sort-key': '{node-dir-name}'}}},
            'name': 'A',
            'subnodes': [],
        }
        node13 = {
            'files': {'en': {'markdown': 'NODE13', 'properties': {
                        'sort-key': '{node-dir-name}'}}},
            'name': 'b',
            'subnodes': [],
        }
        node1 = {
            'files': {
                'en': {'markdown': 'RootEn', 'properties': {}},
                'default': {'markdown': 'RootDefault', 'properties': {}},
                },
            'name': 'node1',
            'subnodes': [node11, node12, node13],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', [])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            self.assertIn('RootEn\n\nNODE12\n\nNODE13\n\nNODE11', contents)

    def test_sorting_title(self):
        node11 = {
            'files': {'en': {'markdown': 'NODE11', 'properties': {
                        'sort-key': '{title}'}}},
            'name': 'Z',
            'subnodes': [],
        }
        node12 = {
            'files': {'en': {'markdown': '## NODE12', 'properties': {
                        'sort-key': '{title}'}}},
            'name': 'A',
            'subnodes': [],
        }
        node13 = {
            'files': {'en': {'markdown': 'NODE13', 'properties': {
                        'sort-key': '{title}'}}},
            'name': 'b',
            'subnodes': [],
        }
        node1 = {
            'files': {
                'en': {'markdown': 'RootEn', 'properties': {}},
                'default': {'markdown': 'RootDefault', 'properties': {}},
                },
            'name': 'node1',
            'subnodes': [node11, node12, node13],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', [])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            self.assertIn('RootEn\n\nNODE11\n\n## NODE12\n\nNODE13', contents)

    def test_sorting_mixed(self):
        node11 = {
            'files': {'en': {'markdown': 'NODE11', 'properties': {
                        'sort-key': '{node-dir-name}'}}},
            'name': 'Z',
            'subnodes': [],
        }
        node12 = {
            'files': {'en': {'markdown': 'NODE12', 'properties': {
                        'sort-key': '{title}'}}},
            'name': 'A',
            'subnodes': [],
        }
        node13 = {
            'files': {'en': {'markdown': 'NODE13', 'properties': {
                        'sort-key': 'B'}}},
            'name': 'M',
            'subnodes': [],
        }
        node1 = {
            'files': {
                'en': {'markdown': 'RootEn', 'properties': {}},
                'default': {'markdown': 'RootDefault', 'properties': {}},
                },
            'name': 'node1',
            'subnodes': [node11, node12, node13],
        }
        with self.tempDir() as dir:
            exporter = AllInOneExporter(node1, dir, 'en', [])
            exporter.export()

            contents = self.get_file_contents(os.path.join(dir, 'all.md.en'))
            self.assertIn('RootEn\n\nNODE13\n\nNODE12\n\nNODE11', contents)
