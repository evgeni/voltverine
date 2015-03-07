from setuptools import setup


setup(
    name="voltverine",
    version="0.1.0",
    description="let's shutdown this machine",
    author="Evgeni Golov",
    author_email="evgeni@golov.de",
    url="http://github.com/evgeni/voltverine",
    license="MIT",
    packages=['voltverine', 'voltverine.plugins', 'voltverine.actions'],
    scripts=['voltverine.py'],
    zip_safe=False,
    install_requires=['psutil'],
    tests_require=['dbusmock'],
    test_suite='nose.collector',
)
