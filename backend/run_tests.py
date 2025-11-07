#!/usr/bin/env python3
"""
Simple test runner for SecureCode Vault
"""
import subprocess
import sys


def run_tests():
    """Run pytest with the correct Python path"""
    print("🚀 Running SecureCode Vault Tests...")

    # Run pytest with the app directory in Python path
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-v",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term",
        ],
        cwd=".",
    )

    if result.returncode == 0:
        print("✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
