import os
import sys
from setuptools import (
    find_packages,
    setup,
)
from distutils.command.install import install
from os import path

# managing version
with open("VERSION", 'r') as f:
    VERSION = f.read()

# managing readme
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    readme = f.read()

class InstallWithKernelspec(install):
    def run(self):
        # Regular installation
        install.run(self)

        # Kernel installation
        if "NO_KERNEL_INSTALL" in os.environ:
            # If the NO_KERNEL_INSTALL env variable is set then skip the kernel installation.
            return
        else:
            from cairo_kernel import install as kernel_install
            kernel_install.main(argv=sys.argv)

setup(
    name='cairo_kernel',
    version=VERSION,
    packages=['cairo_kernel'],
    description='Jupyter kernel for Cairo language',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ankit Chiplunkar, Arie Benhamou',
    author_email='ankitchiplunkar@gmail.com, benhamou.arie@gmail.com',
    python_requires='>=3.6, <3.10',
    keywords=['ethereum', 'starkware'],
    install_requires=[
        "pygments",
        "contextvars",
        "cairo-lang==0.4.2",
        "jupyter==1.0.0",
        "jupyter_client==6.1.12",
        "ipykernel==6.4.2",
        "pytest==6.2.5",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)