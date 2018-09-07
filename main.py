import paho.mqtt.client as mqtt
import numpy as np
import cv2  # for resizing image
print("Starting mqtt-amblight")
cap = cv2.VideoCapture(0)

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected to mqtt broker with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mqtt-amblight/")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
# client.username_pw_set("homeassistant", "veiligmijnlichtenbedienen")
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()


def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue


previousColor = ""

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print(frame)
    # print(get_dominant_color(frame))
    # Our operations on the frame come here
    #dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
    data = np.reshape(frame, (-1, 3))
    # print(data.shape)
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
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
        client.publish("mqtt-ambilight/", to_publish)
        previousColor = to_publish
    # else:
    #     print("same color")


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
