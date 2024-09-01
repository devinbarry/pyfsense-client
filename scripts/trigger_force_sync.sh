#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f .env ]; then
  export $(grep -E '^[^#]+=' .env | xargs)
fi

# Check if required environment variables are set
if [ -z "$GITLAB_API_URL" ] || [ -z "$PROJECT_ID" ] || [ -z "$GITLAB_TOKEN" ]; then
  echo "Error: Missing required environment variables. Please set GITLAB_API_URL, PROJECT_ID, and GITLAB_TOKEN in your .env file."
  exit 1
fi

# Run against master branch unless we override this
BRANCH="${BRANCH:-master}"

# Trigger the pipeline with FORCE_SYNC set to true
response=$(curl -s -X POST "${GITLAB_API_URL}/projects/${PROJECT_ID}/pipeline" \
  -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "'"${BRANCH}"'",
    "variables": [
      {
        "key": "FORCE_SYNC",
        "value": "true"
      }
    ]
  }')

# Check if the pipeline was triggered successfully
if echo "$response" | grep -q '"id":'; then
  pipeline_id=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d':' -f2)
  echo "Pipeline triggered successfully. Pipeline ID: $pipeline_id"
else
  echo "Failed to trigger pipeline. Response:"
  echo "$response"
  exit 1
fi
