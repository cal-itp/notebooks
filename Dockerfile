FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt 

RUN pip install -r /tmp/requirements.txt

EXPOSE 8888
EXPOSE 3838

WORKDIR /root/work

CMD ["voila","--port=8080","--no-browser","--show_tracebacks=True"] 
