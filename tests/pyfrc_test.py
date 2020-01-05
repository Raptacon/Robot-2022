'''
    This test module imports tests that come with pyfrc, and can be used
    to test basic functionality of just about any robot.
'''

from pyfrc.tests import *


def two_plus(arg):
    return 2 + arg

def test_addition():
    assert two_plus(2) == 5
