FROM python:3.10.6-alpine

RUN apk update

RUN pip install --upgrade pip

WORKDIR /app

RUN python -m venv venv/
RUN . venv/bin/activate

RUN apk add gcc python3-dev musl-dev libffi-dev g++

COPY requirements.txt .

RUN pip3 install -r requirements.txt


COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]