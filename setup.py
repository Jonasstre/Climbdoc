from setuptools import setup
from setuptools import find_packages

setup(
    name='climbdocmain.py',
    version='0.5.2',
    packages=find_packages(where=__file__),
    url='',
    license='',
    author='Jonas Streckmann',
    author_email='Jonas.H.Streckmann@studmail.w-hs.de',
    description='Python program for the "Kletterretter" project',
    install_requires=[
        "matplotlib==3.5.2"
        "numpy==1.22.3"
        "PyQt5==5.15.6"
        "pyqtgraph==0.12.4"
        "pyserial==3.5"
        "qtpy==2.1.0"
        "setuptools==58.1.0"

    ],
    python_requires='>=3.10.4'
)
