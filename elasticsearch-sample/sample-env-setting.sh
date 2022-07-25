# Password for the 'elastic' user (at least 6 characters)
export ELASTIC_PASSWORD=

# Password for the 'kibana_system' user (at least 6 characters)
export KIBANA_PASSWORD=

# Version of Elastic products
export STACK_VERSION=8.3.2

# Set the cluster name
export CLUSTER_NAME=docker-cluster

# Set to 'basic' or 'trial' to automatically start the 30-day trial
exoprt LICENSE=basic
#LICENSE=trial

# Port to expose Elasticsearch HTTP API to the host
export ES_PORT=192.168.64.2:9200
#ES_PORT=127.0.0.1:9200

# Port to expose Kibana to the host
export KIBANA_PORT=192.168.64.2:5601
#KIBANA_PORT=80

# Increase or decrease based on the available host memory (in bytes)
export MEM_LIMIT=2000000000

# Project namespace (defaults to the current folder name if not set)
#COMPOSE_PROJECT_NAME=myproject
