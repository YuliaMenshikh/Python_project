from setuptools import setup, find_packages


setup(
    name='task-py-diary',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'task-py-diary': ['resources/*'],
    },
    install_requires=[
        'appdirs',
        'terminaltables',
    ],
    entry_points={
        'console_scripts': [
            'taskpydiary = task_py_diary:main',
        ],
    }
)
