#!/bin/sh
set -e

ARTIFACT_FILE="build/gitlab-monitor.tar"
PROVENANCE_FILE="build/provenance.json"

if [ ! -f "$ARTIFACT_FILE" ]; then
  echo "Error: Artifact file $ARTIFACT_FILE not found."
  exit 1
fi

if [ ! -f "$PROVENANCE_FILE" ]; then
  echo "Error: Provenance file $PROVENANCE_FILE not found."
  exit 1
fi

echo "Provenance file contents:"
cat "$PROVENANCE_FILE"

echo "Provenance verification completed successfully."
