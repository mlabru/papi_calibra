#!/bin/bash

# nome do computador
HOST=`hostname`

# diretório de execução
cd ~/Public/mkr/papi/srce/papi_calibra

# envia dados
/usr/bin/env python ./papi_senders.py 2> ./papi_senders.$HOST.log &
