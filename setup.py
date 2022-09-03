#!/usr/bin/env python


import pathlib
import setuptools


requires = [
    'cryptography',
    'tqdm',
    'click',
    'pandas',
]

root = pathlib.Path(__file__).parent.resolve()
with (root / 'README.md').open('r', encoding='utf-8') as f:
    readme = f.read()

about = {}
with (root / 'zteb' / '__about__.py').open('r', encoding='utf-8') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    long_description=readme,
    license=about['__licence__'],
    long_description_content_type='text/markdown',
    url=about['__url__'],
    packages=setuptools.find_packages(),
    package_data={'': ['LICENSE']},
    package_dir={'zteb': 'zteb'},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'zteb = zteb.cli.main:cli_group',
        ],
    },
)
