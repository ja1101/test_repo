#!/usr/bin/env python
import sys
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
