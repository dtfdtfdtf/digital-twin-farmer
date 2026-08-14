import requests
import json

url = "http://localhost:8000/api/farmers"

data = {
    "first_name": "Test",
    "last_name": "Farmer",
    "phone": "0888999777",
    "national_id": "TEST123456",
    "village": "Chilumba",
    "district": "Lilongwe",
    "region": "Central"
}

print("Sending POST request to /api/farmers")
print("Data:", json.dumps(data, indent=2))

try:
    response = requests.post(url, json=data)
    print("\nStatus Code:", response.status_code)
    print("Response:", response.text)
    
    if response.status_code == 201:
        print("\n✅ Farmer created successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("\n❌ Error occurred")
        
except Exception as e:
    print("Exception:", e)