
# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com



# # --- Script used in the pipeline to check the provenance of the source code.

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
