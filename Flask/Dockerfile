FROM python:3.10.7-slim-buster

# set work directory
ENV APP_HOME /app
WORKDIR $APP_HOME
# set the port
ENV PORT 5000

# allow statements and log message to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .
# Install additional dependencies and run the commands
RUN apt-get update \
    && apt-get install -y wget \
    && wget https://raw.githubusercontent.com/Agney-gt/google-compute-engine-selenium/master/install.sh \
    && chmod +x install.sh \
    && ./install.sh \
    && chmod +x start_headless.sh \
    && ./start_headless.sh \
    && chmod +x demo.py \
    && ./demo.py
EXPOSE 5000

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 GoodReadsAPI:app
