FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt 

RUN pip install /tmp/requirements.txt
