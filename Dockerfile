FROM python:latest

LABEL author="Abner Andino"
LABEL github="https://github.com/bighelmet7"

RUN mkdir /opt/indigo

COPY . /opt/indigo

WORKDIR /opt/indigo

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["app.py"]

