"""
EduSolve AI - Application Entry Point
Run this file to start the Flask server
"""

import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.config import Config

if __name__ == '__main__':
    # Create Flask app
    app = create_app()
    
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║           🚀 EduSolve AI - Starting Server 🚀          ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    print(f"📍 Server running at: http://{Config.HOST}:{Config.PORT}")
    print(f"🎯 Environment: {Config.FLASK_ENV}")
    print(f"🤖 AI Model: {Config.GROQ_MODEL}")
    print("\n💡 Open your browser and navigate to http://localhost:5000")
    print("⚠️  Press CTRL+C to stop the server\n")
    
    # Run Flask app
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
