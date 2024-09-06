FROM python:3.12-bullseye
RUN apt update && \
    apt upgrade -y && \
    apt install -y sudo curl
ENV SHELL=bash PYTHONPATH=/home/node/works/puzzle_dsl_interpreter
ARG USERNAME=node
RUN curl -sSfL https://raw.githubusercontent.com/itkmaingit/my-config/main/docker/setup_user.sh | bash -s $USERNAME

USER $USERNAME
WORKDIR /home/"$USERNAME"/works
COPY ./works/setup.sh ./setup.sh

RUN bash /home/$USERNAME/works/setup.sh $USERNAME
