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

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'StuffPages',
    description = \
    'StuffPages - ' \
    'A quick way to create simple web pages using Markdown',
    author = 'Florian Krause',
    author_email = 'florian.krause@fladd.de',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://fladd.github.io/StuffPages/',
    version = get_version(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = ['stuffpages'],
    package_data = {'stuffpages': ['_stuffpages/*.*',
                                   '_stuffpages/styles/*.*']},
    python_requires=">=3.6",
    setup_requires = ['wheel'],
    install_requires = ['markdown==3.3.4',
                        'pymdown-extensions==9.1',
                        'Pygments==2.10.0',
                        'beautifulsoup4==4.10.0'],
    entry_points = {
        'console_scripts': [
            'stuffpages = stuffpages.__main__:main'
        ]
    }
)
