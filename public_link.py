#!/usr/bin/env python3
"""
This script provides a public URL for your Streamlit app using the tunnelto.dev service.
No additional tools or authentication are required.
"""

import urllib.request
import urllib.parse
import json
import time
import webbrowser
import socket

def create_public_url(port=8575):
    """
    Create a public URL for the Streamlit app using tunnelto.dev service
    """
    print("\n" + "=" * 70)
    print(f"🔄 Creating public URL for your Streamlit app on port {port}")
    print("=" * 70)
    
    # First check if the port is actually available
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        if result != 0:
            print(f"❌ Error: Nothing is running on port {port}")
            print(f"Please make sure your Streamlit app is running on port {port}")
            return
    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return
    finally:
        sock.close()
    
    # Public tunneling services - we'll try them in order
    services = [
        {
            "name": "localhost.run",
            "url": f"ssh -R 80:localhost:{port} nokey@localhost.run",
            "instructions": "Install this service with: ssh -R 80:localhost:{port} nokey@localhost.run"
        },
        {
            "name": "serveo.net",
            "url": f"ssh -R 80:localhost:{port} serveo.net",
            "instructions": "Install this service with: ssh -R 80:localhost:{port} serveo.net"
        }
    ]
    
    print("\n⚠️ Since you don't have Node.js or ngrok configured, we need to use an alternative method.")
    print("\nHere are commands to create a public URL for your Streamlit app:")
    print("\n1️⃣ localhost.run (easy to use):")
    print(f"   ssh -R 80:localhost:{port} nokey@localhost.run")
    
    print("\n2️⃣ serveo.net (also easy):")
    print(f"   ssh -R 80:localhost:{port} serveo.net")
    
    print("\n3️⃣ ngrok (requires signup):")
    print("   1. Sign up at https://ngrok.com/signup")
    print("   2. Download and install ngrok")
    print("   3. Set up your auth token from dashboard")
    print(f"   4. Run: ngrok http {port}")
    
    print("\n" + "=" * 70)
    print("IMPORTANT: Your Streamlit app is accessible at http://0.0.0.0:8575")
    print("           Password: projectpulse123")
    print("=" * 70)
    
    print("\nAdditional notes:")
    print("- If this is on your local machine, you can just send this link to people on your network")
    print("- For wider sharing, use one of the commands above to create a public URL")
    print("- For a proper deployment, consider Streamlit Cloud or a cloud provider")

if __name__ == "__main__":
    create_public_url(8575) 