#!/usr/bin/env python3
"""
HRMS Dual Service Runner
Runs both FastAPI (port 8000) and gRPC (port 50051) services concurrently
"""

import asyncio
import logging
import signal
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.service_manager import service_manager
import uvicorn
from main import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DualServiceRunner:
    """Runs both FastAPI and gRPC services concurrently"""

    def __init__(self):
        self.fastapi_task = None
        self.grpc_task = None
        self.running = False

    async def start_grpc_service(self):
        """Start gRPC service on port 50051"""
        try:
            logger.info("Starting gRPC service on port 50051...")
            # gRPC service is already initialized in service_manager
            # Keep it running indefinitely
            while self.running:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"gRPC service error: {e}")

    async def start_fastapi_service(self):
        """Start FastAPI service on port 8000"""
        try:
            logger.info("Starting FastAPI service on port 8000...")
            # Use uvicorn programmatically
            config = uvicorn.Config(
                app=app,
                host="0.0.0.0",
                port=8000,
                log_level="info"
            )
            server = uvicorn.Server(config)
            await server.serve()
        except Exception as e:
            logger.error(f"FastAPI service error: {e}")

    async def run_services(self):
        """Run both services concurrently"""
        self.running = True

        try:
            # Initialize all services (including gRPC)
            logger.info("Initializing all HRMS services...")
            if not service_manager.initialize_services():
                logger.error("Failed to initialize services")
                return

            logger.info("✅ All services initialized successfully")
            logger.info("🚀 Starting dual service mode:")
            logger.info("   📱 FastAPI Web UI: http://localhost:8000/hrmkit/")
            logger.info("   🔧 gRPC API: localhost:50051")

            # Create tasks for both services
            self.grpc_task = asyncio.create_task(self.start_grpc_service())
            self.fastapi_task = asyncio.create_task(self.start_fastapi_service())

            # Run both tasks concurrently
            await asyncio.gather(
                self.grpc_task,
                self.fastapi_task,
                return_exceptions=True
            )

        except KeyboardInterrupt:
            logger.info("Received shutdown signal...")
        except Exception as e:
            logger.error(f"Error running services: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Shutdown both services gracefully"""
        logger.info("Shutting down services...")
        self.running = False

        # Cancel tasks
        if self.grpc_task and not self.grpc_task.done():
            self.grpc_task.cancel()
        if self.fastapi_task and not self.fastapi_task.done():
            self.fastapi_task.cancel()

        # Shutdown service manager
        service_manager.shutdown_services()

        logger.info("✅ Services shutdown complete")

def main():
    """Main entry point"""
    runner = DualServiceRunner()

    # Handle shutdown signals
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(runner.shutdown())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the services
    try:
        asyncio.run(runner.run_services())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()