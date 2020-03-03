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
import subprocess
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
        shutil.rmtree(os.path.expanduser('~/.wc/wc_sandbox/packages'))

        with __main__.App(argv=['install-packages']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with mock.patch('subprocess.check_call', return_value=None):
                    app.run()
                text = captured.stdout.get_text()
        self.assertIn('Installed packages', text)
        self.assertIn('- bpforms', text)

        with __main__.App(argv=['install-packages']) as app:
            with mock.patch('subprocess.check_call', return_value=None):
                app.run()

    def test_get_notebooks(self):
        if os.path.isdir(os.path.expanduser('~/.wc/wc_sandbox/notebooks')):
            shutil.rmtree(os.path.expanduser('~/.wc/wc_sandbox/notebooks'))

        with __main__.App(argv=['install-packages']) as app:
            with mock.patch('subprocess.check_call', return_value=None):
                app.run()

        with __main__.App(argv=['get-notebooks']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                app.run()
                text = captured.stdout.get_text()
        self.assertIn('Got notebooks', text)
        self.assertIn('- bpforms', text)
        self.assertTrue(os.path.isdir(os.path.expanduser('~/.wc/wc_sandbox/notebooks')))
        self.assertTrue(os.path.isdir(os.path.expanduser('~/.wc/wc_sandbox/notebooks/bpforms')))
        self.assertTrue(os.path.isfile(os.path.expanduser('~/.wc/wc_sandbox/notebooks/bpforms/1. Introductory tutorial.ipynb')))

        with __main__.App(argv=['get-notebooks']) as app:
            app.run()

    def test_start(self):
        class Popen(object):
            def __init__(self, returncode):
                self.returncode = returncode
                self.counter = 0

            def poll(self):
                self.counter += 1
                if self.counter < 3:
                    return None
                return 0

        with __main__.App(argv=['start', '--allow-root', '--port', '8888', '--no-browser']) as app:
            with mock.patch('subprocess.Popen', return_value=Popen(0)):
                app.run()

        with __main__.App(argv=['start', '--allow-root', '--port', '8888', '--no-browser']) as app:
            with self.assertRaises(Exception):
                with mock.patch('subprocess.Popen', return_value=Popen(1)):
                    app.run()
