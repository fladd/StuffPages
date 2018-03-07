from setuptools import setup

setup(
    name = 'stuffpages',
    version = '0.6.0',
    packages = ['stuffpages'],
    package_data = {'stuffpages': ['styles/*.*']},
    entry_points = {
        'console_scripts': [
            'stuffpages = stuffpages.__main__:main'
        ]
    },
    install_requires = ['markdown',
                        'pymdown-extensions',
                        'Pygments',
                        'beautifulsoup4'])
