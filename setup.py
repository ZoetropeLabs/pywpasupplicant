#!/usr/bin/env python

from setuptools import setup, Extension
from pywpasupplicant import __version__

from setuptools.command.install import install


class Build_ext_first(install):
    def run(self):
        self.run_command("build_ext")
        return install.run(self)


wpa_ctrl_iface_ext = Extension(
    name="pywpasupplicant._wpa_ctrl",
    sources=[
        "pywpasupplicant/wpa_ctrl.c",
        "pywpasupplicant/wpa_ctrl.i",
    ],
    depends=[
        "pywpasupplicant/wpa_ctrl.h",
    ],
    define_macros=[
        ("CONFIG_CTRL_INTERFACE", None),
        ("CONFIG_CTRL_IFACE_UNIX", None),
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
    py_modules=["wpa_ctrl"],
    cmdclass = {'install' : Build_ext_first},
)
