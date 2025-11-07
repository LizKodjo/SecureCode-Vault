#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running SecureCode Vault Tests...${NC}"

# Run tests with coverage
python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo -e "${GREEN}📊 Coverage report generated in htmlcov/index.html${NC}"
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    exit 1
fi