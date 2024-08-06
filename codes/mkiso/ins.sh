apt install gcc-12
gcc-12 --version
chmod +x NVIDIA-Linux-x86_64-535.154.05.run 
./NVIDIA-Linux-x86_64-535.154.05.run 
apt install make 
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100
gcc --version
cc --verison
export CC=/usr/bin/gcc
cc --verison
gcc --version
cd /usr/bin/
ln -s gcc cc 
cc --version


 apt install linux-headers-$(uname -r)

./NVIDIA-Linux-x86_64-535.154.05.run 
bash NVIDIA-Linux-x86_64-535.154.05.run 
cd qwllm/
bash cuda_12.2.0_535.54.03_linux.run 
nvidia-smi 
top
nvidia-smi 
uname -r 

#ins docker
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update

VERSION_STRING=5:24.0.0-1~ubuntu.22.04~jammy
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin


sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo docker --version
sudo systemctl start docker
sudo systemctl enable docker
sudo groupadd docker
sudo usermod -aG docker ns
docker run hello-world


====================================================================================================
1. download iso file

2. mount -o loop *.iso /mnt

3. uncompress squashfs
unsquashfs ubuntu-server-minimal.squashfs 
cp /etc/resolv.conf ./squashfs-root/etc/resolv.conf
mount --bind /dev/ ./squashfs-root/dev; mount -t proc none ./squashfs-root/proc;mount -t sysfs none ./squashfs-root/sys

chroot  custom-iso
	apt install linux-headers-$(uname -r)  make -y
	~/NVIDIA-Linux-x86_64-535.154.05.run
	apt install vim -y 

exit


umount -l  ./squashfs-root/dev ./squashfs-root/proc ./squashfs-root/sys 
mksquashfs ~/squashfs_contents /path/to/modified-ubuntu-server-minimal.squashfs




#change cn source

sed -i "s/^deb/#deb/g" /etc/apt/sources.list

cat > /etc/apt/sources.list.d/aliyun.list << EOF
deb https://mirrors.aliyun.com/debian/ bookworm main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bookworm main non-free contrib
deb https://mirrors.aliyun.com/debian-security/ bookworm-security main
deb-src https://mirrors.aliyun.com/debian-security/ bookworm-security main
deb https://mirrors.aliyun.com/debian/ bookworm-updates main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bookworm-updates main non-free contrib
deb https://mirrors.aliyun.com/debian/ bookworm-backports main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bookworm-backports main non-free contrib
EOF

cat > /etc/apt/sources.list.d/firmware.list << EOF
deb http://mirrors.163.com/debian/ bookworm main non-free-firmware
deb-src http://mirrors.163.com/debian/ bookworm main non-free-firmware
deb http://mirrors.163.com/debian/ bookworm-updates main non-free-firmware
deb-src http://mirrors.163.com/debian/ bookworm-updates main non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main non-free-firmware
deb-src http://security.debian.org/debian-security bookworm-security main non-free-firmware
EOF

#mk debian chroot
apt install  debootstrap squashfs-tools
sudo debootstrap stable /chroot/debian12






#source code to build ros2

mkdir -p ~/ros2_humble/src
cd ~/ros2_humble
vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src

