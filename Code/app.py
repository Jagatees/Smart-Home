from flask import Flask, request, jsonify, render_template, Response
from flask_mqtt import Mqtt
import requests
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '192.168.1.124'  # Replace with your MQTT broker URL
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0
streamurl = "192.168.1.73" #replace with streamer pi url

mqtt = Mqtt(app)

# Global variable to store the latest MQTT message
latest_message = ""

@app.route('/')
def index():
    return render_template('index.html', message=latest_message)

@app.route('/publish')
def publish():
    mqtt.publish('test/topic', 'Hello from Flask')
    return 'Message sent to MQTT'

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.form
    message = data.get('message')
    mqtt.publish('test/topic', message)
    return jsonify({"status": "Message sent to MQTT", "message": message})

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt.subscribe('test/topic')  # Subscribe to the topic where you expect messages

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global latest_message
    topic = message.topic
    payload = message.payload.decode('utf-8')
    print(f"Received message '{payload}' on topic '{topic}'")

    # Update the latest_message variable with the received message
    latest_message = payload

@app.route('/video_feed')
def video_feed():
    stream_url = 'http://'+streamurl+':5000/video_feed'

    def generate():
        with requests.get(stream_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
