import os

from setuptools import setup, find_packages
from pip.req import parse_requirements


basedir = os.path.dirname(__file__)
requirements_path = os.path.join(basedir, 'requirements.txt')

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_requirements = parse_requirements(
    requirements_path, session=False
)

# Convert to setup's list of strings format:
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='widely',
    version='0.16',
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
