FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt 

RUN pip install -r /tmp/requirements.txt

CMD ["voila","--port","$PORT","--no-browser","--show_tracebacks","True" 
