import paho.mqtt.client as mqtt
import numpy as np
import cv2
import yaml
import time
import sys

print("Starting mqtt-amblight")

try:
    with open("configuration.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    server = cfg['mqtt']['server']
    base_topic = cfg['mqtt']['base_topic']
    light_topic = cfg['mqtt']['light_topic']
    user = None
    password = None
    wait_time = cfg['wait_time']
    webcam_index = cfg['webcam_index']
    run_analyzer = cfg['analyze_on_start']

    if 'user' in cfg['mqtt'] and 'password' in cfg['mqtt']:
        print('user and password found in configuration')
        user = cfg['mqtt']['user']
        password = cfg['mqtt']['password']

    cap = cv2.VideoCapture(webcam_index)
    if not cap.isOpened():
        raise Exception('Invalid video capture/webcam index')
except IOError as e:
    sys.exit('configuration.yaml not found in mounted config directory. Copy configuration.example.yaml to get started.')
except Exception as e:
    sys.exit(e)


def on_connect(client, userdata, flags, rc):
    global run_analyzer
    print("Connected to mqtt broker with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(base_topic + "power")
    print("Starting webcam analysis")
    run_analyzer = True


def on_message(client, userdata, msg):
    global base_topic
    global run_analyzer
    if base_topic + "power" == msg.topic:
        message = int(msg.payload)
        if message == 0:
            print("Turning off")
            run_analyzer = False
        elif message == 1:
            print("Turning on")
            run_analyzer = True
        elif message == 2:
            print("Toggling power")
            run_analyzer = not run_analyzer


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if user != None and password != None:
    client.username_pw_set(user, password)

print("Connecting to mqtt broker " + server)
client.connect(server, 1883, 60)
client.loop_start()


previousColor = ""
while True:
    if run_analyzer:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print(frame)
        # print(get_dominant_color(frame))
        # Our operations on the frame come here
        #dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
        data = np.reshape(frame, (-1, 3))
        # print(data.shape)
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(
            data, 1, None, criteria, 10, flags)

        bgr = centers[0].astype(np.int32)
        rgb = bgr[..., ::-1]
        rgb_hex = hex(sum([j*256**i for i, j in enumerate(rgb)]))
        to_publish = '#' + str(rgb_hex)[2:]

        if to_publish != previousColor:
            # print(to_publish)
            # print('Dominant color is: bgr({})'.format(centers[0].astype(np.int32)))
            client.publish(light_topic, to_publish)
            client.publish(base_topic + "color", to_publish)
            previousColor = to_publish
            time.sleep(wait_time)
    # else:
        #     print("same color")

# When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()
