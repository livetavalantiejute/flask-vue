# build
FROM node:alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
COPY ./client/vite*.json ./
RUN npm install
COPY ./client .
RUN npm run build

# production
# FROM nginx:stable-alpine as production
# WORKDIR /app
# RUN apk update && apk add --no-cache python3 && \
#     python3 -m ensurepip && \
#     rm -r /usr/lib/python*/ensurepip && \
#     pip3 install --upgrade pip setuptools && \
#     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
#     if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
#     rm -r /root/.cache
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# COPY --from=build-vue /app/dist /usr/share/nginx/html
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
# COPY ./server/requirements.txt .
# RUN pip install -r requirements.txt
# EXPOSE 5000
# RUN pip install gunicorn
# COPY ./server .
# CMD gunicorn -b 0.0.0.0:5000 app:app --daemon && \
#       sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
#       nginx -g 'daemon off;'

# FROM python:3.9-slim
# WORKDIR /code
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# RUN apt-get -y install \
#     python3 python3-dev gcc \
#     gfortran musl-dev
# RUN pip install --upgrade pip setuptools wheel
# RUN pip install numpy opencv-python
# COPY ./server/main.py main.py
# COPY ./server/data.json data.json
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
# ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apt install -y gcc musl-dev
# COPY ./server/requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . .
# CMD ["flask", "run"]


# production
FROM nginx:1.20-alpine as production
WORKDIR /app
RUN apk update && apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN apk update && apk add ffmpeg libc-dev libffi-dev gfortran
RUN apk update && apk add postgresql-dev gcc g++ python3-dev musl-dev
RUN apk add build-base
RUN pip3 install numpy==1.24.0
# RUN pip install setuptools==60.8.2
# RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -U opencv-python==4.5.5.62
RUN python -m pip install --user --upgrade pip
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
RUN pip install gunicorn
COPY ./server .
CMD gunicorn -b 0.0.0.0:5000 app:app --daemon && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'