"""
WSGI entry point for production deployment
"""

import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
