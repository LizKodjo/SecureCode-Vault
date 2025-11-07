#!/usr/bin/env python3
"""
Simple test runner that sets up the environment correctly
"""
import subprocess
import sys
import os


def run_tests():
    """Run tests with proper Python path setup"""
    print("🚀 Running SecureCode Vault Tests...")

    # Set the Python path
    env = os.environ.copy()
    env['PYTHONPATH'] = '/app'

    # Run pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/", "-v",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term"
    ], env=env, cwd="/app")

    if result.returncode == 0:
        print("✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
