from setuptools import setup, find_packages

setup(
    name = 'Lumen',
    version = '0.1',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    entry_points = {
        'console_scripts': ['lumen = Lumen.lumen:main']
    },
)