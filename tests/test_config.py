""" Tests of config module

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2019-02-12
:Copyright: 2019, Karr Lab
:License: MIT
"""

import os.path
import unittest
import wc_sandbox.config.core


class ConfigTestCase(unittest.TestCase):
    def test_get_config(self):
        config = wc_sandbox.config.core.get_config()
        self.assertEqual(config['wc_sandbox']['notebooks_dir'],
                         os.path.expanduser('~/.wc/wc_sandbox/notebooks'))
        self.assertIn('bpforms', config['wc_sandbox']['packages'].keys())
