from setuptools import setup

setup(
        name='ziprefresh',
        version='0.1',
        py_modules=['ziprefresh'],
        install_requires=[
            'Click',
            ],
        entry_points='''
            [console_scripts]
            ziprefresh=ziprefresh:refresh
        ''',
    )
