#! /usr/bin/env bash
#set -x #echo on
echo "Stopping splunk/splunk container if it is running."

docker stop $(docker ps -q --filter ancestor=splunk/splunk)
VERSION=1.0
SPLUNK_API_KEY=mysplunkkey
LOCAL=localhost
SPLUNK_HOSTNAME=`ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -n1`
echo "Your splunk instance is running on $LOCAL"
echo "Splunk in docker on $SPLUNK_HOSTNAME"
SPLUNK_API_PASSWORD=none
INITIAL_PASSWORD=changemeagain
SPLUNK_PORT=8088
docker run -p 8000:8000 -p 9997:9997 -p 8088:8088 -p 8089:8089 -p 1514:1514 -d \
           -e "SPLUNK_START_ARGS=--accept-license --answer-yes --no-prompt --seed-passwd $INITIAL_PASSWORD" \
           -e "SPLUNK_PASSWORD=$INITIAL_PASSWORD" -e "SPLUNK_USER=root" splunk/splunk

sleep 30
SPLUNK_API_PASSWORD=`curl -k -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http \
 -d name=$SPLUNK_API_KEY  | grep -oP '(?<=<s:key name="token">).*?(?=</s:key>)'`

echo "Your splunk instance is running at https://$LOCAL:8000, username: admin, password: $INITIAL_PASSWORD"
echo "Your token is: $SPLUNK_API_PASSWORD"
sleep 5
curl -k -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/$SPLUNK_API_KEY -d description="For testing purposes" > /dev/null 2>&1
echo "Description for your token changed to be only 'for testing purposes'."
curl -k -X "POST" -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/http/enable
sleep 5
curl -k -X "POST" -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/$SPLUNK_API_KEY/enable > /dev/null 2>&1
echo "Your token $SPLUNK_API_KEY is enabled now"
curl -k -X "POST" -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/http -d enableSSL='0'
echo "HTTP event Collector is now enabled and without SSL"

echo "Building webtentacle docker"
docker stop $(docker ps -q --filter ancestor=webtentacle:$VERSION)
docker rm $(docker ps -aq --filter name=mywebtentacle)

docker build --build-arg SPLUNK_API_KEY=$SPLUNK_API_KEY \
    --build-arg SERVICE=webtentacle \
    --build-arg SPLUNK_API_PASSWORD=$SPLUNK_API_PASSWORD \
    --build-arg SPLUNK_HOSTNAME=$SPLUNK_HOSTNAME \
    --build-arg SPLUNK_PORT=$SPLUNK_PORT \
    -t webtentacle:$VERSION . 
docker run -d --name mywebtentacle -it webtentacle:$VERSION
exit

