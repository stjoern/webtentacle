FROM alpine:3.7

RUN mkdir -p /usr/src/perl
WORKDIR /usr/src/perl

RUN apk update && apk upgrade && apk add curl tar make build-base wget gnupg
#RUN apk add --update --no-cache --virtual  openssl-dev
RUN apk add --update --virtual  openssl-dev

RUN apk add --update perl perl-net-ssleay perl-crypt-ssleay

RUN apk add  --virtual .build-deps g++ python3-dev libffi-dev openssl-dev postfix && \
    apk add  --update python3 && \
    pip3 install --upgrade pip setuptools

RUN apk add git

WORKDIR /usr/src
RUN git clone https://github.com/sullo/nikto.git Nikto2

ENV PATH="/usr/src/Nikto2/program:$PATH"
RUN echo "$PATH"
RUN echo "$(which perl)"
RUN echo "$(which python3)"
RUN echo "$(which git)"
RUN echo "$(which nikto.pl)"

RUN mkdir -p /code/tmp
WORKDIR /code
COPY . .

#RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt

# start CRON (for testing purpose every 5 minutes)
#RUN echo '5 * * * * cd /code && python3 ./main.py' > /etc/crontabs/root
#CMD ['crond','-l 2','-f']
#RUN touch /var/log/cron.log
RUN chmod +x ./launcher.sh
RUN chmod +x ./entry.sh
ENTRYPOINT ["./entry.sh"]