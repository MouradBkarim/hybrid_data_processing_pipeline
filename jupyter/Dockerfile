FROM jupyter/pyspark-notebook:spark-3.4.1

USER root

RUN pip install \
    delta-spark==2.4.0 \
    papermill \
    pandas \
    psycopg2-binary \
    flask

COPY start.sh /home/jovyan/start.sh
RUN chmod +x /home/jovyan/start.sh

COPY notebook_server.py /home/jovyan/notebook_server.py

RUN mkdir -p /mnt/s3mock && \
    chown -R jovyan:users /mnt/s3mock

ENV PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 pyspark-shell"
    
USER jovyan
CMD ["/bin/bash", "/home/jovyan/start.sh"]
