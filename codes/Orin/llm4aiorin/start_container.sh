jetson-containers run -d  $(autotag ollama) ollama run qwen2_0.5b_hk:latest



docker run --runtime nvidia -it --rm --network host \
    --volume /tmp/argus_socket:/tmp/argus_socket \
    --volume /etc/enctune.conf:/etc/enctune.conf \
    --volume /etc/nv_tegra_release:/etc/nv_tegra_release \
    --volume /tmp/nv_jetson_model:/tmp/nv_jetson_model \
    --volume /var/run/dbus:/var/run/dbus \
    --volume /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume /home/admin/ssd_disk/hdmap_wanghaikuan/jetson-containers/data:/data \
    --device /dev/snd --device /dev/bus/usb \
    --device /dev/video0 --device /dev/video1 --device /dev/video2 --device /dev/video3 \
    --device /dev/i2c-0 --device /dev/i2c-1 --device /dev/i2c-2 --device /dev/i2c-3 \
    --device /dev/i2c-4 --device /dev/i2c-5 --device /dev/i2c-6 --device /dev/i2c-7 \
    --device /dev/i2c-8 -v /run/jtop.sock:/run/jtop.sock \
    -d --name ollama_container_name \
    -e OLLAMA_MODEL=qwen2_0.5b_hk:latest \
    dustynv/ollama:r35.4.1 ollama run qwen2_0.5b_hk:latest

