from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='shell-ai',
    version='0.3.0',
    author='Rick Lamers',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': ['setuptools', 'wheel', 'twine']
    },
    entry_points={
        'console_scripts': [
            'shai=shell_ai.main:main',
        ],
    },
)