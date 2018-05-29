FROM ubuntu:14.04
MAINTAINER "Montri" <montri2025@gmail.com>

# environment
ENV DEBIAN_FRONTEND noninteractive

# update
RUN apt-get update

# environment dependencies
RUN apt-get -y install build-essential checkinstall \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
    git python-pip python-snappy

# clean cache files
RUN apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# add key
RUN mkdir -p /root/.ssh
ADD key/id_rsa /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa && \
    sed -i 's/^#   StrictHostKeyChecking ask/    StrictHostKeyChecking no/g' /etc/ssh/ssh_config

## make directory work space and clone project
RUN mkdir workspace && cd workspace && \
    git clone git@github.com:montri2025/pyconth2018.git  && \
    pip install -r worker/dependencies.txt



ADD consummer-start /usr/local/bin/
RUN chmod +x /usr/local/bin/worker-start


CMD ["worker-start"]
