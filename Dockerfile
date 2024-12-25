FROM ubuntu:25.04
RUN apt-get update && apt-get install -y curl python3.12 python3.12-venv
COPY requirements.txt .
RUN python3.12 -m venv /opt/python/.venv
RUN /opt/python/.venv/bin/pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"]