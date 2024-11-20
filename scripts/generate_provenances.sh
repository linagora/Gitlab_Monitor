#!/bin/sh
set -e

mkdir -p build

cat <<EOF > build/provenance.json
{
  "commit": "$CI_COMMIT_SHA",
  "pipeline": "$CI_PIPELINE_ID",
}
EOF
