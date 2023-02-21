FROM python:3.9-slim
WORKDIR /code
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get -y install \
    python3 python3-dev gcc \
    gfortran musl-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy opencv-python
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt install -y gcc musl-dev
COPY requirements.txt requirements.txt
# Move the default conf out of the way
COPY /nginx/default.conf /etc/nginx/default.conf_orig 
# Copy in your project's new nginx conf
RUN cp flask/default.conf /etc/nginx/default.conf
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]