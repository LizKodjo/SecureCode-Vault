#!/bin/bash

set -e

echo "🔒 Running Security Scans..."

# Bandit - Static Application Security Testing
echo "Running Bandit (SAST)..."
bandit -r backend/app/ -f json -o reports/bandit-report.json

# Safety - Dependency Vulnerability Scanning
echo "Running Safety Check..."
safety check --json > reports/safety-report.json

# Trivy - Container & Filesystem Scanning
echo "Running Trivy Scan..."
trivy fs --security-checks vuln,secret --exit-code 1 . > reports/trivy-report.txt

# Secret Scanning
echo "Running Git Secrets Scan..."
if command -v git-secrets >/dev/null 2>&1; then
    git secrets --scan
else
    echo "git-secrets not installed, skipping..."
fi

echo "✅ Security scans completed!"
echo "📊 Reports saved to: reports/"