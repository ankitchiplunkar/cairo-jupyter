
from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='cairo_kernel',
    version='0.0.1',
    packages=['cairo_kernel'],
    description='Jupyter kernel for Cairo landuage',
    long_description=readme,
    author='Ankit Chiplunkar',
    author_email='ankitchiplunkar@gmail.com',
    python_requires='>=3.6, <4',
    keywords=['ethereum', 'starkware'],
    install_requires=[
        "pygments",
        "contextvars",
        "cairo-lang==0.4.2",
        "jupyter==1.0.0",
        "jupyter_client==6.1.12",
        "ipykernel==6.4.2",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)