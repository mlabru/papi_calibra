#!/bin/bash

# nome do computador
HOST=`hostname`

# diretório de execução
cd ~/Public/mkr/papi/srce/papi_calibra

# envia dados dos sensores
/usr/bin/env python ./papi_sender_sns.py 2> ./papi_sender_sns.$HOST.log &

# envia imagem da camera
/usr/bin/env python ./papi_sender_cam.py 2> ./papi_sender_cam.$HOST.log &
