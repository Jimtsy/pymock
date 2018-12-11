try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pymock',
    version='0.0.1',
    packages=['pymock'],
    url='https://github.com/Jimtsy/pymock.git',
    license='MIT',
    author='jim',
    description='base on sanic',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
    ],
    install_requires=[
        "aiohttp",
    ]
)
