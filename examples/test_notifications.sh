#!/bin/bash
#
# Example: Test Suite with Sound Notifications
#
# This script wraps a test suite and provides audio feedback on completion.
# Perfect for long test runs where you want to be notified when they finish.

set -e

SOUND_SERVER="http://localhost:9091"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

play_sound() {
    local sound=$1
    local volume=${2:-1.0}
    curl -s -X POST "$SOUND_SERVER/play" \
        -H 'Content-Type: application/json' \
        -d "{\"sound\":\"$sound\", \"volume\":$volume}" \
        > /dev/null 2>&1 || true
}

echo "🧪 Starting test suite..."
play_sound "test-start.mp3" 0.7

# Track test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Example: Run different test suites with individual notifications
run_test_suite() {
    local suite_name=$1
    local test_command=$2

    echo ""
    echo "Running $suite_name..."
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $suite_name passed${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        play_sound "tick.mp3" 0.4
    else
        echo -e "${RED}❌ $suite_name failed${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        play_sound "error.mp3" 0.6
    fi
}

# Run various test suites
run_test_suite "Unit Tests" "pytest tests/unit/"
run_test_suite "Integration Tests" "pytest tests/integration/"
run_test_suite "Linting" "pylint src/"
run_test_suite "Type Checking" "mypy src/"

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test Results:"
echo "  Total:  $TOTAL_TESTS"
echo -e "  ${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED_TESTS${NC}"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Final notification based on results
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    play_sound "test-success.mp3" 1.0
    exit 0
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    play_sound "test-failed.mp3" 1.0
    exit 1
fi
