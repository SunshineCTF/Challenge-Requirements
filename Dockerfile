FROM python:3.8

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY check.py .

ENTRYPOINT ["python3", "check.py"]