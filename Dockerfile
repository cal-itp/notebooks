FROM jupyter/datascience-notebook

COPY ./requirements.txt /tmp/requirements.txt 

RUN pip install -r /tmp/requirements.txt

EXPOSE 8888
EXPOSE 3838
EXPOSE 8080

WORKDIR "/app"

COPY . /app

 
# Note that using linebreaks with CMD appears impossible when using []
# see https://stackoverflow.com/q/46469821/1144523
CMD voila \
     --port=8080 --no-browser --show_tracebacks=True \
     --VoilaConfiguration.file_whitelist="['.*\.(png|jpg|gif|svg|mp4|avi|ogg|csv)']" \
     --TagRemovePreprocessor.remove_cell_tags hide \
     --TagRemovePreprocessor.remove_cell_tags dummy-hide
