#!/bin/bash
# Test script for Sound Server

BASE_URL="http://localhost:48291"

echo "🔍 Testing Sound Server..."
echo ""

# Test 1: Health check
echo "1️⃣  Health Check:"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: List sounds
echo "2️⃣  Available Sounds:"
curl -s "$BASE_URL/sounds" | python3 -m json.tool
echo ""
echo ""

# Test 3: Play a sound
echo "3️⃣  Playing 'strong_minded.mp3':"
curl -s -X POST "$BASE_URL/play" \
  -H 'Content-Type: application/json' \
  -d '{"sound":"strong_minded.mp3"}' | python3 -m json.tool
echo ""
echo ""

# Test 4: Play with volume
echo "4️⃣  Playing 'just_saying.mp3' at 50% volume:"
curl -s -X POST "$BASE_URL/play" \
  -H 'Content-Type: application/json' \
  -d '{"sound":"just_saying.mp3", "volume":0.5}' | python3 -m json.tool
echo ""
echo ""

# Test 5: Test from Docker (if running in Docker)
echo "5️⃣  Testing Docker access (using host.docker.internal):"
curl -s -X POST "http://host.docker.internal:48291/play" \
  -H 'Content-Type: application/json' \
  -d '{"sound":"you_would_be_glad_to_know.mp3"}' | python3 -m json.tool 2>/dev/null || echo "⚠️  Not accessible (expected if not running in Docker)"
echo ""

echo "✅ Tests complete!"
