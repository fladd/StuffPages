from setuptools import setup

def get_version():
    """Get version and version_info from stuffpages/__meta__.py file."""

    import os
    module_path = os.path.join(os.path.dirname('__file__'), 'stuffpages',
                               '__meta__.py')

    import importlib.util
    spec = importlib.util.spec_from_file_location('__meta__', module_path)
    meta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(meta)
    return meta.__version__

__version__ = get_version()

setup(
    name = 'StuffPages',
    version = __version__,
    packages = ['stuffpages'],
    package_data = {'stuffpages': ['_stuffpages/styles/*.*']},
    entry_points = {
        'console_scripts': [
            'stuffpages = stuffpages.__main__:main'
        ]
    },
    install_requires = ['markdown',
                        'pymdown-extensions',
                        'Pygments',
                        'beautifulsoup4'])
