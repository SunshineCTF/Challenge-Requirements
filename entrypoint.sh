#!/bin/bash
date
ls -la
pwd

# Check if monorepo input is set to false, then use single-challenge mode
if [ "$INPUT_MONOREPO" = "false" ]; then
    python3 /check.py --single-challenge
else
    python3 /check.py --monorepo
fi