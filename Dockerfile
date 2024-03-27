# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.9

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/code/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

COPY --chmod=777 ./src/db.sqlite3 /code/src/db.sqlite3

# port where the Django app runs  
EXPOSE 7860



RUN chmod 777 src/db.sqlite3

# start server  
CMD python src/manage.py runserver 0.0.0.0:7860
