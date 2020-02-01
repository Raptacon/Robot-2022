'''
    This test module imports tests that come with pyfrc, and can be used
    to test basic functionality of just about any robot.
'''


import os

if os.getenv("DOC_STRING_CHECK"):
    from pyfrc.tests.docstring_test import * # noqa: F4
else:
    from pyfrc.tests import * # noqa: F4
    def two_plus(arg):
        """
        Simple sample function
        """
        return 2 + arg

    def test_addition():
        """
        Simple test example
        """
        assert two_plus(2) == 4

