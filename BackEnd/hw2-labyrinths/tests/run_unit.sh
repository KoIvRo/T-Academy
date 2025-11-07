#!/bin/sh

set -euo pipefail

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

run_tests() {
    local path=$1
    local passed=0
    local failed=0
    
    if [ -f "$path" ]; then
        printf "${YELLOW}Запуск $path${RESET}\n"
        if python -m pytest "$path" -v; then
            printf "${GREEN}ПРОЙДЕН${RESET}\n"
            passed=1
        else
            printf "${RED}НЕ ПРОЙДЕН${RESET}\n"
            failed=1
        fi
    elif [ -d "$path" ]; then
        printf "${YELLOW}Запуск тестов из $path${RESET}\n"
        for test_file in "$path"/test_*.py; do
            if [ -f "$test_file" ]; then
                if python -m pytest "$test_file" -v; then
                    passed=$((passed + 1))
                else
                    failed=$((failed + 1))
                fi
            fi
        done
    else
        printf "${RED}Не найден: $path${RESET}\n"
        exit 1
    fi
    
    printf "\n${GREEN}Успешно: $passed${RESET}, ${RED}Неудачи: $failed${RESET}\n"
    [ $failed -eq 0 ]
}

if [ $# -eq 0 ]; then
    run_tests "tests/unit"
else
    run_tests "$1"
fi