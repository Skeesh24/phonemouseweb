FROM python:3.12-slim-bullseye

COPY . .

RUN pip install -r requirements.txt --no-cache

ENTRYPOINT ["python3.12", "src/main.py"]
