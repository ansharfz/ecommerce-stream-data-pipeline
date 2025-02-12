FROM flink:1.19.1-scala_2.12-java11

ADD https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.3.0-1.19/flink-sql-connector-kafka-3.3.0-1.19.jar \
    /opt/flink/lib/flink-sql-connector-kafka-3.3.0-1.19.jar 

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && apt-get install -y python3.11 python3.11-venv \
    && python3.11 -m venv /opt/python/.venv \
    && /opt/python/.venv/bin/pip install -r requirements.txt \
    && . /opt/python/.venv/bin/activate
