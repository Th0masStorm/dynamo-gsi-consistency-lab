#!/bin/bash
set -euo pipefail

TABLE=$(aws cloudformation describe-stacks --stack-name dynamo --query "Stacks[0].Outputs[0].OutputValue" --output text)
ITEMS=$(aws dynamodb scan --table-name ${TABLE} --select "COUNT" --query "Count")
INCONSISTENT_READS=$(wc -l out.log | awk '{ print $1 }')
CONSISTENT_READS=$((${ITEMS}-${INCONSISTENT_READS}))
PERCENTILE=$(python3 -c "print(f\"{(${CONSISTENT_READS}*100/${ITEMS}):.3f}\")")

echo "Total items count: ${ITEMS}"
echo "Consistent reads percentile: ${PERCENTILE}"