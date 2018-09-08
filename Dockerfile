FROM mohaseeb/raspberrypi3-python-opencv:latest

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY "main.py" /
CMD [ "python", "main.py" ]