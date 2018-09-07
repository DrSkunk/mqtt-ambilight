FROM jjanzic/docker-python3-opencv

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY "main.py" /
CMD [ "python", "main.py" ]