"""Setup configuration"""
from setuptools import find_packages, setup


def parse_requirements():
    with open('./requirements.txt') as f:
        requirements = f.read().splitlines()
        return requirements

dev_requires = [
    "black>=19.10b0",
    "pylint>=2.4",
    "pytest-cov>=2.8.1",
    "pytest>=5.0.0",
    "rope>=0.14.0",
],

setup(
    name="flask-minimal",
    version="0.1.0",
    description="minimal flask app",
    long_description=open("README.md").read(),
    package_dir={"": "src"},
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    install_requires=parse_requirements(),
    extras_require={"dev": dev_requires},
)
