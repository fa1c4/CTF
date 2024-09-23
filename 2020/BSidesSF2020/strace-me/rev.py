# strace ./strace-me 2>&1 | cut -d'(' -f2 | cut -c3-10 | grep -v 'exited' | sed '$d' | tail -n24 | tr -d '\n'; echo ''

s = '4354467b7468655f6c6f6e6765725f7468655f666c61675f69735f7468655f6d6f72655f696e746572657374696e675f6f75747075745f796f755f6172655f736565696e675f736f5f7468655f6c6f6e675f666c61675f69735f6c6f6e67217d'
byte_data = bytes.fromhex(s)
print(byte_data.decode())
