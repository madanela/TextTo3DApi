import uvicorn
from argparse import ArgumentParser

from app import app

if __name__ == "__main__":
    # Create an argument parser for CLI options
    parser = ArgumentParser(description="Run the FastAPI server")
    parser.add_argument('--host', type=str, default="0.0.0.0", help='Host to run the FastAPI server on (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the FastAPI server on (default: 8000)')
    
    # Parse CLI arguments
    args = parser.parse_args()

    # Run the Uvicorn server with the provided host and port
    uvicorn.run(app, host=args.host, port=args.port)