#!/usr/bin/env bash
set -euo pipefail

# Example: curl requests to seed vector store by uploading PDFs in ./sample_pdfs
BACKEND_URL=${BACKEND_URL:-http://localhost:8000}

shopt -s nullglob
files=(sample_pdfs/*.pdf)
if [ ${#files[@]} -eq 0 ]; then
  echo "No PDFs in sample_pdfs. Place service manuals there."
  exit 0
fi

curl -s -X POST "$BACKEND_URL/upload-documents" \
  -H 'Content-Type: multipart/form-data' \
  $(for f in "${files[@]}"; do printf "-F files=@%q " "$f"; done) | jq .
