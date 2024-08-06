echo -e "\nmenuentry 'Windows 12' {
    insmod part_gpt
    insmod fat
    insmod search
    insmod chain
    search --set=root --file /EFI/Microsoft/Boot/bootmgfw.efi
    chainloader /EFI/Microsoft/Boot/bootmgfw.efi
}" | tee -a /etc/grub.d/40_custom
