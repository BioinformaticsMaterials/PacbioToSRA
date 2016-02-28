from setuptools import setup

setup(
    name='pacb_ncbi',
    version='0.6',
    py_modules=['pacb_ncbi'],
    install_requires=[
        'Click',
        'futures',
        'openpyxl'
    ],
    entry_points='''
        [console_scripts]
        pacb_ncbi=pacb_ncbi:cli
    ''',
)

