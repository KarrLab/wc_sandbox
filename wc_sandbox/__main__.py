""" wc_sandbox command line interface

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2019-02-08
:Copyright: 2019, Karr Lab
:License: MIT
"""

import cement
import git
import importlib
import os
import pip._internal
import shutil
import subprocess
import sys
import time
import wc_sandbox
import wc_sandbox.config.core


class BaseController(cement.Controller):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        description = "Jupyter server for interactive whole-cell modeling tutorials"
        help = "Jupyter server for interactive whole-cell modeling tutorials"
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
        help = 'Install packages'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
        ]

    @cement.ex(hide=True)
    def _default(self):
        config = wc_sandbox.config.core.get_config()
        package_ids = config['wc_sandbox']['packages'].keys()
        packages_dir = config['wc_sandbox']['packages_dir']

        if not os.path.isdir(packages_dir):
            os.makedirs(packages_dir)
        for package_id in package_ids:
            package_path = os.path.join(packages_dir, package_id)
            if os.path.isdir(package_path):
                repo = git.Repo(path=package_path)
                repo.remotes['origin'].pull()
            else:
                git.Repo.clone_from('https://github.com/KarrLab/{}.git'.format(package_id), package_path)

            py_v = '{}.{}'.format(sys.version_info[0], sys.version_info[1])
            
            cmd = ['pip' + py_v, 'install', '-r', os.path.join(package_path, '.circleci', 'requirements.txt')]
            subprocess.check_call(cmd)

            cmd = ['pip' + py_v, 'install', '-e', package_path]
            subprocess.check_call(cmd)

        print('Installed packages:\n- {}'.format('\n- '.join(sorted(package_ids))))


class GetNotebooks(cement.Controller):
    """ Get notebooks from WC packages """

    class Meta:
        label = 'get-notebooks'
        description = 'Get notebooks'
        help = 'Get notebooks'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
        ]

    @cement.ex(hide=True)
    def _default(self):
        config = wc_sandbox.config.core.get_config()
        package_ids = config['wc_sandbox']['packages'].keys()
        packages_dir = config['wc_sandbox']['packages_dir']
        notebooks_dir = config['wc_sandbox']['notebooks_dir']

        if os.path.isdir(notebooks_dir):
            shutil.rmtree(notebooks_dir)
        os.makedirs(notebooks_dir)

        for package_id in package_ids:
            src_dir = os.path.join(packages_dir, package_id, 'examples')
            if os.path.isdir(src_dir):
                dest_dir = os.path.join(notebooks_dir, package_id)
                shutil.copytree(src_dir, dest_dir)

        print('Got notebooks for:\n- {}'.format('\n- '.join(sorted(package_ids))))


class StartController(cement.Controller):
    """ Start server """

    class Meta:
        label = 'start'
        description = 'Start server'
        help = 'Start server'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['--allow-root'], dict(action='store_true', default=False,
                                    help='Allow the notebook to be run from root user.')),
            (['--ip'], dict(type=str, default='*', help='IP address the notebook server will listen on.')),
            (['--port'], dict(type=int, default=None, help='Port the notebook server will listen on.')),
            (['--no-browser'], dict(action='store_true', default=False,
                                    help="Don't open the notebook in a browser after startup.")),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs

        options = []
        if args.allow_root:
            options.append('--allow-root')
        if args.ip:
            options.append('--ip=' + args.ip)
        if args.port:
            options.append('--port=' + str(args.port))
        if args.no_browser:
            options.append('--no-browser')

        config = wc_sandbox.config.core.get_config()
        notebooks_dir = config['wc_sandbox']['notebooks_dir']
        process = subprocess.Popen(['jupyter', 'notebook',
                                    '--notebook-dir=' + notebooks_dir,
                                    '--NotebookApp.password=',
                                    '--NotebookApp.password_required=False',
                                    '--NotebookApp.allow_password_change=False',
                                    '--NotebookApp.token=',
                                    ] + options)
        while process.poll() is None:
            time.sleep(0.1)
        if process.returncode != 0:
            raise Exception('Error starting jupyter server')


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
        ]


def main():
    with App() as app:
        app.run()
