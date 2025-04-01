#!/usr/bin/env python3
"""
This script creates an ngrok tunnel to your existing Streamlit app.
"""

import time
from pyngrok import ngrok, conf

def create_tunnel(port=8575):
    """
    Create an ngrok tunnel to an existing Streamlit app
    """
    print("\n" + "=" * 70)
    print("🔄 Creating secure tunnel to your Streamlit app on port", port)
    print("=" * 70)
    
    # Configure ngrok
    conf.get_default().monitor_thread_timeout = 120
    conf.get_default().request_timeout = 120
    
    # Close any existing tunnels
    tunnels = ngrok.get_tunnels()
    for tunnel in tunnels:
        print(f"Closing existing tunnel: {tunnel.public_url}")
        ngrok.disconnect(tunnel.public_url)
    
    # Create a new tunnel
    public_url = ngrok.connect(port).public_url
    
    print("\n" + "=" * 70)
    print("✅ TUNNEL CREATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"🌐 Public URL: {public_url}")
    print(f"🔑 Password: projectpulse123")
    print("\n📱 Share this URL with specific people to give them access")
    print("=" * 70)
    
    # Keep the tunnel open
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down tunnel...")
        ngrok.kill()
        print("Tunnel closed.")

if __name__ == "__main__":
    create_tunnel(8575) 