from typing import Self
import paho.mqtt.client as mqtt
import json
import time
import firebase_admin
from numpy import mean
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

MQTT_SERVER = "192.168.168.171"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "msg/info"
mqtt_client = mqtt.Client()

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('Desktop/serviceAccount.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
# 當伺服器收到訊息要做的動作
def on_message(client, userdata, msg):
    print(f"{msg.topic} - Temp: {json.loads(msg.payload)['Temp']}, Humidity: {json.loads(msg.payload)['Humidity']}")
    temp = float(f"{json.loads(msg.payload)['Temp']}")
    hunidity = float(f"{json.loads(msg.payload)['Humidity']}")
    date = datetime.now().strftime("%Y/%m/%d")
    dtime=datetime.now().strftime("%H:%M")
   #製作時間搓
    nowTime = time.time()
    
    doc = {
        'temp': temp,
        'hunidity': hunidity,
        'date': date,
        'TS': nowTime,
        'time':dtime
    }
    clo_ref = db.collection("Min")
    clo_ref.add(doc)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
mqtt_client.loop_forever()