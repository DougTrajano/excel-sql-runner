# base image
FROM python:3.8

# making directory of app
RUN mkdir /app
WORKDIR /app

# copy over requirements
COPY requirements.txt /app/

# install pip then packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --upgrade

# copying all files over
COPY . /app/

ENV PYTHONPATH="${PYTHONPATH}:/app"

# exposing default port for streamlit
EXPOSE 8501

# cmd to launch app when container is run
CMD streamlit run main.py