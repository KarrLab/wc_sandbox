""" Tests of wc_sandbox command line interface (wc_sandbox.__main__)

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2019-01-31
:Copyright: 2019, Karr Lab
:License: MIT
"""

from wc_sandbox import __main__
import wc_sandbox
import capturer
import mock
import os.path
import shutil
import time
import unittest


class CliTestCase(unittest.TestCase):
    def test_cli(self):
        with mock.patch('sys.argv', ['wc_sandbox', '--help']):
            with self.assertRaises(SystemExit) as context:
                __main__.main()
                self.assertRegex(context.Exception, 'usage: wc_sandbox')

    def test_help(self):
        with self.assertRaises(SystemExit):
            with __main__.App(argv=[]) as app:
                app.run()

        with self.assertRaises(SystemExit):
            with __main__.App(argv=['--help']) as app:
                app.run()

    def test_version(self):
        with __main__.App(argv=['-v']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with self.assertRaises(SystemExit):
                    app.run()
                self.assertEqual(captured.stdout.get_text(), wc_sandbox.__version__)
                self.assertEqual(captured.stderr.get_text(), '')

        with __main__.App(argv=['--version']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with self.assertRaises(SystemExit):
                    app.run()
                self.assertEqual(captured.stdout.get_text(), wc_sandbox.__version__)
                self.assertEqual(captured.stderr.get_text(), '')

    def test_install_packages(self):
        with __main__.App(argv=['install-packages']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                app.run()
                text = captured.stdout.get_text()
        self.assertIn('Installed packages', text)
        self.assertIn('- bpforms', text)

    def test_get_notebooks(self):
        if os.path.isdir(os.path.expanduser('~/.wc/notebooks')):
            shutil.rmtree(os.path.expanduser('~/.wc/notebooks'))

        with __main__.App(argv=['get-notebooks']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                app.run()
                text = captured.stdout.get_text()

        self.assertIn('Got notebooks', text)
        self.assertIn('- bpforms', text)
        self.assertTrue(os.path.isdir(os.path.expanduser('~/.wc/notebooks')))
        self.assertTrue(os.path.isdir(os.path.expanduser('~/.wc/notebooks/bpforms')))
        self.assertTrue(os.path.isfile(os.path.expanduser('~/.wc/notebooks/bpforms/Tutorial.ipynb')))

    def test_start_stop(self):
        with __main__.App(argv=['start', '--port', '8888', '--no-browser']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                app.run()
                text = captured.stdout.get_text()
                self.assertIn('Server started', text)

        with __main__.App(argv=['stop']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                app.run()
                text = captured.stdout.get_text()
                self.assertIn('Server stopped', text)
