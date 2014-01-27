
from setuptools import setup, find_packages

# See http://bugs.python.org/issue15881
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='turing',
    version='0.1a',
    description='Simple turing machine language compiler',
    long_description=open('README.md').read(), author='Maxim Yaskevich',
    author_email='myaskevich@live.com',
    license='MIT',
    packages=find_packages(),
    tests_require=['nose', 'mock'],
    test_suite='nose.collector',
    install_requires=['parsimonious', 'jinja2'],
    url='https://github.com/myaskevich/turing',
    package_data = {
        'turing': ['compiler/templates/*.txt'],
    },
    entry_points={
        'console_scripts': ['turingc=turing.compiler.main:main'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Software Development :: Compilers',
    ],
    keywords=['turing', 'machine', 'compiler', 'automaton'],
)
