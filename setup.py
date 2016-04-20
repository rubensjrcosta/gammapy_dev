#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
import sys

import ah_bootstrap
from setuptools import setup

# A dirty hack to get around some early import/configurations ambiguities
if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins
builtins._ASTROPY_SETUP_ = True

from astropy_helpers.setup_helpers import (
    register_commands, get_debug_option, get_package_info)
from astropy_helpers.git_helpers import get_git_devstr
from astropy_helpers.version_helpers import generate_version_py

# Get some values from the setup.cfg
from distutils import config
conf = config.ConfigParser()
conf.read(['setup.cfg'])
metadata = dict(conf.items('metadata'))

PACKAGENAME = metadata.get('package_name', 'packagename')
DESCRIPTION = metadata.get('description', 'Astropy affiliated package')
AUTHOR = metadata.get('author', '')
AUTHOR_EMAIL = metadata.get('author_email', '')
LICENSE = metadata.get('license', 'unknown')
URL = metadata.get('url', 'http://astropy.org')

# Get the long description from the package's docstring
# __import__(PACKAGENAME)
# package = sys.modules[PACKAGENAME]
# LONG_DESCRIPTION = package.__doc__
LONG_DESCRIPTION = open('LONG_DESCRIPTION.rst').read()


# Store the package name in a built-in variable so it's easy
# to get from other parts of the setup infrastructure
builtins._ASTROPY_PACKAGE_NAME_ = PACKAGENAME

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
# We use the format is `x.y` or `x.y.z` or `x.y.dev`
VERSION = '0.4'

# Indicates if this version is a release version
RELEASE = 'dev' not in VERSION

if not RELEASE:
    VERSION += get_git_devstr(False)

# Populate the dict of setup command overrides; this should be done before
# invoking any other functionality from distutils since it can potentially
# modify distutils' behavior.
cmdclassd = register_commands(PACKAGENAME, VERSION, RELEASE)


# Freeze build information in version.py
generate_version_py(PACKAGENAME, VERSION, RELEASE,
                    get_debug_option(PACKAGENAME))

# Get configuration information from all of the various subpackages.
# See the docstring for setup_helpers.update_package_files for more
# details.
package_info = get_package_info()

# Add the project-global data
package_info['package_data'].setdefault(PACKAGENAME, [])

# Define entry points for command-line scripts
entry_points = {'console_scripts': []}
for key, value in conf.items('entry_points'):
    entry_points['console_scripts'].append('{0} = {1}'.format(key, value))

# Note: usually the `affiliated_package/data` folder is used for data files.
# In Gammapy we use `gammapy/data` as a sub-package.
# Uncommenting the following line was needed to avoid an error during
# the `python setup.py build` phase
# package_info['package_data'][PACKAGENAME].append('data/*')

# Include all .c files, recursively, including those generated by
# Cython, since we can not do this in MANIFEST.in with a "dynamic"
# directory name.
c_files = []
for root, dirs, files in os.walk(PACKAGENAME):
    for filename in files:
        if filename.endswith('.c'):
            c_files.append(
                os.path.join(
                    os.path.relpath(root, PACKAGENAME), filename))
package_info['package_data'][PACKAGENAME].extend(c_files)

setup(
    name=PACKAGENAME,
    version=VERSION,
    description=DESCRIPTION,
    # Note: these are the versions we test.
    # Older versions could work, but are unsupported.
    # To find out if everything works run the Gammapy tests.
    install_requires=[
      'setuptools',
      'click',
      'numpy>=1.8',
      'astropy>=1.1',
    ],
    extras_require=dict(
      analysis=[
          'scipy>=0.15',
          'scikit-image>=0.10',
          'photutils>=0.1',
          'reproject',
          'gwcs',
          'astroplan',
          'uncertainties>=2.4',
          'naima',
          'iminuit',
          'sherpa',
      ],
      plotting=[
          'matplotlib>=1.4',
          'wcsaxes>=0.3',
          'aplpy>=0.9',
      ],
      gui=[
          'flask',
          'flask-bootstrap',
          'flask-wtf',
          'flask-nav',
      ],
    ),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    long_description=LONG_DESCRIPTION,
    classifiers=[
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: C',
      'Programming Language :: Cython',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: Implementation :: CPython',
      'Topic :: Scientific/Engineering :: Astronomy',
      'Development Status :: 3 - Alpha',
    ],
    cmdclass=cmdclassd,
    zip_safe=False,
    use_2to3=False,
    entry_points=entry_points,
    **package_info
)
