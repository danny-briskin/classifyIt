FROM python:3.8

LABEL authors="Danny Briskin (dbriskin@qaconsultants.com)"

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install waitress
COPY . /tmp/classifyit

WORKDIR /tmp/classifyit

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["-m", "com.qaconsultants.classifyit.app" ]
