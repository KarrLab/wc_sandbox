""" Tests

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2019-02-08
:Copyright: 2019, Karr Lab
:License: MIT
"""

import unittest
import wc_sandbox


class VersionTestCase(unittest.TestCase):
    def test(self):
        self.assertIsInstance(wc_sandbox.__version__, str)
