FROM ubuntu
LABEL this is from ubuntu image
MAINTAINER name ravi teja kanchanapally
COPY index.html .
WORKDIR /teja/devops/
ADD https://downloads.apache.org/tomcat/tomcat-9/v9.0.111/bin/apache-tomcat-9.0.111.tar.gz .
EXPOSE 80
ARG course=devops
ENV subject=aws
RUN echo "learning the ${course} with ${subject}"


