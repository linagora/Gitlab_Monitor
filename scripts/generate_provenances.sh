#!/bin/sh
set -e

mkdir -p build

tar -czf build/gitlab-monitor.tar ./gitlab-monitor

cat <<EOF > build/provenance.json
{
  "artifact": "build/gitlab-monitor.tar",
  "commit": "$CI_COMMIT_SHA",
  "pipeline": "$CI_PIPELINE_ID",
}
EOF
