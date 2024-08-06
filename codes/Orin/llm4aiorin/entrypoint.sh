#!/bin/bash

exec /usr/local/bin/ollama serve &
OLLAMA_PID=$!

sleep 5

ollama create qwen2-1.5b-chat-mul_02-Q8_0:v1.0 -f /home/admin/ssd_disk/workspace/Modelfile
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "Model creation successful. Running inference..."
    first_service_pid=$!
    wait_for_first_service() {
  	#while ! curl -s -o /dev/null localhost:11434; do
    	until ollama run qwen2-1.5b-chat-mul_02-Q8_0:v1.0 ;do sleep 2;done
	}
    
    wait_for_first_service

    gunicorn -w 1 -b 0.0.0.0:11436  --log-level info --access-logfile -   serve_intend_mapping:app
    wait $first_service_pid
else
    echo "Model creation failed. Exiting..."
    kill $OLLAMA_PID
    exit $RESULT
fi


