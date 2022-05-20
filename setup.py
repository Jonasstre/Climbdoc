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
        "PyQt5"
    ],
    python_requires='>=3.10.4'
)
