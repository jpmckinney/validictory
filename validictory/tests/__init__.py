#!/usr/bin/env python

import unittest
import doctest


def additional_tests():
    import validictory
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(validictory))
    return suite


def main():
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))
    main()
