FROM swr.cn-east-3.myhuaweicloud.com/cloud-course-2023112556-2023112429/pyspark:v9

WORKDIR /opt/spark/work-dir

COPY spark-jobs/douban_spark_analysis.py /opt/spark/work-dir/douban_spark_analysis.py
COPY spark-jobs/douban_spark_analysis_v2.py /opt/spark/work-dir/douban_spark_analysis_v2.py
COPY spark-jobs/wordcount.py /opt/spark/work-dir/wordcount.py

COPY datasets/raw/douban_movies.csv /opt/spark/work-dir/data/douban_movies.csv
COPY datasets/raw/sample.txt /opt/spark/work-dir/data/sample.txt

USER root
RUN chmod 644 /opt/spark/work-dir/douban_spark_analysis.py && \
    chmod 644 /opt/spark/work-dir/douban_spark_analysis_v2.py && \
    chmod 644 /opt/spark/work-dir/wordcount.py && \
    chmod 644 /opt/spark/work-dir/data/douban_movies.csv && \
    chmod 644 /opt/spark/work-dir/data/sample.txt

USER 185
