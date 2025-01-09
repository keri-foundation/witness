#!/usr/bin/env bash

set -xue

TIME=$(kli time)
CURLS="http://164.90.253.93:5642"

cat <<EOF > "/usr/local/var/keri/cf/sample.json"
{
  "sample": {
   "dt": "$TIME",
   "curls": ["$CURLS"]
 },
 "dt": "$TIME"
}
EOF

if [ ! -f /usr/local/var/keri/db/sample/data.mdb ]; then
  kli init --name "sample" --nopasscode --salt "0AA4JO-wA4Ct4uiyMI9zXxER"
fi

export DEBUG_KLI=1
kli migrate run --name "sample"
kli escrow clear --force --name "sample"
kli witness start --name "sample" --alias "sa" --http "5642"
