#! /usr/bin/env bash
#set -x #echo on

# globals
VERSION=1.0
SPLUNK_API_KEY=mysplunkkey
LOCAL=localhost
INITIAL_PASSWORD=changemeagain
SPLUNK_PORT=8088
SPLUNK_API_PASSWORD=None
PROTOCOL=http
VERIFY=False

# colors for terminal
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`


# get the Operating system
function getOS()
{
    local machine
    unameOut="$(uname -s)"
    case "${unameOut}" in
        Linux*)     machine=Linux;;
        Darwin*)    machine=Mac;;
        *)          machine="UNKNOWN:${unameOut}"
    esac
    echo "$machine"
}

# only Linux and Mac is supported, for other systems the automatic development
# doesn't work, but must be installed manually
function checkCompatibility {
    machine=$1
    supported=(Linux Mac)
    if [[ ! ${supported[*]} =~ ${machine} ]] ; then
        echo -e \
        "checking compatibility .......... ${red}Failed${reset}\n" \
        " - ${yellow}${machine} is not supported to run automatic installation!"
        exit 1
    else
        echo "checked compatibility .......... ${green}ok${reset}"
    fi
}

# check if docker is running
function checkDockerRunning {
    docker ps -q
    if [ $? -eq 0 ] ; then
        echo -e \
        "checking docker daemon ......... ${green}ok${reset}"
    else
        echo -e \
        "checking docker daemon ......... ${red}failed${reset}\n" \
        " -  ${yellow}please start docker daemon!${reset}"
        exit 1
    fi
}
# stop running containers
function stopContainers {
    {
        docker rm $(docker stop $(docker ps -a -q --filter ancestor=splunk/splunk --format="{{.ID}}"))
        docker rm $(docker stop $(docker ps -a -q --filter ancestor=webtentacle:$VERSION --format="{{.ID}}")) 
    } &>/dev/null
}

function showLoading() {
    mypid=$!
    loadingText=$1
    echo -ne "$loadingText\r"

    while kill -0 $mypid 2>/dev/null; do
        echo -ne "$loadingText.\r"
        sleep 0.5
        echo -ne "$loadingText ..\r"
        sleep 0.5
        echo -ne "$loadingText ...\r"
        sleep 0.5
        echo -ne "$loadingText ....\r"
        sleep 0.5
        echo -ne "$loadingText ....\r"
        sleep 0.5
        echo -ne "$loadingText ....\r"
        sleep 0.5
        echo -ne "$loadingText ....\r"
        sleep 0.5
        echo -ne "$loadingText .....\r"
        sleep 0.5
        echo -ne "$loadingText ......\r"
        sleep 0.5
        echo -ne "$loadingText .......\r"
        sleep 0.5
        echo -ne "$loadingText ........\r"
        sleep 0.5
        echo -ne "$loadingText ..........\r"
        sleep 0.5
        echo -ne "\r\033[K"
        echo -ne "$loadingText\r"
        sleep 0.5
    done
    echo "$loadingText ............ ${green}ok${reset}"
}

function getBridgeHostnameForSplunkInDocker()
{
    local __resulutvar=$1
    local IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' splunk`
    echo -e \
        "checking your bridge IP ........ $IP"
    eval $__resulutvar="'$IP'"
}

function startSplunk
{
    docker run --name splunk -p 8000:8000 -p 9997:9997 -p 8088:8088 -p 8089:8089 -p 1514:1514 -d \
           -e "SPLUNK_START_ARGS=--accept-license --answer-yes --no-prompt --seed-passwd $INITIAL_PASSWORD" \
           -e "SPLUNK_PASSWORD=$INITIAL_PASSWORD" -e "SPLUNK_USER=root" splunk/splunk
}

function createToken
{
    if [ $MACHINE == "Linux" ] ; then
        sleep 21 &
        echo -en \
        "waiting for response "
    
        while ps | grep $! &>/dev/null; do
            echo -n "."
            sleep 2
        done
    else
        echo "${yellow}be patient, waiting for response, it will take 21 seconds.${reset}"
        sleep 21
    fi

    
    echo -e "${green} ok${reset}"
    if [ $MACHINE == "Linux" ] ; then
        SPLUNK_API_PASSWORD=`curl -k -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http \
 -d name=$SPLUNK_API_KEY  | grep -oP '(?<=<s:key name="token">).*?(?=</s:key>)'`
    else
        SPLUNK_API_PASSWORD=`curl -k -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http \
 -d name=$SPLUNK_API_KEY  | sed -n 's:.*<s\:key name="token">\(.*\)</s\:key>.*:\1:p'`
    fi
    echo -e \
    "creating token ................. ${green}ok${reset}\n" \
    "your token .................... $SPLUNK_API_PASSWORD"
}

function enableToken
{
    {
        curl -k -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/$SPLUNK_API_KEY -d description="For testing purposes"
        curl -k -X "POST" -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/http/enable 
        curl -k -X "POST" -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/$SPLUNK_API_KEY/enable 
    } &>/dev/null
}

function disableSSL
{
    {
        curl -k -X "POST" -u admin:$INITIAL_PASSWORD https://$LOCAL:8089/servicesNS/admin/splunk_httpinput/data/inputs/http/http -d enableSSL='0'
    } &>/dev/null
}

function buildWebtentacle
{
    docker build --build-arg SPLUNK_API_KEY=$SPLUNK_API_KEY \
    --build-arg SERVICE=webtentacle \
    --build-arg SPLUNK_API_PASSWORD=$SPLUNK_API_PASSWORD \
    --build-arg SPLUNK_HOSTNAME=$SPLUNK_HOSTNAME \
    --build-arg SPLUNK_PORT=$SPLUNK_PORT \
    --build-arg PROTOCOL=$PROTOCOL \
    --build-arg VERIFY=$VERIFY \
    -t webtentacle:$VERSION . 
}

function runWebtentacle
{
    if [ $MACHINE == "Linux" ] ; then
        docker run -d --name mywebtentacle -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro -it webtentacle:$VERSION 2>/dev/null
    else
        docker run -d --name mywebtentacle -it webtentacle:$VERSION 2>/dev/null
    fi
    echo -e "running mywebtentacle ..................... ${green}ok${reset}"
}

function epilogue
{
    echo -e "${yellow}.. You are ready to go .. ${reset}"
}

MACHINE=$(getOS)
checkCompatibility $MACHINE
checkDockerRunning
stopContainers & showLoading "stopping containers"
startSplunk && showLoading "starting splunk    "
createToken
enableToken && showLoading "enabling token     "
disableSSL && showLoading "disabling SSL      "
getBridgeHostnameForSplunkInDocker SPLUNK_HOSTNAME
buildWebtentacle && showLoading "building webtentacle image    "
runWebtentacle 
epilogue
exit 0
