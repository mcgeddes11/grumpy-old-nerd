FROM tiangolo/uwsgi-nginx-flask:flask
RUN apt-get -q update
RUN apt-get -q -y install python
RUN apt-get -q -y install vim
RUN apt-get install -q -y python-pip
RUN pip install --upgrade pip
RUN apt-get -q -y install libatlas-base-dev gfortran build-essential g++
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV BLOG_MAIL_DEFAULT_SENDER=admin@grumpyoldnerd.com
ENV BLOG_MAIL_PASSWORD=DixieWiener11
ENV BLOG_MAIL_USERNAME=joncocks@hotmail.com
ENV BLOG_SECRET_KEY=e05e8743-21e8-494b-a7c5-b4cf7ab94cc1
