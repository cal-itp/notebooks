FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt 

RUN pip install -r /tmp/requirements.txt

EXPOSE 8888
EXPOSE 3838
EXPOSE 8080

WORKDIR "/app"
CMD ["voila","--port=8080","--no-browser","--show_tracebacks=True"] 
