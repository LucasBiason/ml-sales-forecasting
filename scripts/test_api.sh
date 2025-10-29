#!/bin/bash

# Test API endpoints
# Usage: ./scripts/test_api.sh

echo "================================================================================"
echo "ML SALES FORECASTING API - TESTS"
echo "================================================================================"
echo ""

API_URL="http://localhost:8000"

# Check if API is running
if ! curl -s "${API_URL}/api/v1/health" > /dev/null 2>&1; then
    echo "ERROR: API is not running!"
    echo "Start the API first with: make run-api"
    exit 1
fi

echo "✓ API is running"
echo ""

# Test 1: Root
echo "TEST 1: Root Endpoint (GET /)"
echo "--------------------------------------------------------------------------------"
curl -s "${API_URL}/" | python -m json.tool
echo ""
echo ""

# Test 2: Health
echo "TEST 2: Health Check (GET /api/v1/health)"
echo "--------------------------------------------------------------------------------"
curl -s "${API_URL}/api/v1/health" | python -m json.tool
echo ""
echo ""

# Test 3: Model Info
echo "TEST 3: Model Information (GET /api/v1/model/info)"
echo "--------------------------------------------------------------------------------"
curl -s "${API_URL}/api/v1/model/info" | python -m json.tool
echo ""
echo ""

# Test 4: Prediction - Terraced in London
echo "TEST 4: Prediction - Terraced House in Greater London"
echo "--------------------------------------------------------------------------------"
echo "REQUEST:"
cat << 'EOF'
{
  "property_type": "T",
  "old_new": "N",
  "duration": "F",
  "county": "GREATER LONDON",
  "postcode": "SW1A 1AA",
  "year": 2024
}
EOF
echo ""
echo "RESPONSE:"
curl -s -X POST "${API_URL}/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"property_type":"T","old_new":"N","duration":"F","county":"GREATER LONDON","postcode":"SW1A 1AA","year":2024}' \
  | python -m json.tool
echo ""
echo ""

# Test 5: Prediction - Detached in Surrey
echo "TEST 5: Prediction - Detached House in Surrey (Expensive)"
echo "--------------------------------------------------------------------------------"
echo "REQUEST:"
cat << 'EOF'
{
  "property_type": "D",
  "old_new": "Y",
  "duration": "F",
  "county": "SURREY",
  "postcode": "GU1 1AA",
  "year": 2024
}
EOF
echo ""
echo "RESPONSE:"
curl -s -X POST "${API_URL}/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"property_type":"D","old_new":"Y","duration":"F","county":"SURREY","postcode":"GU1 1AA","year":2024}' \
  | python -m json.tool
echo ""
echo ""

# Test 6: Prediction - Flat in Manchester
echo "TEST 6: Prediction - Flat in Greater Manchester (Cheaper)"
echo "--------------------------------------------------------------------------------"
echo "REQUEST:"
cat << 'EOF'
{
  "property_type": "F",
  "old_new": "N",
  "duration": "L",
  "county": "GREATER MANCHESTER",
  "postcode": "M1 1AA",
  "year": 2024
}
EOF
echo ""
echo "RESPONSE:"
curl -s -X POST "${API_URL}/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"property_type":"F","old_new":"N","duration":"L","county":"GREATER MANCHESTER","postcode":"M1 1AA","year":2024}' \
  | python -m json.tool
echo ""
echo ""

echo "================================================================================"
echo "ALL TESTS COMPLETED!"
echo "================================================================================"

