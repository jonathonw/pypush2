from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name = "pypush2",
    version = "0.1",
    packages = find_packages(exclude=['examples']),
    install_requires = [
      'python-rtmidi>=0.5b1',
      'mido>=1.1.14',
      'pyusb>=1.0.0b2',
      'cairocffi>=0.7.2',
      'cython>=0.23.2',
      'flufl.enum>=4.1',
      'axel>=0.0.4'
    ],
    entry_points = {
        'console_scripts': [
        ]
    },
    setup_requires=[
      'pytest-runner>=2.0,<3dev'
    ],
    tests_require=[
      'pytest>=2.8.7'
    ],
    ext_modules = cythonize("pypush2/rgbtools.pyx")
)
