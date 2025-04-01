#!/usr/bin/env python3
"""
This script creates a localtunnel to your existing Streamlit app.
Localtunnel doesn't require authentication and provides a public URL.
"""

import os
import time
import subprocess
import webbrowser

def create_public_url(port=8575):
    """
    Create a localtunnel to expose the Streamlit app
    """
    print("\n" + "=" * 70)
    print(f"🔄 Creating public URL for your Streamlit app on port {port}")
    print("=" * 70)
    
    # First make sure localtunnel is installed
    try:
        # Check if npx is available
        subprocess.run(["which", "npx"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ npx not found. Please install Node.js first:")
        print("Visit: https://nodejs.org/en/download/")
        return
    
    # Create the tunnel using localtunnel
    process = subprocess.Popen(
        ["npx", "localtunnel", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Wait for the URL to be generated
    url = None
    for line in process.stdout:
        if "your url is:" in line.lower():
            url = line.split("is:")[1].strip()
            break
    
    if not url:
        print("❌ Failed to create public URL")
        return
    
    print("\n" + "=" * 70)
    print("✅ PUBLIC URL CREATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"🌐 Public URL: {url}")
    print(f"🔑 Password: projectpulse123")
    print("\n📱 Share this URL with specific people to give them access")
    print("=" * 70)
    
    # Keep the tunnel open
    try:
        print("\nPress Ctrl+C to stop the tunnel...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down tunnel...")
        process.terminate()
        print("Tunnel closed.")

if __name__ == "__main__":
    create_public_url(8575) 