#!/usr/bin/env python3
"""
OpenTelemetry Logging Demo Application

This demo shows how to integrate OpenTelemetry with Python logging to:
- Set up structured logging with OpenTelemetry
- Correlate logs with traces and spans
- Export logs to console
- Use different log levels and formats
"""

import logging
import time
import random
from contextlib import contextmanager

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogRecordExporter
    OTEL_AVAILABLE = True
except ImportError:
    print("OpenTelemetry packages not found. Running in basic logging mode.")
    OTEL_AVAILABLE = False


class OpenTelemetryLoggingDemo:
    """Demo class for OpenTelemetry logging integration."""
    
    def __init__(self, service_name: str = "otel-logging-demo"):
        """Initialize OpenTelemetry components."""
        self.service_name = service_name
        
        if OTEL_AVAILABLE:
            self.setup_telemetry()
            self.setup_logging()
            # Get tracer and logger
            self.tracer = trace.get_tracer(__name__)
        else:
            self.setup_basic_logging()
            self.tracer = None
            
        self.logger = logging.getLogger(__name__)
    
    def setup_telemetry(self):
        """Set up OpenTelemetry tracing."""
        # Create resource with service information
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": "1.0.0",
            "environment": "demo"
        })
        
        # Set up trace provider
        trace_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(trace_provider)
        
        # Add console exporter for traces
        console_span_processor = BatchSpanProcessor(ConsoleSpanExporter())
        trace_provider.add_span_processor(console_span_processor)
        
        print(f"✅ Tracing initialized for service: {self.service_name}")
    
    def setup_logging(self):
        """Set up OpenTelemetry logging."""
        # Create resource with service information
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": "1.0.0",
        })
        
        # Set up log provider
        logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(logger_provider)
        
        # Add console exporter for logs
        console_log_processor = BatchLogRecordProcessor(ConsoleLogRecordExporter())
        logger_provider.add_log_record_processor(console_log_processor)
        
        # Create OpenTelemetry logging handler
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        
        # Configure Python logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # Console output
                handler  # OpenTelemetry handler
            ]
        )
        
        print("✅ Logging initialized with OpenTelemetry integration")
    
    def setup_basic_logging(self):
        """Set up basic Python logging when OpenTelemetry is not available."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        print("✅ Basic logging initialized (OpenTelemetry not available)")
    
    @contextmanager
    def create_span(self, name: str):
        """Create a span with automatic logging."""
        if OTEL_AVAILABLE and self.tracer:
            with self.tracer.start_as_current_span(name) as span:
                self.logger.info(f"Started span: {name}")
                try:
                    yield span
                except Exception as e:
                    self.logger.error(f"Error in span {name}: {str(e)}", exc_info=True)
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    raise
                finally:
                    self.logger.info(f"Completed span: {name}")
        else:
            self.logger.info(f"Started operation: {name}")
            try:
                yield None
            except Exception as e:
                self.logger.error(f"Error in operation {name}: {str(e)}", exc_info=True)
                raise
            finally:
                self.logger.info(f"Completed operation: {name}")
    
    def simulate_user_request(self, user_id: int, action: str):
        """Simulate a user request with logging and tracing."""
        with self.create_span("user_request") as span:
            # Add span attributes if span is available
            if span and OTEL_AVAILABLE:
                span.set_attribute("user.id", user_id)
                span.set_attribute("user.action", action)
            
            # Log user action with structured data
            self.logger.info(
                f"Processing user request - User: {user_id}, Action: {action}, Request ID: req_{random.randint(1000, 9999)}"
            )
            
            # Simulate processing time
            processing_time = random.uniform(0.1, 0.5)
            time.sleep(processing_time)
            
            # Simulate success or failure
            if random.random() < 0.8:  # 80% success rate
                self.logger.info(
                    f"Successfully processed {action} for user {user_id} (took {processing_time*1000:.1f}ms)"
                )
                return True
            else:
                error_msg = f"Failed to process {action} for user {user_id}"
                self.logger.error(error_msg)
                raise Exception(error_msg)
    
    def simulate_database_operation(self, table: str, operation: str):
        """Simulate a database operation with nested spans."""
        with self.create_span("database_operation") as span:
            if span and OTEL_AVAILABLE:
                span.set_attribute("db.table", table)
                span.set_attribute("db.operation", operation)
            
            self.logger.debug(f"Connecting to database for {operation} on {table}")
            
            # Simulate connection time
            time.sleep(random.uniform(0.05, 0.15))
            
            with self.create_span("execute_query") as query_span:
                if query_span and OTEL_AVAILABLE:
                    query_span.set_attribute("db.statement", f"SELECT * FROM {table}")
                
                self.logger.info(f"Executing {operation} query on table {table}")
                
                # Simulate query execution
                execution_time = random.uniform(0.1, 0.3)
                time.sleep(execution_time)
                
                rows_affected = random.randint(1, 100)
                self.logger.info(
                    f"Database {operation} completed - Table: {table}, Rows: {rows_affected}, Time: {execution_time*1000:.1f}ms"
                )
                
                if query_span and OTEL_AVAILABLE:
                    query_span.set_attribute("db.rows_affected", rows_affected)
    
    def demonstrate_log_levels(self):
        """Demonstrate different log levels with OpenTelemetry."""
        with self.create_span("log_levels_demo") as span:
            self.logger.debug("This is a DEBUG message - typically for detailed diagnostic info")
            self.logger.info("This is an INFO message - general information about program execution")
            self.logger.warning("This is a WARNING message - something unexpected happened")
            self.logger.error("This is an ERROR message - a serious problem occurred")
            
            # Log with structured data in message format
            self.logger.info(
                "Structured logging example - CPU: 45.2%, Memory: 78.9%, Connections: 12, Tags: [demo, structured, metrics]"
            )
    
    def run_demo(self):
        """Run the complete OpenTelemetry logging demo."""
        print("\n🚀 Starting OpenTelemetry Logging Demo")
        print("=" * 50)
        
        try:
            # Demonstrate log levels
            print("\n📊 Demonstrating different log levels:")
            self.demonstrate_log_levels()
            
            # Simulate user requests
            print("\n👤 Simulating user requests:")
            users = [
                (101, "login"),
                (102, "purchase"),
                (103, "logout"),
                (104, "view_profile")
            ]
            
            for user_id, action in users:
                try:
                    self.simulate_user_request(user_id, action)
                except Exception:
                    pass  # Already logged in simulate_user_request
                
                # Add some delay between requests
                time.sleep(0.2)
            
            # Simulate database operations
            print("\n🗄️  Simulating database operations:")
            db_operations = [
                ("users", "SELECT"),
                ("orders", "INSERT"),
                ("products", "UPDATE"),
                ("inventory", "DELETE")
            ]
            
            for table, operation in db_operations:
                self.simulate_database_operation(table, operation)
                time.sleep(0.1)
            
            print("\n✅ Demo completed successfully!")
            
        except Exception as e:
            self.logger.critical(f"Demo failed with critical error: {str(e)}", exc_info=True)
            raise
        
        finally:
            # Allow time for log processing
            print("\n⏳ Waiting for log processing to complete...")
            time.sleep(2)


def main():
    """Main entry point for the demo application."""
    print("OpenTelemetry Logging Demo Application")
    print("=====================================")
    
    if not OTEL_AVAILABLE:
        print("\n⚠️  OpenTelemetry packages are not installed.")
        print("Install them with: pip install -r requirements.txt")
        print("Running in basic logging mode...\n")
    
    # Create and run the demo
    demo = OpenTelemetryLoggingDemo("otel-logging-demo-app")
    demo.run_demo()
    
    print("\n🎉 All logs have been processed!")
    print("\nKey Features Demonstrated:")
    print("• Structured logging with OpenTelemetry (if packages installed)")
    print("• Trace and span correlation with logs")
    print("• Different log levels (DEBUG, INFO, WARNING, ERROR)")
    print("• Nested spans with automatic logging")
    print("• Custom attributes and metadata")
    print("• Error handling and exception logging")
    print("• Graceful fallback to basic logging")


if __name__ == "__main__":
    main()