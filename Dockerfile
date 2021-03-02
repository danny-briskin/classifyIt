#build image
FROM python:3.8-slim as builder

RUN apt-get update \
&& apt-get install gcc libcairo2-dev -y \
&& apt-get clean

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install waitress apispec flask_swagger_ui apispec_webframeworks marshmallow
COPY . /tmp/classifyit

#build image
FROM python:3.8-slim as app

LABEL authors="Danny Briskin (dbriskin@qaconsultants.com)"

COPY --from=builder /root/.local /root/.local
COPY --from=builder /tmp/classifyit /tmp/classifyit
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
#cairo and deps
COPY --from=builder /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
COPY --from=builder /usr/share/doc/libcairo-gobject2 /usr/share/doc/libcairo-gobject2
COPY --from=builder /usr/share/doc/libcairo2-dev /usr/share/doc/libcairo2-dev
COPY --from=builder /usr/share/doc/libcairo2 /usr/share/doc/libcairo2
COPY --from=builder /usr/include/cairo /usr/include/cairo
COPY --from=builder /usr/local/bin/cairosvg /usr/local/bin/cairosvg
COPY --from=builder /var/lib/dpkg/info/libcairo* /var/lib/dpkg/info/
COPY --from=builder /root/.cache/pip/ /root/.cache/pip/

WORKDIR /tmp/classifyit
EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["-m", "com.qaconsultants.classifyit.app" ]
