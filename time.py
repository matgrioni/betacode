import argparse
import time

import betacode.conv

def read(fn):
    """
    Read in the given file name as is.

    Args:
    fn: The filename to read in. The file will be read relative to the current
        execution environment.

    Returns:
    The text of the file.
    """
    f = open(fn)
    text = f.read()
    f.close()

    return text

parser = argparse.ArgumentParser()
parser.add_argument('fn', help='The filename to read in')
args = parser.parse_args()

text = read(args.fn)

start = time.time()
result = betacode.conv.beta_to_uni(text)
end = time.time()

print(end - start)
