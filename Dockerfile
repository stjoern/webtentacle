FROM alpine:3.7

RUN mkdir -p /usr/src/perl
WORKDIR /usr/src/perl

RUN apk update && apk upgrade && apk add curl tar make build-base wget gnupg glib-dev dbus-dev

# && \
#    apk add --update gnome-keyring libgnome-keyring-dev
RUN apk add --update --virtual  openssl-dev

#RUN apk add --update perl perl-net-ssleay perl-crypt-ssleay

RUN apk add  --virtual .build-deps g++ python3-dev libffi-dev openssl-dev postfix && \
    apk add  --update python3 && \
    pip3 install --upgrade pip setuptools


#RUN apk add git

#WORKDIR /usr/src
#RUN git clone https://github.com/sullo/nikto.git Nikto2

#RUN ln -s /usr/src/Nikto2/program/nikto.pl /usr/src/Nikto2/program/nikto
#ENV PATH="/usr/src/Nikto2/program:$PATH"
#RUN echo "$PATH"
#RUN echo "$(which perl)"
#RUN echo "$(which python3)"
#RUN echo "$(which git)"
#RUN echo "$(which nikto.pl)"

# edit nikto.conf for correct DTD path
#RUN sed -i 's/NIKTODTD=docs\/nikto.dtd.*/NIKTODTD=\/usr\/src\/Nikto2\/program\/docs\/nikto.dtd/g' /usr/src/Nikto2/program/nikto.conf.default

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

RUN pip3 install cx-freeze

ARG SPLUNK_INITIAL_PASSWORD

#ENV SPLUNK_INITIAL_PASSWORD "$SPLUNK_INITIAL_PASSWORD"
RUN echo ${SPLUNK_INITIAL_PASSWORD}
RUN python3 -c "from keyring import get_keyring;print(get_keyring())"
RUN python3 -c "import sys;from keyrings.cryptfile.cryptfile import CryptFileKeyring;kr=CryptFileKeyring();\
                kr.keyring_key=sys.argv[1];kr.set_password('system',sys.argv[2],sys.argv[3])" monika admin ${SPLUNK_INITIAL_PASSWORD}         

#RUN python3 -c "import keyring;keyring.set_password('webtentacle','xkcd','correct horse battery staple')"

#RUN python3 -c "import keyring;print(keyring.get_password('webtentacle','xkcd'))"     
#RUN python3 webtentacle/security/security.py -s splunkenterprise admin ${SPLUNK_INITIAL_PASSWORD}
#RUN python3 webtentacle/security/security.py -g splunkenterprise admin

#RUN chmod +x webtentacle/launcher.sh
#RUN chmod +x webtentacle/entry.sh
#ENTRYPOINT ["webtentacle/entry.sh"]