FROM python:3.10

ARG GID=1000
ARG UID=1000

RUN groupadd -g ${GID} python
RUN useradd -u ${UID} -g ${GID} -s /bin/bash python

COPY main.py .

RUN chmod +x main.py

USER python

ENTRYPOINT [ "python", "-u", "/main.py" ]
