FROM python:3
ARG BASE \
    AWSCLI=https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip

RUN apt-get update
RUN apt-get -y install locales less && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8 
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

#
WORKDIR ${BASE}
#
RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false

#
COPY pyproject.toml poetry.lock README.md ${BASE}/
COPY figma_files/ ${BASE}/figma_files/
RUN poetry install

