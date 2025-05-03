#in case the task requeries python to be installed:
FROM python:3.9-slim-buster
#else if its just a system : 
#FROM ubuntu:22.04

# Install some libs
RUN apt-get update && apt-get -y upgrade

# create ctf-user
RUN groupadd -r ctf && useradd -r -g ctf ctf
COPY quest.sh /home/ctf/
COPY launch.sh /home/ctf/
COPY ynetd /home/ctf/

#set some proper permissions
RUN pip install inputimeout 
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/quest.sh
RUN chmod 750 /home/ctf/ynetd
RUN chmod 750 /home/ctf/launch.sh

USER ctf
EXPOSE 1337

CMD /home/ctf/ynetd -p 1337 /home/ctf/launch.sh
