#!/bin/bash

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "📚 Downloading NLTK data..."
python -m nltk.downloader punkt stopwords wordnet

echo "📁 Creating data directories if they don't exist..."
mkdir -p data
mkdir -p models

echo "✅ Build complete! Ready for deployment."
