FROM python:3.9.7

WORKDIR /app
COPY app/ .

RUN pip install -r requirements.txt

COPY src/ src/
COPY data/databases data/
COPY data/tag_definitions.csv data/

RUN chmod +x run.sh
CMD ["./run.sh"]
