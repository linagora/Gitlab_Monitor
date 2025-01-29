
# # --- Copyright (c) 2024-2025 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com



# # --- Script used in the pipeline to generate the provenance of the source code.

#!/bin/sh
set -e

mkdir -p build

cat <<EOF > build/provenance.json
{
  "commit": "$CI_COMMIT_SHA",
  "pipeline": "$CI_PIPELINE_ID",
}
EOF
