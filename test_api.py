"""
Test Script untuk Blockchain API
Script ini menguji semua endpoint API
"""

import requests
import json
import time

# Base URL
BASE_URL = "http://localhost:8001/api"

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response):
    """Print formatted response"""
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_api():
    """Test all API endpoints"""
    
    print_section("🚀 TESTING BLOCKCHAIN API")
    
    # 1. Get initial chain
    print_section("1. Get Initial Blockchain")
    response = requests.get(f"{BASE_URL}/chain")
    print_response(response)
    
    # 2. Get stats
    print_section("2. Get Statistics")
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response)
    
    # 3. Create transactions
    print_section("3. Create Transaction #1")
    response = requests.post(f"{BASE_URL}/transaction", json={
        "sender": "Alice",
        "recipient": "Bob",
        "amount": 50.0
    })
    print_response(response)
    
    print_section("4. Create Transaction #2")
    response = requests.post(f"{BASE_URL}/transaction", json={
        "sender": "Bob",
        "recipient": "Charlie",
        "amount": 30.0
    })
    print_response(response)
    
    print_section("5. Create Transaction #3")
    response = requests.post(f"{BASE_URL}/transaction", json={
        "sender": "Charlie",
        "recipient": "Alice",
        "amount": 20.0
    })
    print_response(response)
    
    # 4. Get pending transactions
    print_section("6. Get Pending Transactions")
    response = requests.get(f"{BASE_URL}/transactions/pending")
    print_response(response)
    
    # 5. Mine block
    print_section("7. Mine Block")
    print("⛏️  Mining... (this may take a few seconds)")
    response = requests.post(f"{BASE_URL}/mine", json={
        "miner_address": "Miner1"
    })
    print_response(response)
    
    # 6. Get updated chain
    print_section("8. Get Updated Blockchain")
    response = requests.get(f"{BASE_URL}/chain")
    print_response(response)
    
    # 7. Validate chain
    print_section("9. Validate Blockchain")
    response = requests.get(f"{BASE_URL}/chain/validate")
    print_response(response)
    
    # 8. Get specific block
    print_section("10. Get Block #1")
    response = requests.get(f"{BASE_URL}/block/1")
    print_response(response)
    
    # 9. Check balances
    print_section("11. Check Alice's Balance")
    response = requests.post(f"{BASE_URL}/balance", json={
        "address": "Alice"
    })
    print_response(response)
    
    print_section("12. Check Miner1's Balance")
    response = requests.post(f"{BASE_URL}/balance", json={
        "address": "Miner1"
    })
    print_response(response)
    
    # 10. Final stats
    print_section("13. Final Statistics")
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response)
    
    print_section("✅ ALL TESTS COMPLETED")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API")
        print("Make sure the server is running:")
        print("  python -m uvicorn app.main:app --reload --port 8001")
    except Exception as e:
        print(f"\n❌ Error: {e}")
