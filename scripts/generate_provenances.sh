
# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

#!/bin/sh
set -e

mkdir -p build

cat <<EOF > build/provenance.json
{
  "commit": "$CI_COMMIT_SHA",
  "pipeline": "$CI_PIPELINE_ID",
}
EOF
