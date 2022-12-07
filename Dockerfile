FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y wget \
    && apt-get install -y git \
    && apt-get install -y gcc \
    && apt-get clean 


COPY ./env_config.yml /app/env_config.yml
COPY ./requirements.txt /app/requirements.txt


RUN conda env create -f /app/env_config.yml 


#SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit","run","main.py"]
