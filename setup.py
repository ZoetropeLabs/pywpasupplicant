#!/usr/bin/env python

from setuptools import setup, Extension
from pywpasupplicant import __version__


wpa_ctrl_iface_ext = Extension(
    name="_wpactrlc",
    sources=[
        "wpa_ctrl.c",
        "wpasupplicantc.c",
    ],
)

EXT = [
    wpa_ctrl_iface_ext,
]

setup(
    name="pywpasupplicant",
    version=__version__,
    author="Michael Boulton",
    license="BSD-3-Clause",
    author_email="michael.boulton@gmail.com",
    description="Python interface to wpa supplicant",
    use_2to3=True,
    ext_modules=EXT,
    packages=["pywpasupplicant"],
)
