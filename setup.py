from setuptools import setup

setup(
    name='widely',
    version='0.1',
    description='Heroku-style Static-site Platform as a Service command line tool',
    long_description=open('README.md').read(),
    author='Kyle Marek-Spartz and Michael Burling',
    author_email='kyle.marek.spartz@gmail.com',
    py_modules=['widely'],
    url='...',
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
    install_requires=['boto', 'docopt', 'prettytable', 'feedparser'],
    entry_points={
        'console_scripts': [
            'widely = widely:main',
        ],
    },
    test_suite='nose.collector',
    classifiers=["Private :: Do Not Upload"],  ## To be added later.
    license='MIT'
)
