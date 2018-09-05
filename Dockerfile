FROM jjanzic/docker-python3-opencv

COPY "main.py" /
CMD [ "python", "main.py" ]