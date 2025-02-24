FROM flink:1.19.1-scala_2.12-java11
# Add dependency jars
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.2.0-1.19/flink-connector-kafka-3.2.0-1.19.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-avro/1.19.1/flink-avro-1.19.1.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-avro-confluent-registry/1.19.1/flink-avro-confluent-registry-1.19.1.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.5.jar \
    https://repo1.maven.org/maven2/org/apache/avro/avro/1.11.4/avro-1.11.4.jar \
    https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar \
    https://repo1.maven.org/maven2/com/google/guava/guava/33.1.0-jre/guava-33.1.0-jre.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.7.1/kafka-clients-3.7.1.jar \
    https://packages.confluent.io/maven/io/confluent/kafka-schema-registry-client/7.7.1/kafka-schema-registry-client-7.7.1.jar \
    https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.16.1/jackson-core-2.16.1.jar \
    https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.16.1/jackson-databind-2.16.1.jar \
    https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.16.1/jackson-annotations-2.16.1.jar \
    /opt/flink/jars/

COPY requirements.txt .

# Install Python 3.11 version
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && apt-get install -y python3.11 python3.11-venv \
    && python3.11 -m venv /opt/python/.venv \
    && /opt/python/.venv/bin/pip install -r requirements.txt
