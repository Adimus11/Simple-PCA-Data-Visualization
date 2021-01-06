FROM python:3.8
COPY . /app
RUN apt-get install cuda-cudart-10-1
RUN mkdir /opt/panel
RUN mkdir /opt/panel/images
COPY ./data/ /opt/panel/images/
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
