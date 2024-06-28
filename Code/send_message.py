import requests

# Flask application URL
flask_url = 'http://192.168.240.1:1883'  # Replace with your Flask application URL

# Example message to send
message = "Hello from Python script!"

# Data to send in POST request
data = {
    'message': message
}

try:
    # Send POST request to Flask application
    response = requests.post(flask_url, data=data)

    # Check if request was successful
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
