from flask import Flask, render_template, request
import requests
import json
import hashlib

app = Flask(__name__, template_folder='D:/VacronGMS/server/Python/GMS_API_TEST_HTML/start/templates')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/result', methods=['POST'])
def result():
    ip = request.form['ip']
    username = request.form['username']
    password = request.form['password']
    deviceid = request.form['deviceid']

    result = send_device_request(ip, username, password, deviceid)
    return render_template('result.html', result=result)

def send_device_request(ip, username, password, deviceid):
    hashed_password = hashlib.sha256(password.encode()).hexdigest().upper()
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    data = {
        "username": username,
        "password": hashed_password,
        "deviceid": deviceid
    }
    gms_ip = ip.rstrip("/")
    url = f"{gms_ip}/gkdevice/device"
    
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return f"HTTP 請求失敗，狀態碼：{response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
