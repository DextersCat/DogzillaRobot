#!/bin/bash
# Timing Fix Verification Script
# Following CTO Directive 001-A: Observe → Prove → Act

echo "🔧 FAULT-TREE V1.0 TIMING FIX VERIFICATION"
echo "========================================"
echo "Testing settle=0.35s, record=5s implementation"
echo ""

# Check if fixes are applied
echo "📋 Code Verification:"
if grep -q "sleep 0.35" ~/amy_core/astra_listen_loop.sh; then
    echo "✅ Listen loop settle time: 0.35s"
else
    echo "❌ Listen loop settle time: NOT UPDATED"
fi

if grep -q "secs=5" ~/amy_core/postwake_router.py; then
    echo "✅ Record duration: 5s"
else
    echo "❌ Record duration: NOT UPDATED"
fi

echo ""
echo "🎙️  Audio Device Status:"
echo "Input:  $(cat ~/amy_core/env/astra_audio.env | grep AREC_DEV)"
echo "Output: $(cat ~/amy_core/env/astra_audio.env | grep AUDIODEV)"

echo ""
echo "🚀 Ready for end-to-end test:"
echo "   1. Run: bash ~/amy_core/astra_listen_loop.sh"
echo "   2. Say: 'Astra' then 'What's the time?'"
echo "   3. Check logs: tail -f ~/logs/pipeline_*.log"
echo ""
echo "Expected: STT should hear 'What's the time?' instead of 'Astro'"