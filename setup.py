#!/usr/bin/env python
"""The setup and build script for the python-telegram-bot library."""

# import codecs
# import os
# import sys

from setuptools import setup, find_packages


def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open("requirements.txt") as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages(exclude=["tests*"])
requirements = requirements()

# Allow for a package install to not use the vendored urllib3
# UPSTREAM_URLLIB3_FLAG = "--with-upstream-urllib3"
# if UPSTREAM_URLLIB3_FLAG in sys.argv:
#     sys.argv.remove(UPSTREAM_URLLIB3_FLAG)
#     requirements.append("urllib3 >= 1.19.1")
#     packages = [x for x in packages if not x.startswith("telegram.vendor.ptb_urllib3")]

setup(
    name="python-telegram-bot",
    version="1.0b1",
    author="Ion Lizarazu",
    author_email="ilizarazu@codesyntax.com",
    license="LGPLv3",
    url="https://t.me/mendidenborak",
    keywords="python telegram bot api wrapper",
    description="Mendidenborak Telegram",
    long_description="Mendi denborak kalkulatzeko telegram bot bat",
    packages=packages,
    install_requires=requirements,
    extras_require={},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
