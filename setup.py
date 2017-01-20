#!/usr/bin/env python3
from setuptools import setup

setup(
	name="Endrilo",
	version="0.2",
	description="This script encodes and decodes text, files or piping, by counting bits in succession.",
	author="z0noxz",
	author_email="z0noxz@mail.com",
	url="https://github.com/z0noxz/endrilo",
	classifiers=[
		"Development Status :: 2 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: End Users/Desktop",
		"Natural Language :: English",
		"Programming Language :: Python",
		"Topic :: Security :: Cryptography",
		"Topic :: Text Processing :: Filters",
		"Topic :: Text Processing :: Linguistic",
	],
	requires=[
		"array",
		"base64",
		"getopt",
		"gzip",
		"hashlib",
		"random",
		"sys",
		"traceback",
		"os"
	],
	scripts=["bin/endrilo"],
	packages=["endrilo"]
)