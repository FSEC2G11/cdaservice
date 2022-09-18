FROM python:3.10.2

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/cdaservice

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 6001

RUN apt update
RUN apt -y install libopenblas-dev liblapack-dev
RUN ln -s /usr/src/cdaservice/cdaengine/libkaxlicvallinux.so /usr/lib/aarch64-linux-gnu
RUN ln -s /usr/src/cdaservice/cdaengine/libcfenginelinux.so /usr/lib/aarch64-linux-gnu
# RUN python manage.py runserver 0.0.0.0:6001

CMD [ "python", "manage.py", "runserver", "0.0.0.0:6001" ]
