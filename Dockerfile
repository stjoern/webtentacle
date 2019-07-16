FROM alpine:3.7

RUN mkdir -p /usr/src/perl
WORKDIR /usr/src/perl

RUN apk update && apk upgrade && apk add curl tar make build-base wget gnupg glib-dev dbus-dev

RUN apk add --update --virtual  openssl-dev

RUN apk add --update perl perl-net-ssleay perl-crypt-ssleay

RUN apk add  --virtual .build-deps g++ python3-dev libffi-dev openssl-dev postfix && \
    apk add  --update python3 && \
    pip3 install --upgrade pip setuptools


RUN apk add git

WORKDIR /usr/src
RUN git clone https://github.com/sullo/nikto.git Nikto2

RUN ln -s /usr/src/Nikto2/program/nikto.pl /usr/src/Nikto2/program/nikto
ENV PATH="/usr/src/Nikto2/program:$PATH"
RUN echo "$PATH"
RUN echo "$(which perl)"
RUN echo "$(which python3)"
RUN echo "$(which git)"
RUN echo "$(which nikto.pl)"

# edit nikto.conf for correct DTD path
RUN sed -i 's/NIKTODTD=docs\/nikto.dtd.*/NIKTODTD=\/usr\/src\/Nikto2\/program\/docs\/nikto.dtd/g' /usr/src/Nikto2/program/nikto.conf.default

RUN mkdir -p /code/tmp
RUN mkdir -p /code/webtentacle

COPY requirements.txt /code/requirements.txt
ADD webtentacle /code/webtentacle

WORKDIR /code
#RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 uninstall pycrypto  -y
RUN pip3 uninstall pycryptodome -y
RUN pip3 install pycryptodome

RUN pip3 install cx_Freeze

ARG SPLUNK_INITIAL_PASSWORD
ARG SERVICE
ARG SPLUNK_API_KEY 
ARG SPLUNK_API_PASSWORD
ARG SPLUNK_HOSTNAME
ARG SPLUNK_PORT

# replace config.yml for splunk configuration
RUN sed -i "s|host: <?>|host: ${SPLUNK_HOSTNAME}|" /code/webtentacle/config.yml
RUN sed -i "s|port: <?>|port: ${SPLUNK_PORT}|" /code/webtentacle/config.yml
RUN sed -i "s|key_name: <?>|key_name: ${SPLUNK_API_KEY}|" /code/webtentacle/config.yml

# build keyring
WORKDIR /code/webtentacle/keyring
RUN mkdir -p /code/.code

# replace dynamically as needed service, username
RUN sed -i "s|self.mother_service='?'|self.mother_service='$SERVICE'|" /code/webtentacle/keyring/crypt.py
RUN sed -i "s|self.kr.keyring_key='?'|self.kr.keyring_key='$SPLUNK_API_KEY'|" /code/webtentacle/keyring/crypt.py
        

RUN python3 setup.py build
WORKDIR /code/.code
RUN pip3 uninstall cx_Freeze -y
RUN rm -fr /code/webtentacle/keyring
RUN keyring/crypt encrypt --username $SPLUNK_API_KEY --password $SPLUNK_API_PASSWORD


#RUN python3 -c "from keyring import get_keyring;print(get_keyring())"
#RUN python3 -c "import sys;from keyrings.cryptfile.cryptfile import CryptFileKeyring;kr=CryptFileKeyring();\
#                kr.keyring_key=sys.argv[1];kr.set_password('system',sys.argv[2],sys.argv[3])" monika admin ${SPLUNK_INITIAL_PASSWORD}         

WORKDIR /code
RUN chmod +x webtentacle/launcher.sh
RUN chmod +x webtentacle/entry.sh
ENTRYPOINT ["webtentacle/entry.sh"]