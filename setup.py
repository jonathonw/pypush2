from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name = "pypush2",
    version = "0.1",
    packages = find_packages(),
    install_requires = ['python-rtmidi>=0.5b1', 'mido>=1.1.14', 'pyusb>=1.0.0b2', 'cairocffi>=0.7.2', 'cython>=0.23.2'],
    entry_points = {
        'console_scripts': [
        ]
    },
    ext_modules = cythonize("pypush2/rgbtools.pyx")
)
