FROM r-base

RUN apt-get update && apt-get install -y python3-pip vim pandoc
RUN pip3 install Flask --break-system-packages

COPY ./rscripts /opt/core/rscripts/

RUN Rscript /opt/core/rscripts/install_pkg.R
