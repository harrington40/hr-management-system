#!/usr/bin/env python3
"""
Standalone gRPC Service Runner
Runs only the gRPC service on port 50051
"""

import asyncio
import logging
import signal
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.service_manager import service_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_grpc_service():
    """Run only the gRPC service"""
    try:
        logger.info("🚀 Starting standalone gRPC service...")

        # Initialize services (this will start gRPC on port 50051)
        if not service_manager.initialize_services():
            logger.error("❌ Failed to initialize services")
            return

        logger.info("✅ gRPC service started successfully on port 50051")
        logger.info("🔧 gRPC API available at: localhost:50051")

        # Keep the service running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("🛑 Received shutdown signal...")
    except Exception as e:
        logger.error(f"❌ gRPC service error: {e}")
    finally:
        service_manager.shutdown_services()
        logger.info("✅ gRPC service shutdown complete")

def main():
    """Main entry point"""
    # Handle shutdown signals
    def signal_handler(signum, frame):
        logger.info(f"📴 Received signal {signum}, shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        asyncio.run(run_grpc_service())
    except KeyboardInterrupt:
        logger.info("👋 gRPC service terminated by user")
    except Exception as e:
        logger.error(f"💥 Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()