#!/bin/bash
function loop_request {
    while true; do
        curl -s "http://192.168.29.238:11434/api/chat" -d'{"model": "test:v1.0","messages":[{"role": "user","content": "why is the sky blue?"}]}' &
        pid=$!
        pids+=($pid)
        # 控制并发数量，这里设置为10
        if [ ${#pids[@]} -ge 10 ]; then
            wait ${pids[@]:0:9}
            pids=(${pids[@]:10})
        fi
    done
}

# 开启10个这样的函数在后台运行
for i in {1..10}; do
    loop_request &
done

# 主进程等待所有后台进程结束
wait
