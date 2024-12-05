# Desc: Compile exp and Pack the rootfs.cpio file
# requirements: 
# export libLian=/path/to/libLian/result (built by nix-build)
# reference: https://github.com/AvavaAYA/nix-config/
# install nix-build: 
# curl -L https://nixos.org/nix/install > install_nix.sh
# chmod +x install_nix.sh
# ./install_nix.sh # it will add the nix to your shell profile


# compiling the exp
cd ./rootfs
cp ../exp.c .

# method I: directly compile the exp.c with gcc
gcc ./exp.c -o exp -masm=intel --static -g

# method II: compile the exp.c based on libLian
# for my environment, I have to export the libLian path as below, modify to yours
# export libLian=/home/fa1c4/Desktop/nix-config/packages/libLian/result
# gcc -static -masm=intel exp.c -L${libLian}/lib -lLian -I${libLian}/include -o exp

chmod 777 ./exp


# packing the rootfs.cpio
# find . -print0 | cpio --null -ov --format=newc > ../rootfs.cpio
find . -print0 | cpio --null -ov --format=newc > ../rootfs.cpio 2> /dev/null
chmod 777 ../rootfs.cpio
echo "rootfs.cpio is ready"
