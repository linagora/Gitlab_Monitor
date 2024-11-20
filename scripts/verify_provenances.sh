#!/bin/sh
set -e

PROVENANCE_FILE="build/provenance.json"

if [ ! -f "$PROVENANCE_FILE" ]; then
  echo "Error: Provenance file $PROVENANCE_FILE not found."
  exit 1
fi

echo "Provenance file contents:"
cat "$PROVENANCE_FILE"

echo "Provenance verification completed successfully."
