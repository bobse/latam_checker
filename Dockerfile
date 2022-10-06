# pull official base image
FROM python:3.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app

# create the appropriate directories
# set work directory
WORKDIR $APP_HOME

# create the app user
RUN addgroup -S app && adduser -S app -G app


# install dependencies
COPY ./requirements.txt $APP_HOME
RUN apk add build-base

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# copy project
COPY . $APP_HOME

EXPOSE 8000

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app


#CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

#Using gunicorn to handle concurrency during search. Otherwirse the uvicorn crashes
CMD gunicorn --bind 0.0.0.0:8000 "main:app" -k uvicorn.workers.UvicornWorker
