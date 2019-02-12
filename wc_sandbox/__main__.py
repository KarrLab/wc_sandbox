""" wc_sandbox command line interface

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2019-02-08
:Copyright: 2019, Karr Lab
:License: MIT
"""

import cement
import importlib
import os
import pip._internal
import shutil
import subprocess
import time
import wc_sandbox
import wc_sandbox.config.core


PACKAGES = (
    'bpforms',
    'wc_rules',
)


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


class InstallPackages(cement.Controller):
    """ Install WC packages """

    class Meta:
        label = 'install-packages'
        description = 'Install packages'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
        ]

    @cement.ex(hide=True)
    def _default(self):
        config = wc_sandbox.config.core.get_config()
        package_ids = config['wc_sandbox']['packages'].keys()
        for package_id in package_ids:
            pip._internal.main([
                'install',
                '-U',
                '--process-dependency-links',
                'git+https://github.com/KarrLab/{0}.git#egg={0}'.format(package_id)])

        print('Installed packages:\n- {}'.format('\n- '.join(sorted(package_ids))))


class GetNotebooks(cement.Controller):
    """ Get notebooks from WC packages """

    class Meta:
        label = 'get-notebooks'
        description = 'Get notebooks'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
        ]

    @cement.ex(hide=True)
    def _default(self):
        config = wc_sandbox.config.core.get_config()

        notebooks_dir = config['wc_sandbox']['notebooks_dir']
        if os.path.isdir(notebooks_dir):
            shutil.rmtree(notebooks_dir)
        os.makedirs(notebooks_dir)

        package_ids = config['wc_sandbox']['packages'].keys()
        for package_id in package_ids:
            package = importlib.import_module(package_id)
            src_dir = os.path.join(os.path.dirname(package.__file__), '..', 'examples')

            dest_dir = os.path.join(notebooks_dir, package_id)
            shutil.copytree(src_dir, dest_dir)

        print('Got notebooks for:\n- {}'.format('\n- '.join(sorted(package_ids))))


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

        config = wc_sandbox.config.core.get_config()
        notebooks_dir = config['wc_sandbox']['notebooks_dir']
        process = subprocess.Popen(['jupyter', 'notebook',
                                    '--notebook-dir=' + notebooks_dir,
                                    '--ip=*',
                                    '--NotebookApp.password=',
                                    '--NotebookApp.password_required=False',
                                    '--NotebookApp.allow_password_change=False',
                                    '--NotebookApp.token=',
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
            InstallPackages,
            GetNotebooks,
            StartController,
            StopController,
        ]


def main():
    with App() as app:
        app.run()
