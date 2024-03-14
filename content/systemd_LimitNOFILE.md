Title: Đọc source code xem systemd chạy chương trình mở được tối đa bao nhiêu file? 
Date: 2024-03-12
Category: frontpage
Tags: systemd, linux, kernel, LimitNOFILE, C

Mặc định chương trình trên Linux chỉ mở được giới hạn file nhất định. Nếu chạy từ shell (như bash) giá trị này thường có thể xem từ lệnh 

```
$ ulimit -n
1024
```

giá trị này có thể thay đổi ngay trên shell 

```
$ ulimit -n 9999
$ ulimit -n
9999
```
### Set process max open files trên Systemd 
Khi chạy bằng systemd, các service sẽ kết thừa giá trị limit của systemd hoặc tự set bằng LimitNOFILE
```
$ systemd --version
systemd 249 (249.11-0ubuntu3.12)
```

Theo `man 2 setrlimit`

> A child process created via fork(2) inherits its parent's resource  limits.   Resource  limits are preserved across execve(2).

Xem giá trị theo 2 cách: dùng lệnh systemctl show và xem trên /proc filesystem

```
% systemctl show cron| grep NOFILE   
LimitNOFILE=524288
LimitNOFILESoft=1024

% systemctl status cron | grep PID
   Main PID: 464 (cron)
% cat /proc/464/limits 
Limit                     Soft Limit           Hard Limit           Units     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            8388608              unlimited            bytes     
Max core file size        0                    unlimited            bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             61289                61289                processes 
Max open files            1024                 524288               files     
Max locked memory         8388608              8388608              bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       61289                61289                signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us   
```

### Soft limit vs hard limit
Theo `man 5 limits.conf`: 

```
hard
for enforcing hard resource limits. These limits are set by the superuser and enforced
by the Kernel. The user cannot raise his requirement of system resources above such
values.

soft
for enforcing soft resource limits. These limits are ones that the user can move up or
down within the permitted range by any pre-existing hard limits. The values specified
with this token can be thought of as default values, for normal system usage.
```

Theo `man 2 getrlimit`

```
The  soft  limit  is  the value that the kernel enforces for the corre‐
sponding resource.  The hard limit acts  as  a  ceiling  for  the  soft
limit:  an  unprivileged process may set only its soft limit to a value
in the range from 0 up to the hard limit, and (irreversibly) lower  its
hard   limit.    A  privileged  process  (under  Linux:  one  with  the
CAP_SYS_RESOURCE capability in the initial user namespace) may make ar‐
bitrary changes to either limit value.
```

Hard limit là giá trị admin set tối đa, để người dùng khác trên cùng hệ thống không set vượt quá được (dùng ulimit). Với system service, không có "người dùng" set giá trị (người dùng là admin??!), giá trị có ý nghĩa duy nhất ở đây là soft limit, thường được set bằng luôn với hard limit.

### Đọc code tìm giá trị tối đa cho Max open files LimitNOFILE  
Lấy code tại tag v249 về:

```
% git clone --depth 1 --branch v249 https://github.com/systemd/systemd
Cloning into 'systemd'...
remote: Enumerating objects: 4600, done.
remote: Counting objects: 100% (4600/4600), done.
remote: Compressing objects: 100% (4063/4063), done.
remote: Total 4600 (delta 765), reused 1588 (delta 287), pack-reused 0
Receiving objects: 100% (4600/4600), 11.05 MiB | 2.92 MiB/s, done.
Resolving deltas: 100% (765/765), done.
Note: switching to 'f6278558da0304ec6b646bb172ce4688c7f162a5'.
...

```

Tìm giá trị config LimitNOFILE trong các file code C
```
% grep -Rin LimitNOFILE | grep '.c:' | grep -v test
grep: test/testdata: warning: recursive directory loop
src/core/main.c:681:                { "Manager", "DefaultLimitNOFILE",           config_parse_rlimit,                RLIMIT_NOFILE, arg_default_rlimit         },
src/core/dbus-manager.c:2706:        SD_BUS_PROPERTY("DefaultLimitNOFILE", "t", bus_property_get_rlimit, offsetof(Manager, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
src/core/dbus-manager.c:2707:        SD_BUS_PROPERTY("DefaultLimitNOFILESoft", "t", bus_property_get_rlimit, offsetof(Manager, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
src/core/dbus-execute.c:1073:        SD_BUS_PROPERTY("LimitNOFILE", "t", bus_property_get_rlimit, offsetof(ExecContext, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
src/core/dbus-execute.c:1074:        SD_BUS_PROPERTY("LimitNOFILESoft", "t", bus_property_get_rlimit, offsetof(ExecContext, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
```

Xem  RLIMIT_NOFILE trong `src/core/main.c` thấy systemd set giá trị tối đa số file có thể mở tới giá trị kernel giới hạn:

```c
static int bump_rlimit_nofile(struct rlimit *saved_rlimit) {
        struct rlimit new_rlimit;
        int r, nr;

        /* Get the underlying absolute limit the kernel enforces */
        nr = read_nr_open();

        /* Calculate the new limits to use for us. Never lower from what we inherited. */
        new_rlimit = (struct rlimit) {
                .rlim_cur = MAX((rlim_t) nr, saved_rlimit->rlim_cur),
                .rlim_max = MAX((rlim_t) nr, saved_rlimit->rlim_max),
        };

        /* Shortcut if nothing changes. */
        if (saved_rlimit->rlim_max >= new_rlimit.rlim_max &&
            saved_rlimit->rlim_cur >= new_rlimit.rlim_cur) {
                log_debug("RLIMIT_NOFILE is already as high or higher than we need it, not bumping.");
                return 0;
        }

        /* Bump up the resource limit for ourselves substantially, all the way to the maximum the kernel allows, for
         * both hard and soft. */
        r = setrlimit_closest(RLIMIT_NOFILE, &new_rlimit);
        if (r < 0)
                return log_warning_errno(r, "Setting RLIMIT_NOFILE failed, ignoring: %m");

        return 0;
}
```

Giá trị tối đa tuyệt đối được Linux kernel quyết định

```c
        /* Get the underlying absolute limit the kernel enforces */
        nr = read_nr_open();
```

Tìm function này:

```
 grep -Rin read_nr_open
src/basic/fd-util.h:106:int read_nr_open(void);
src/basic/rlimit-util.c:382:                limit = read_nr_open();
src/basic/fd-util.c:701:int read_nr_open(void) {
src/test/test-fd-util.c:183:static void test_read_nr_open(void) {
src/test/test-fd-util.c:184:        log_info("nr-open: %i", read_nr_open());
src/test/test-fd-util.c:291:        test_read_nr_open();
src/core/main.c:1228:                k = read_nr_open();
src/core/main.c:1260:        nr = read_nr_open();
src/core/main.c:2273:                nr = read_nr_open();
```

Trong `src/basic/fd-util.c` có định nghĩa function `int read_nr_open(void) {`

```c
int read_nr_open(void) {
        _cleanup_free_ char *nr_open = NULL;
        int r;

        /* Returns the kernel's current fd limit, either by reading it of /proc/sys if that works, or using the
         * hard-coded default compiled-in value of current kernels (1M) if not. This call will never fail. */

        r = read_one_line_file("/proc/sys/fs/nr_open", &nr_open);
        if (r < 0)
                log_debug_errno(r, "Failed to read /proc/sys/fs/nr_open, ignoring: %m");
        else {
                int v;

                r = safe_atoi(nr_open, &v);
                if (r < 0)
                        log_debug_errno(r, "Failed to parse /proc/sys/fs/nr_open value '%s', ignoring: %m", nr_open);
                else
                        return v;
        }

        /* If we fail, fall back to the hard-coded kernel limit of 1024 * 1024. */
        return 1024 * 1024;
}
```

Function này đọc giá trị kernel set từ `/proc/sys/fs/nr_open` hoặc nếu fail sẽ dùng giá trị 1024 * 1024. Xem thử file này trên máy Ubuntu 22.04:
```
% cat /proc/sys/fs/nr_open
1048576
```

Cũng bằng với 1024 * 1024.

Tìm function gọi function `read_nr_open`:

```
$ grep -Rin read_nr_open
src/basic/fd-util.h:106:int read_nr_open(void);
src/basic/rlimit-util.c:382:                limit = read_nr_open();
src/basic/fd-util.c:701:int read_nr_open(void) {
src/test/test-fd-util.c:183:static void test_read_nr_open(void) {
src/test/test-fd-util.c:184:        log_info("nr-open: %i", read_nr_open());
src/test/test-fd-util.c:291:        test_read_nr_open();
src/core/main.c:1228:                k = read_nr_open();
src/core/main.c:1260:        nr = read_nr_open();
src/core/main.c:2273:                nr = read_nr_open();
```
Xem src/basic/rlimit-util.c


```c
int rlimit_nofile_bump(int limit) {
        int r;

        /* Bumps the (soft) RLIMIT_NOFILE resource limit as close as possible to the specified limit. If a negative
         * limit is specified, bumps it to the maximum the kernel and the hard resource limit allows. This call should
         * be used by all our programs that might need a lot of fds, and that know how to deal with high fd numbers
         * (i.e. do not use select() — which chokes on fds >= 1024) */

        if (limit < 0)
                limit = read_nr_open();

        if (limit < 3)
                limit = 3;

        r = setrlimit_closest(RLIMIT_NOFILE, &RLIMIT_MAKE_CONST(limit));
        if (r < 0)
                return log_debug_errno(r, "Failed to set RLIMIT_NOFILE: %m");

        return 0;
}
```

Khi limit < 0, limit sẽ nhận giá trị của `read_nr_open()`, khi limit >=3, gọi `setrlimit_closest`

```c
int setrlimit_closest(int resource, const struct rlimit *rlim) {
        struct rlimit highest, fixed;
...
        if (setrlimit(resource, rlim) >= 0)
                return 0;

        if (errno != EPERM)
                return -errno;

        /* So we failed to set the desired setrlimit, then let's try
         * to get as close as we can */

        if (getrlimit(resource, &highest) < 0)
                return -errno;

        /* If the hard limit is unbounded anyway, then the EPERM had other reasons, let's propagate the original EPERM
         * then */
        if (highest.rlim_max == RLIM_INFINITY)
                return -EPERM;

        fixed = (struct rlimit) {
                .rlim_cur = MIN(rlim->rlim_cur, highest.rlim_max),
                .rlim_max = MIN(rlim->rlim_max, highest.rlim_max),
        };
...
}
```

Giá trị được set là `MIN(rlim->rlim_cur, highest.rlim_max)`, nên người dùng không thể set cao hơn giá trị `highest.rlim_max`, tức giá trị max hard limit kế thừa từ systemd, hay kết quả của function read_nr_open, ở ví dụ này là 1024*1024.

### Tạo service chạy Python thử set hard limit lớn hơn 1024*1024
Python3.10 hiển thị giá trị RLIMIT_NOFILE của Python process:

```py
% python3 -c 'import resource; print(resource.getrlimit(resource.RLIMIT_NOFILE))' 
(1024, 1048576)
```
Tạo 1 systemd service tên `pymi` lần lượt set LimitNOFILE=5242880 và 5000 
```
# systemctl  cat pymi.service 
# /lib/systemd/system/pymi.service
[Unit]
Description=FAMILUG.org rlimit test
After=remote-fs.target nss-user-lookup.target

[Service]
ExecStart=python3 -c 'import resource; print(resource.getrlimit(resource.RLIMIT_NOFILE))'
LimitNOFILE=5242880
IgnoreSIGPIPE=false
KillMode=process

[Install]
WantedBy=multi-user.target

```

```
# systemctl daemon-reload
# systemctl start pymi
# systemctl status pymi
root@mini:~# systemctl status pymi
○ pymi.service - FAMILUG.org rlimit test
     Loaded: loaded (/lib/systemd/system/pymi.service; disabled; vendor preset: enabled)
     Active: inactive (dead)

Thg 3 15 00:49:13 mini systemd[1]: Started FAMILUG.org rlimit test.
Thg 3 15 00:49:13 mini python3[215501]: (1048576, 1048576)
Thg 3 15 00:49:13 mini systemd[1]: pymi.service: Deactivated successfully.
Thg 3 15 00:49:33 mini systemd[1]: Started FAMILUG.org rlimit test.
Thg 3 15 00:49:34 mini python3[216937]: (5000, 5000)
Thg 3 15 00:49:34 mini systemd[1]: pymi.service: Deactivated successfully.
```

Kết quả: 

- Khi set 5242880 (5 triệu), giá trị này bị set về giá trị tối đa của kernel set 1048576.
- khi set 5000, chương trình Python thấy cả 2 soft và hard limit đều = 5000.


## Kết luận
Tại systemd v249, Không thể set LimitNOFILE lớn hơn giá trị trong `/proc/sys/fs/nr_open`.

Nhưng giá trị trong nr_open có thể thay đổi bằng sysctl:

```
# sysctl -a | grep nr_open
fs.nr_open = 1048576
```

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
