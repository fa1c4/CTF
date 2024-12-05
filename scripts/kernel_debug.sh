# Desc: default gdb set to pwndbg | gef

sudo -E gdb ./vmlinux.bin -ex "set architecture i386:x86-64" \
	-ex "target remote localhost:1234" \
	-ex "add-symbol-file ./rootfs/xxx.ko $1" \
	-ex "b *(device_write + 0x233)" \
	-ex "c"
