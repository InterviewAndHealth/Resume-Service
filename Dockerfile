FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

ENV ENV=production

COPY ./app /code/app

CMD ["python", "-m", "app"]