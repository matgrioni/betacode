from distutils.core import setup
import os

def read(fn):
    """
    Read in the given file.

    Args:
    fn: The filename to read in, relative to the current folder.

    Returns:
    The text contents of the file.
    """
    with open(os.path.join(os.path.dirname(__file__), fn), encoding='utf-8') as f:
        return f.read()

setup(
    name = 'betacode',
    packages = ['betacode'],
    version = '1.0',
    description = 'Betacode to Unicode converter.',
    long_description = read('README.rst'),
    author = 'Matias Grioni',
    author_email = 'matgrioni@gmail.com',
    url = 'https://github.com/matgrioni/betacode',
    license = 'MIT',
    keywords = ['encoding', 'unicode', 'betacode', 'greek'],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Greek',
    ],
)
