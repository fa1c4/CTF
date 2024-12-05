# Desc: Extract the rootfs.cpio file

mkdir ./rootfs; cd ./rootfs; cpio -idm < ../rootfs.cpio
