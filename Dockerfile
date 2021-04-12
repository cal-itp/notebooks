FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt 

RUN pip install -r /tmp/requirements.txt

CMD ["voila","--port=8080","--no-browser","--show_tracebacks=True"] 
