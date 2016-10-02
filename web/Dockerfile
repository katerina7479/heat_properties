FROM tiangolo/uwsgi-nginx:python2.7

# Turn off output buffering in Python.
ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "-u", "app.py"]
