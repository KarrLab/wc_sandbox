""" Configuration

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2019-01-06
:Copyright: 2017-2019, Karr Lab
:License: MIT
"""

import configobj
import os
import pathlib
import pkg_resources
import wc_utils.config


def get_config(extra=None):
    """ Get configuration

    Args:
        extra (:obj:`dict`, optional): additional configuration to override

    Returns:
        :obj:`configobj.ConfigObj`: nested dictionary with the configuration settings loaded from the configuration source(s).
    """
    paths = wc_utils.config.ConfigPaths(
        default=pkg_resources.resource_filename('wc_sandbox', 'config/core.default.cfg'),
        schema=pkg_resources.resource_filename('wc_sandbox', 'config/core.schema.cfg'),
        user=(
            'wc_sandbox.cfg',
            os.path.expanduser('~/.wc/wc_sandbox.cfg'),
        ),
    )

    context = {
        'HOME': str(pathlib.Path.home()),
    }

    return wc_utils.config.ConfigManager(paths).get_config(extra=extra, context=context)
