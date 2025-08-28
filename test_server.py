#!/usr/bin/env python
import requests
import time

def test_server():
    """Test if Django server is running"""
    try:
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test the main page
        response = requests.get('http://localhost:8000/', timeout=10)
        print(f"Server Status: {response.status_code}")
        print(f"Response length: {len(response.text)}")
        
        if response.status_code == 200:
            print("✅ Server is running successfully!")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - it may not be running")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    test_server()
