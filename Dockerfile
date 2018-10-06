FROM python:3.7

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc
RUN echo "python -m pytest" >> /root/.bash_history

WORKDIR /app

RUN pip install -U pip

ADD requirements.txt /app
ADD requirements-dev.txt /app

RUN pip install -r requirements-dev.txt
