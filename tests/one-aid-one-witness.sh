#!/bin/bash

test_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export WITNESS_CONFIG="${test_dir}/config"
export DATA="${test_dir}/data"
export TEST_BASE="${test_dir}/base"

echo "removing test base directory: $TEST_BASE"
if [ -d "$TEST_BASE" ]; then
  rm -rf "$TEST_BASE"
fi

#witness start --alias "sample" -H 5642 --config-dir "${WITNESS_CONFIG}" --config-file "sample" --config-file "sample" --salt 0AB7emu7HAP3C3wjz9EiH1_e --base "${TEST_BASE}" &
#wit_pid=$!
#
#cleanup() {
#  echo "Killing process with PID $wit_pid"
#  kill $wit_pid
#}
#
#trap cleanup EXIT

# Your script logic here
kli init --name alice --salt 0ACDEyMzQ1Njc4OWxtbm9GhI --nopasscode --config-dir "${DATA}" --config-file witness --base "${TEST_BASE}"
kli incept --name alice --alias alice --file "${DATA}"/incept.json --base "${TEST_BASE}"
# Add your script logic here

#wait $wit_pid