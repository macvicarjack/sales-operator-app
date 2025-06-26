#!/usr/bin/env python3
"""
Test runner script for Sales Operator app.
Runs all tests with coverage reporting.
"""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests with pytest."""
    # Get the directory containing this script
    test_dir = Path(__file__).parent / "tests"
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        "-v",  # Verbose output
        "--cov=services",  # Coverage for services
        "--cov=utils",     # Coverage for utils
        "--cov=db",        # Coverage for db
        "--cov-report=term-missing",  # Show missing lines
        "--cov-report=html:htmlcov",  # Generate HTML report
        "--tb=short"       # Short traceback format
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 