import os 
import re
from setuptools import setup, find_packages

def get_version():
    with open(os.path.join("tanbot", "__init__.py")) as f:
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', f.read())
        if match:
            return match.group(1)
        raise RuntimeError("Unable to find version string.")

def read_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        # Remove comments and blank lines
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


DESCRIPTION = 'TAN-bot: A bot to fetch data from Google Sheets'
LONG_DESCRIPTION = 'TAN-bot is a bot that fetches data from a google sheet'

setup(
    name='tanbot',
    version=get_version(),
    author='asroc-tw, kuochuanpan',
    author_email='secretariat@asroc.org.tw',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
    keywords=['tanbot', 'bot', 'google sheets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)   