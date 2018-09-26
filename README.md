# MQTT ambilight

Docker application to get the average color of a webcam/video capture device and broadcast it over MQTT

## How to use

Get it on DockerHub:

- Regular version: https://hub.docker.com/r/whitebird/mqtt-ambilight-rpi/
- Raspberry Pi version: https://hub.docker.com/r/whitebird/mqtt-ambilight/

To run the application:

- Copy `configuration.example.yaml` to `configuration.example.yaml` and add your mqtt details.
- Run it with a command like this: 

```
docker run -it \
    -v ~/mqtt-ambilight/configuration.yaml:/configuration.yaml \
    --device=/dev/video0:/dev/video0 \
    --net="host" \
    -t mqtt-ambilight
```

