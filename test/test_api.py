import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    test_cases = [
        {
            "name": "Example A",
            "data": ["a", "1", "334", "4", "R", "$"]
        },
        {
            "name": "Example B", 
            "data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]
        },
        {
            "name": "Example C",
            "data": ["A", "ABcD", "DOE"]
        }
    ]
    
    print("Testing BFHL API\n")
    
    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        print(f"Input: {test_case['data']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/bfhl",
                json={"data": test_case['data']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(result, indent=2)}")
            else:
                print(f"Status: {response.status_code}")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Connection Error: Make sure the API server is running!")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)

def test_root():
    print("Testing Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("Root endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"Root endpoint error: {str(e)}")
    print("-" * 50)

if __name__ == "__main__":
    print("BFHL API Test Suite")
    print("=" * 50)
    
    test_root()
    test_api()
    
    print("\nTesting completed!")
    print("\nTo test manually:")
    print('curl -X POST "http://localhost:8000/bfhl" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"data": ["a","1","334","4","R", "$"]}\'')