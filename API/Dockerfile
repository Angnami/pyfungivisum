FROM debian:latest

WORKDIR /app

COPY . .

RUN apt update && apt install python3-pip  -y  
RUN apt update && apt install python3-opencv -y libopencv-dev
RUN pip install --upgrade pip
RUN pip install tensorflow
RUN pip install -r requirements.txt

EXPOSE 9000

CMD uvicorn main:app --host 0.0.0.0 --port 9000



