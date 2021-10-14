# Dockerfile, image, container
FROM python:3.8-slim

ADD HL_GG_Proto.py . txnlog.dat .

RUN pip install numpy pandas

CMD ["python", "./HL_GG_Proto.py"]