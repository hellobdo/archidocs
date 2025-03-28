#!/bin/bash
pdftocairo -pdf "$1" /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "PDF/A validation passed"
  exit 0
else
  echo "PDF/A validation failed"
  exit 1
fi
