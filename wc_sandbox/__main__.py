""" wc_sandbox command line interface

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2019-02-08
:Copyright: 2019, Karr Lab
:License: MIT
"""

import cement
import os
import subprocess
import time
import wc_sandbox


class BaseController(cement.Controller):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        description = "wc-sandbox"
        arguments = [
            (['-v', '--version'], dict(action='version', version=wc_sandbox.__version__)),
        ]

    @cement.ex(hide=True)
    def _default(self):
        raise SystemExit(self._parser.print_help())


class StartController(cement.Controller):
    """ Start server """

    class Meta:
        label = 'start'
        description = 'Start server'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['--no-browser'], dict(action='store_true', default=False,
                                    help='Do not open server in web browser')),
            (['--port'], dict(type=int, default=None, help='Port')),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs

        options = []
        if args.port:
            options.append('--port=' + str(args.port))
        if args.no_browser:
            options.append('--no-browser')

        process = subprocess.Popen(['jupyter', 'notebook',
                                    '--notebook-dir=wc_sandbox/notebooks',
                                    '--ip=*',
                                    ] + options)
        time.sleep(5.)
        print('Server started')


class StopController(cement.Controller):
    """ Stop server """

    class Meta:
        label = 'stop'
        description = 'Stop server'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
        ]

    @cement.ex(hide=True)
    def _default(self):
        process = subprocess.Popen(['jupyter', 'notebook', 'stop'], stdout=subprocess.PIPE)
        time.sleep(2.)
        print('Server stopped')


class App(cement.App):
    """ Command line application """
    class Meta:
        label = 'wc-sandbox'
        base_controller = 'base'
        handlers = [
            BaseController,
            StartController,
            StopController,
        ]


def main():
    with App() as app:
        app.run()
