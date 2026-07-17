import os

from setuptools import setup, find_packages


basedir = os.path.dirname(__file__)
requirements_path = os.path.join(basedir, 'requirements.txt')

requirements = []
if os.path.exists(requirements_path):
    with open(requirements_path) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='widely',
    version='0.17',
    description='Static Site as a Service using AWS S3',
    long_description=open('README.rst').read(),
    author='Kyle Marek-Spartz and Michael Burling',
    author_email='kyle.marek.spartz@gmail.com',
    py_modules=['widely'],
    url='http://www.celador.mn/widely',
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'widely = widely:main',
        ],
    },
    test_suite='nose.collector',
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Information Technology",
                 "Intended Audience :: System Administrators",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 2 :: Only",
                 "Topic :: Internet",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Internet :: WWW/HTTP :: Site Management",
                 "Topic :: Utilities"],
    license='MIT'
)
