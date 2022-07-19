# -*- coding: utf-8 -*-
#
#  pyProxy6 - Lib setup file.
#  Created by LulzLoL231 at 02/07/22
#
import re
from setuptools import setup


init_data = open('proxy6/__init__.py').read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, init_data, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in "proxy6/__init__.py"')


def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def requirements():
    reqs_list = []
    with open("requirements.txt", encoding='utf-8') as reqs:
        for req in reqs:
            reqs_list.append(req.strip())
    return reqs_list


setup(
    name='pyProxy6',
    version=verstr,
    long_description=long_description(),
    long_description_content_type='text/markdown',
    description='Python wrapper for proxy6.net API',
    author='Maxim Mosin',
    author_email='max@mosin.pw',
    license='Apache License, Version 2.0, see LICENSE file',
    keywords=['proxy6', 'proxy6.net', 'proxy'],
    url='https://github.com/LulzLoL231/pyProxy6',
    download_url='https://github.com/LulzLoL231/pyProxy6/archive/master.zip',
    packages=['proxy6', 'proxy6.sync', 'proxy6.async_'],
    install_requires=requirements(),
    setup_requires=['wheel'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
        'Programming Language :: Python :: 3 :: Only',
    ]
)
