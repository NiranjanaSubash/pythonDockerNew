FROM python:3.12

WORKDIR /docker_project

COPY main.py .
COPY requirements.txt  .
COPY instance/cafes.db instance/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]