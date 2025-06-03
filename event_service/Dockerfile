FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 🔧 ESTE é o ponto importante:
CMD ["python", "consumer.py"]
