#!/bin/bash
# Simple installation script for OpenTelemetry Demo App

echo "Installing OpenTelemetry Logging Demo dependencies..."
echo "=================================================="

# Try to install with pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "Now you can run the demo with full OpenTelemetry features:"
    echo "python otel_demo_app_logs.py"
else
    echo "⚠️ Some dependencies failed to install."
    echo "The demo will still work in basic logging mode."
    echo ""
    echo "Run the demo anyway:"
    echo "python otel_demo_app_logs.py"
fi