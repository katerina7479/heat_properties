FROM tiangolo/uwsgi-nginx:python2.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "-u", "app.py"]
