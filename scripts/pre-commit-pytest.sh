#!/bin/bash

if [[ $(git branch --show-current) =~ ^draft/ ]]; then
  echo "Skipping pytest due to draft detected."
else
  pytest
fi
