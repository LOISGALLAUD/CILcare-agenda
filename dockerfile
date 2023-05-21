FROM python:3.10

WORKDIR /agenda_app

COPY . /agenda_app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
