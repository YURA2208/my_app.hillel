FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNDUFFERED 1
WORKDIR /my_app
COPY ./requirements.txt /my_app

RUN pip install -r /my_app/requirements.txt
COPY . /my_app
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
