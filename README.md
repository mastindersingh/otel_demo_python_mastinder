# OpenTelemetry Python Demo App

This app demonstrates traces, metrics, logs, SLO/SLI simulation, and a trade service with Dynatrace OTLP export.

## Features
- Multiple endpoints: `/service`, `/distributed`, `/topology`, `/event`, `/slo/success`, `/slo/fail`, `/slo/latency`, `/trade/buy`, `/trade/sell`, `/load`
- Distributed traces, logs, and metrics with host/service context
- SLO/SLI simulation and trade operations
- Built-in load generator (`/load` endpoint)

## Quick Start
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set Dynatrace OTLP environment variables (see `dynatrace-otel-config.ps1` or your own config).
3. Run the app:
   ```
   python otel_demo_app.py
   ```
4. Open [http://localhost:8080](http://localhost:8080) to see available endpoints.
5. Visit `/load` to start generating traffic for Dynatrace.

## Requirements
- Python 3.8+
- Dynatrace API token with ingest scopes

## Example Endpoints
- `/service` - Service span and metric
- `/distributed` - Simulated distributed trace
- `/topology` - Host and topology info
- `/event` - Custom event
- `/slo/success`, `/slo/fail`, `/slo/latency` - SLO/SLI simulation
- `/trade/buy`, `/trade/sell` - Trade operations with random outcome
- `/load` - Starts background load generator

# Installation & Run Instructions

# 1. Create and activate a virtual environment
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# --- Dynatrace OTLP config (change these) ---
# Set these environment variables before running the app:
# (Replace <your-env> and <YOUR_DT_API_TOKEN> with your values)

$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "https://<your-env>.live.dynatrace.com/api/v2/otlp"
$env:OTEL_EXPORTER_OTLP_HEADERS = "Authorization=Api-Token <YOUR_DT_API_TOKEN>"
$env:OTEL_SERVICE_NAME = "demo-python"
$env:OTEL_TRACES_EXPORTER = "otlp"
$env:OTEL_METRICS_EXPORTER = "none"
$env:OTEL_LOGS_EXPORTER = "none"

# 3. Auto-instrument Flask + requests and run the app
opentelemetry-instrument python app.py
