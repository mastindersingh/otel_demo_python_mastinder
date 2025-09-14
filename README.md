# OpenTelemetry Logging Demo Application

A comprehensive Python demo application that demonstrates how to integrate OpenTelemetry with Python logging for observability and distributed tracing.

## Features

This demo application showcases:

- **Structured Logging**: Integration of OpenTelemetry with Python's standard logging library
- **Trace Correlation**: Automatic correlation between logs and distributed traces
- **Span Management**: Creating and managing spans with automatic logging
- **Multiple Log Levels**: Demonstration of DEBUG, INFO, WARNING, and ERROR log levels
- **Nested Operations**: Simulating real-world scenarios with nested spans and operations
- **Error Handling**: Proper error logging and exception handling with OpenTelemetry
- **Structured Data**: Logging with custom attributes and metadata
- **Export Formats**: Console and OTLP export capabilities

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mastindersingh/otel_demo_app_logs.py.git
   cd otel_demo_app_logs.py
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the demo application:

```bash
python otel_demo_app_logs.py
```

## What the Demo Does

The application simulates a typical web service with the following operations:

1. **Log Levels Demo**: Shows different log levels with structured data
2. **User Request Simulation**: Simulates user actions (login, purchase, logout, etc.)
3. **Database Operations**: Simulates database queries with nested spans
4. **Error Scenarios**: Demonstrates error handling and logging

## Sample Output

The demo will output both regular Python logs and OpenTelemetry-formatted logs to the console. You'll see:

- Trace IDs and Span IDs correlating logs with traces
- Structured log data with custom attributes
- Nested span relationships
- Performance metrics and timing information
- Error handling and exception logging

## Configuration

The demo uses the following OpenTelemetry components:

- **TracerProvider**: For creating and managing traces
- **LoggerProvider**: For OpenTelemetry logging integration
- **ConsoleSpanExporter**: Exports traces to console
- **ConsoleLogRecordExporter**: Exports logs to console
- **Resource**: Service identification and metadata

## Customization

You can modify the demo by:

- Changing the service name in the `OpenTelemetryLoggingDemo` constructor
- Adding new simulation scenarios in the `run_demo()` method
- Configuring different exporters (OTLP, Jaeger, etc.)
- Adjusting log levels and formats
- Adding custom attributes and metadata

## Dependencies

The demo requires the following OpenTelemetry packages:

- `opentelemetry-api`: Core OpenTelemetry API
- `opentelemetry-sdk`: OpenTelemetry SDK implementation
- `opentelemetry-instrumentation`: Base instrumentation package
- `opentelemetry-exporter-otlp`: OTLP protocol exporter
- `opentelemetry-exporter-console`: Console output exporter

Additional packages for the demo scenarios:
- `requests`: HTTP client library
- `flask`: Web framework (for potential web service examples)

## License

This project is open source and available under the MIT License.