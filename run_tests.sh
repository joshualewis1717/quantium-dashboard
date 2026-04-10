#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/venv/Scripts/activate"

if pytest; then exit 0; fi
exit 1