FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /eurovision

COPY ./eurovision .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

