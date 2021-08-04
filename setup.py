#!/usr/bin/python

from setuptools import Extension, setup


setup(
    name = "python-v4l2capture",
    version = "12",
    author = "pi-top",
    author_email = "deb-maintainers@pi-top.com",
    url = "https://github.com/pi-top/python-v4l2capture",
    description = "Capture video with video4linux2",
    long_description = "python-v4l2capture is a slim and easy to use Python "
    "extension for capturing video with video4linux2.",
    license = "Public Domain",
    classifiers = [
        "License :: Public Domain",
        "Programming Language :: C"],
    ext_modules = [
        Extension("v4l2capture", ["v4l2capture.c"], libraries = ["v4l2"])])
