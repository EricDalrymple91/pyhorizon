from setuptools import setup

__version__ = '0.1'

setup(
    name='pyhorizon',
    version=__version__,
    
    packages=['pyhorizon'],

    description='Pyhorizon is a thin wrapper on top of the NASA API.',
    author='Eric Dalrymple',
	author_email='ericjdalrymple@gmail.com',
    url='https://github.com/EricDalrymple91/pyhorizon',
    download_url='https://github.com/EricDalrymple91/pyhorizon/tarball/0.1',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    license='MIT',
    install_requires=[
        'requests'
    ],
 )
 