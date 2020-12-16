"""
Unit and regression test for the wemrr package.
"""

# Import package, test suite, and other packages as needed
import wemrr
import pytest
import sys

def test_wemrr_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "wemrr" in sys.modules
