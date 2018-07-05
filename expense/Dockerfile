FROM ubuntu:latest

RUN	apt-get -qq update && \
	apt-get install -y --allow-unauthenticated \
	curl \
	git \
	wget \
	python \
	python-dev \
	python-setuptools \
	build-essential \
	libssl-dev \
	libffi-dev \
	ruby
RUN easy_install pip
RUN pip install --upgrade pip
WORKDIR /usr/local/expense
COPY requirements.txt ./
RUN pip install -r requirements.txt
ADD . ./
ADD entrypoint.sh /tmp/entrypoint.sh
RUN chmod a+x /tmp/entrypoint.sh
CMD ["/tmp/entrypoint.sh"]
EXPOSE 8000
