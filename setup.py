import setuptools

setuptools.setup(
    name='tractdb',
    version='0.1.3',
    description='TractDB',
    url='https://tractdb.org',
    packages=['tractdb'],
    install_requires=[
        'couchdb',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [],
    },
    zip_safe=False,
)
