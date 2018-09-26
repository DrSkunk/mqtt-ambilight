docker run -it \
    -v ~/mqtt-ambilight/configuration.yaml:/configuration.yaml \
    --device=/dev/video0:/dev/video0 \
    --net="host" \
    -t mqtt-ambilight
