from setuptools import setup


def readfile(fn):
    with open(fn, 'r+') as f:
        return f.read()

setup(
    name="dima-db",
    version="1.0.0",
    description="CLI to view and kill running queries in postgres",
    long_description=readfile('README.md'),
    author="Matthew Ruttley",
    author_email="matt@frame.io",
    url="",
    py_modules=['dima'],
    license=readfile('LICENSE'),
    entry_points={
        'console_scripts': [
            'dima = dima:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database"
    ],
    data_files = [("", ["LICENSE", "README.md"])]
)
