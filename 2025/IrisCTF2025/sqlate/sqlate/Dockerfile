FROM ubuntu:22.04

RUN /usr/sbin/useradd --no-create-home -u 1000 user
# RUN apt-get update && apt-get install -y netcat
RUN apt-get update && apt-get install -y socat

COPY . /home/user/

USER user

# CMD ["sh", "-c", "cd /home/user && /home/user/vuln"]
CMD ["sh", "-c", "cd /home/user && socat TCP-LISTEN:10000,fork EXEC:./vuln"]
