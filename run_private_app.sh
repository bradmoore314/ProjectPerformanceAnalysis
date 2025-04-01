#!/bin/bash

# Script to run the Project Profit Pulse app privately
# This script starts the Streamlit app and creates a secure ngrok tunnel

echo "🚀 Starting Project Profit Pulse dashboard..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking required packages..."
python3 -m pip install -q streamlit pandas numpy plotly matplotlib scikit-learn pyngrok

# Run Streamlit in the background
echo "📊 Starting Streamlit server..."
streamlit run app.py --server.port 8501 &
streamlit_pid=$!

# Wait for Streamlit to start
echo "⏳ Waiting for Streamlit to start..."
sleep 5

# Create ngrok tunnel
echo "🔐 Creating secure tunnel with ngrok..."
python3 setup_ngrok.py

# When the user exits ngrok (Ctrl+C), kill the Streamlit process
echo "🛑 Shutting down Streamlit server..."
kill $streamlit_pid

echo "✅ Project Profit Pulse has been shut down." 