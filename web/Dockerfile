FROM tiangolo/uwsgi-nginx:python2.7

# Turn off output buffering in Python.
ENV PYTHONUNBUFFERED=1

# Copy & install requirements first, for caching
RUN mkdir app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

# Copy the rest
COPY . /app
WORKDIR /app

EXPOSE 5000
CMD ["python", "-u", "app.py"]
