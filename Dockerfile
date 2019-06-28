FROM alpine:3.7

RUN mkdir -p /usr/src/perl
WORKDIR /usr/src/perl

RUN apk update && apk upgrade && apk add curl tar make build-base wget gnupg
RUN apk add --update --no-cache --virtual  openssl-dev


## from perl; `true make test_harness` because 3 tests fail
## some flags from http://git.alpinelinux.org/cgit/aports/tree/main/perl/APKBUILD?id=19b23f225d6e4f25330e13144c7bf6c01e624656
#RUN curl -SLO https://www.cpan.org/src/5.0/perl-5.26.3.tar.gz \
#    && echo '940e1739dd979a284f343dff57ddcbf7f555b928 *perl-5.26.3.tar.gz' | sha1sum -c - \
#    && tar --strip-components=1 -xzf perl-5.26.3.tar.gz -C /usr/src/perl \
#    && rm perl-5.26.3.tar.gz \
#    && ./Configure -des \
#        -Duse64bitall \
#        -Dcccdlflags='-fPIC' \
#        -Dcccdlflags='-fPIC' \
#        -Dccdlflags='-rdynamic' \
#        -Dlocincpth=' ' \
#        -Duselargefiles \
 #       -Dusethreads \
 #       -Duseshrplib \
 #       -Dd_semctl_semun \
 #       -Dusenm \
 #   && make libperl.so \
 #   && make -j$(nproc) \
 #   && true TEST_JOBS=$(nproc) make test_harness \
#    && make install \
#    && curl -LO https://raw.githubusercontent.com/miyagawa/cpanminus/master/cpanm \
#    && chmod +x cpanm \
#    && ./cpanm App::cpanminus \
#    && rm -fr ./cpanm /root/.cpanm /usr/src/perl

## from tianon/perl
#ENV PERL_CPANM_OPT --verbose --mirror https://cpan.metacpan.org --mirror-only
#RUN cpanm Digest::SHA Module::Signature && rm -rf ~/.cpanm
#ENV PERL_CPANM_OPT $PERL_CPANM_OPT --verify
RUN apk add --update --no-cache perl perl-net-ssleay perl-crypt-ssleay

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
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
RUN touch /var/log/cron.log
RUN chmod 755 ./entry.sh ./main.py
RUN /usr/bin/crontab ./crontab.txt
CMD ["./entry.sh"]
CMD tail -f /var/log/cron.log