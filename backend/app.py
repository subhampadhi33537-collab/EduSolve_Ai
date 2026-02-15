"""
EduSolve AI - Flask Application Entry Point
Main application factory and configuration
"""

import os
import sys
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from routes import api

def create_app():
    """
    Application factory function
    Creates and configures the Flask application
    
    Returns:
        Flask: Configured Flask application instance
    """
    
    # Define paths for templates and static files (relative to project root)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(project_root, 'frontend', 'templates')
    static_dir = os.path.join(project_root, 'frontend', 'static')
    
    # Create Flask application with correct paths
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir,
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS (Cross-Origin Resource Sharing) for frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(api)
    
    # =====================================================
    # Page Routes (Multi-page Navigation)
    # =====================================================
    
    @app.route('/')
    def index():
        """Serve the home page"""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Render dashboard page with analytics"""
        return render_template('dashboard.html')
    
    @app.route('/features')
    def features():
        """Render features showcase page"""
        return render_template('features.html')
    
    @app.route('/about')
    def about():
        """Render about page"""
        return render_template('about.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('index.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        print(f"Server error: {error}")
        return {"status": "error", "message": "Internal server error"}, 500
    
    # Logging
    print(f"Flask Environment: {Config.FLASK_ENV}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Groq Model: {Config.GROQ_MODEL}")
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run()
    # Run the Flask development server
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
