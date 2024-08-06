#https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-base/tags
#GPU APP FROM nvcr.io/nvidia/l4t-base:35.3.1
FROM  harbor.nanshe-arch.com/aipcimages/arm64v8/ubuntu:22.04 

RUN apt-get update && \
    apt-get install -y curl python3-pip  gunicorn && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install  requests fastapi flask openai flask_apscheduler aiohttp timeout_decorator
#RUN  ln -sf /usr/share/zoneinfo/Asia/Shanghai    /etc/localtime
#RUN  sed  -i  's#Etc\/UTC#Asia\/Shanghai#'  /etc/timezone
RUN useradd -u 1000 -m admin -s /bin/bash
WORKDIR /home/admin/http_server
EXPOSE 11435

COPY http_server_allplfmv6.py /home/admin/http_server/http_server_allplfmv6.py
COPY run.sh /home/admin/http_server/run.sh
RUN chmod +x /home/admin/http_server/run.sh

CMD ["bash", "run.sh"]
