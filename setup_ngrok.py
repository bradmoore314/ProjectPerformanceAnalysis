#!/usr/bin/env python
"""
This script sets up an ngrok tunnel to your Streamlit app running locally.
Run this script after starting your Streamlit app to create a public URL.

Usage:
1. Start your Streamlit app: streamlit run app.py
2. In a separate terminal, run: python setup_ngrok.py

Requirements: 
- pip install pyngrok
"""

import time
import os
import subprocess
import webbrowser
from pyngrok import ngrok, conf

def setup_ngrok_tunnel(port=8501):
    """
    Set up an ngrok tunnel to the specified port
    """
    # Check if ngrok is installed
    try:
        # Set up ngrok configuration - increase timeout
        conf.get_default().monitor_thread_timeout = 120
        conf.get_default().request_timeout = 120
        
        # Clean any existing tunnels
        try:
            for tunnel in ngrok.get_tunnels():
                ngrok.disconnect(tunnel.public_url)
        except:
            pass
        
        # Start ngrok tunnel
        public_url = ngrok.connect(port).public_url
        
        print("\n" + "=" * 70)
        print(f"🔐 SECURE TUNNEL CREATED!")
        print("=" * 70)
        print(f"🌐 Public URL: {public_url}")
        print(f"🔑 Password: projectpulse123")
        print("\n📱 Share this URL with specific people to give them access to your dashboard")
        print("=" * 70 + "\n")
        
        # Prompt to open in browser
        open_browser = input("Open the URL in your browser? (y/n): ")
        if open_browser.lower() == 'y':
            webbrowser.open(public_url)
        
        print("\nPress Ctrl+C to stop the tunnel when you're done.")
        
        # Keep the tunnel open
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down ngrok tunnel...")
        ngrok.kill()
        print("Tunnel closed.")
    except Exception as e:
        print(f"Error setting up ngrok: {e}")
        
        # Provide instructions to install ngrok if that's the issue
        print("\nIf ngrok is not installed, please follow these steps:")
        print("1. Install the pyngrok package: pip install pyngrok")
        print("2. Run this script again")

if __name__ == "__main__":
    print("\n📊 Project Profit Pulse - Private Sharing Setup")
    print("-----------------------------------------------")
    
    # Ask for the port where Streamlit is running
    port_input = input("Enter the port where your Streamlit app is running (default: 8501): ")
    port = int(port_input) if port_input.strip() else 8501
    
    # Set up the tunnel
    setup_ngrok_tunnel(port) 