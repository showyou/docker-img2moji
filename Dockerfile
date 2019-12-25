FROM python:3.7.5

LABEL maintainer="Showyou <showyou41@gmail.com>"

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Tokyo

RUN apt-get update && \
    apt-get install -y python3-pip fonts-ipafont-gothic python3-opencv && \
    groupadd -r pyuser && useradd --no-log-init -r -m -g pyuser pyuser
USER pyuser
WORKDIR /home/pyuser
RUN pip3 install --user matplotlib numpy pillow
#RUN ls -al
EXPOSE 8888
CMD ["/bin/bash"]
#CMD ["jupyter", "notebook", "--ip=0.0.0.0"]
