import requests

BASE_URL = "http://127.0.0.1:5000" 

def test_update_storage(tag_id, storage_id):
    url = f"{BASE_URL}/update_storage/{tag_id}"
    payload = {"storage_id": storage_id}
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        print(f"Success: {response.json()}")
    else:
        print(f"Error {response.status_code}: {response.json()}")

if __name__ == "__main__":
    # Test cases
    print("Test 1: Assign instrument with tag_id=1 to storage_id=2")
    test_update_storage(tag_id=1, storage_id=2)

    print("\nTest 2: Assign instrument with tag_id=1 to a non-existent storage_id=999")
    test_update_storage(tag_id=1, storage_id=999)

    print("\nTest 3: Assign a non-existent instrument with tag_id=999 to storage_id=2")
    test_update_storage(tag_id=999, storage_id=2)

    print("\nTest 4: Remove storage from instrument with tag_id=1 (set storage_id=None)")
    test_update_storage(tag_id=1, storage_id=None)