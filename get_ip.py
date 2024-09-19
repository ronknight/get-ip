import socket
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json()['ip']
    except requests.RequestException:
        ip = "Unable to get external IP"
    return ip

def get_location(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        return response.json()
    except requests.RequestException:
        return {"error": "Unable to get location information"}

@app.route('/')
def index():
    local_ip = get_local_ip()
    external_ip = get_external_ip()
    location = get_location(external_ip)
    return render_template('index.html', local_ip=local_ip, external_ip=external_ip, location=location)

@app.route('/api/ip')
def api_ip():
    return jsonify({
        'local_ip': get_local_ip(),
        'external_ip': get_external_ip()
    })

@app.route('/api/location')
def api_location():
    external_ip = get_external_ip()
    return jsonify(get_location(external_ip))

if __name__ == '__main__':
    local_ip = get_local_ip()
    external_ip = get_external_ip()
    print(f"Your local IP address is: {local_ip}")
    print(f"Your external IP address is: {external_ip}")
    app.run(debug=True, host='0.0.0.0')