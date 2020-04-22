FROM python:3.8.1
EXPOSE 8000
WORKDIR /opt/app
COPY . .
RUN apt-get update
RUN apt-get -y install potrace unrar-free
RUN pip3 install --no-cache-dir -e .
CMD ["uvicorn", "--host", "0.0.0.0", "aocrecs.main:APP"]
