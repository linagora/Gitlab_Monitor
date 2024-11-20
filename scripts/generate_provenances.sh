#!/bin/sh
set -e

mkdir -p build

tar -czf build/task-manager.tar ./code_final

cat <<EOF > build/provenance.json
{
  "artifact": "build/task-manager.tar",
  "commit": "$CI_COMMIT_SHA",
  "pipeline": "$CI_PIPELINE_ID",
}
EOF
