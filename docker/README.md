# pyconth2018

## Prerequisite
    -  Install Docker machine  

1. Docker container  for MQTT  Service 
     ```
    # docker run -d --name mqtt  -p 1883:1883 -p 9001:9001 toke/mosquitto
    ```

2. Docker container for Grafana , Graphite and Statd 
    ```
     # docker run -d -e "TZ=Asia/Bangkok" --name graphite -p 3000:3000 -p 8125:8125/udp raintank/graphite-stack

    ```