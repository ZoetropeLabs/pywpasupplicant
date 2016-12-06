#!/usr/bin/env python

from setuptools import setup, Extension, find_packages
from pywpasupplicant import __version__

from setuptools.command.install import install


class Build_ext_first(install):
    def run(self):
        self.run_command("build_ext")
        return install.run(self)


wpa_ctrl_iface_ext = Extension(
    name="_wpa_ctrl",
    sources=[
        "pywpasupplicant/wpa_ctrl.i",
    ],
    depends=[
        "setup.py",
    ],
    libraries=[
        "wpactrl",
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
    packages=find_packages(exclude=["tests"]),
    py_modules=["pywpasupplicant.wpa_ctrl"],
    cmdclass = {'install' : Build_ext_first},
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
