Title: Đọc code xem NGINX auto dùng bao nhiêu worker_processes trong container
Date: 2024-08-28
Category: frontpage
Tags: linux, C, NGINX, container, docker, podman

NGINX là HTTP server phổ biến nhất trên thế giới.
NGINX có kiến trúc "master" - "worker", với master process làm nhiệm vụ quản lý, và các worker process sẽ nhận các HTTP request và xử lý.

### NGINX worker_processes là gì
Số lượng worker process được set bằng config directive: `worker_processes` mặc định là 1, và có thể "tự động" với từ khóa `auto`.


```
Syntax: 	worker_processes number | auto;
Default:

worker_processes 1;

Context: 	main

Defines the number of worker processes.

The optimal value depends on many factors including (but not limited to) the number of CPU cores, the number of hard disk drives that store data, and load pattern. When one is in doubt, setting it to the number of available CPU cores would be a good start (the value “auto” will try to autodetect it).

    The auto parameter is supported starting from versions 1.3.8 and 1.2.5.
```
<https://nginx.org/en/docs/ngx_core_module.html#worker_processes>

khi set `auto`, NGINX sẽ `try to autodetect` - cố tìm số "available CPU cores", dễ dàng xem số CPU trên máy với câu lệnh

```
$ nproc
4
```
hay file `/proc/cpuinfo`

```
$ grep processor /proc/cpuinfo
processor	: 0
processor	: 1
processor	: 2
processor	: 3
```

### auto là bao nhiêu?
"auto" là bao nhiêu? lấy giá trị từ đâu? có đọc từ `/proc` ra không? thử đọc code C xem viết gì:

```
$ git clone --depth 1 https://github.com/nginx/nginx --branch release-1.27.1
Cloning into 'nginx'...
remote: Enumerating objects: 555, done.
...
Note: switching to 'e06bdbd4a20912c5223d7c6c6e2b3f0d6086c928'.
...

$ cd nginx
$ grep -Rn 'define NGINX_VERSION' src/core/nginx.h
13:#define NGINX_VERSION      "1.27.1"
```

Tìm từ khóa `auto`:

```
$ grep -Rin '"auto"'
...
src/core/nginx.c:1425:    if (ngx_strcmp(value[1].data, "auto") == 0) {
src/core/nginx.c:1566:    if (ngx_strcmp(value[1].data, "auto") == 0) {
...
```

Mở `src/core/nginx.c` tìm `"auto"` thấy:

```c
static char *
ngx_set_worker_processes(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_str_t        *value;
    ngx_core_conf_t  *ccf;

    ccf = (ngx_core_conf_t *) conf;

    if (ccf->worker_processes != NGX_CONF_UNSET) {
        return "is duplicate";
    }

    value = cf->args->elts;

    if (ngx_strcmp(value[1].data, "auto") == 0) {
        ccf->worker_processes = ngx_ncpu;
        return NGX_CONF_OK;
    }

    ccf->worker_processes = ngx_atoi(value[1].data, value[1].len);

    if (ccf->worker_processes == NGX_ERROR) {
        return "invalid value";
    }

    return NGX_CONF_OK;
}
```

nếu đọc từ config được giá trị là `"auto"`, NGINX sẽ gán `ccf->worker_processes = ngx_ncpu`.

Tìm `ngx_ncpu`:

```
$ grep -Rn ngx_ncpu
src/os/win32/ngx_os.h:59:extern ngx_uint_t   ngx_ncpu;
src/os/win32/ngx_win32_init.c:14:ngx_uint_t  ngx_ncpu;
src/os/win32/ngx_win32_init.c:131:    ngx_ncpu = si.dwNumberOfProcessors;
src/os/unix/ngx_os.h:79:extern ngx_int_t    ngx_ncpu;
src/os/unix/ngx_posix_init.c:13:ngx_int_t   ngx_ncpu;
src/os/unix/ngx_posix_init.c:62:    if (ngx_ncpu == 0) {
src/os/unix/ngx_posix_init.c:63:        ngx_ncpu = sysconf(_SC_NPROCESSORS_ONLN);
src/os/unix/ngx_posix_init.c:67:    if (ngx_ncpu < 1) {
src/os/unix/ngx_posix_init.c:68:        ngx_ncpu = 1;
src/os/unix/ngx_freebsd_init.c:210:        ngx_ncpu = ngx_freebsd_hw_ncpu / 2;
src/os/unix/ngx_freebsd_init.c:213:        ngx_ncpu = ngx_freebsd_hw_ncpu;
src/os/unix/ngx_darwin_init.c:164:    ngx_ncpu = ngx_darwin_hw_ncpu;
...
```

thấy trên các hệ điều hành, NGINX sẽ lấy giá trị theo cách khác nhau. Trên "posix" như các Linux-based OS, NGINX gọi C function `sysconf(_SC_NPROCESSORS_ONLN)`.

Gõ `man sysconf`

```
NAME
       sysconf - get configuration information at run time

SYNOPSIS
       #include <unistd.h>
...
- _SC_NPROCESSORS_ONLN
      The number of processors currently online (available).  See also get_nprocs_conf(3).
```

Viết 1 chương trình C 5 dòng để in ra giá trị này:

```C
// main.c
#include <stdio.h>
#include <unistd.h>

int main() {
    printf("online CPUs %ld\n", sysconf(_SC_NPROCESSORS_ONLN));
}

// $ cc main.c  # compile C code to a.out file
// $ ./a.out
// online CPUs 4
```

Dùng `strace` xem sysconf thực sự đọc từ đâu:

```
$ strace ./a.out 2>&1 | grep open
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/sys/devices/system/cpu/online", O_RDONLY|O_CLOEXEC) = 3
$ cat /sys/devices/system/cpu/online
0-3
```

Vậy NGINX lấy giá trị được tính bởi sysconf, đọc từ file `/sys/devices/system/cpu/online`.

### Trong container, NGINX auto dùng mấy worker process?
Nếu dùng podman xem [link này](https://github.com/containers/podman/blob/0e5eba6053137192fe6d5feb257204cb8e360517/troubleshooting.md#26-running-containers-with-resource-limits-fails-with-a-permissions-error) để có thể dùng option --cpus, docker không cần chỉnh gì:


```
--cpus float                               Number of CPUs. The default is 0.000 which means no limit
```

Trong container

```
$ podman run --cpus=1 -it docker.io/nginx bash

#root@1f334076d74f:/ nginx &
[1] 2
2024/08/28 13:19:04 [notice] 2#2: using the "epoll" event method
2024/08/28 13:19:04 [notice] 2#2: nginx/1.27.1
2024/08/28 13:19:04 [notice] 2#2: built by gcc 12.2.0 (Debian 12.2.0-14)
2024/08/28 13:19:04 [notice] 2#2: OS: Linux 6.8.0-40-generic
2024/08/28 13:19:04 [notice] 2#2: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/08/28 13:19:04 [notice] 3#3: start worker processes
2024/08/28 13:19:04 [notice] 3#3: start worker process 4
2024/08/28 13:19:04 [notice] 3#3: start worker process 5
2024/08/28 13:19:04 [notice] 3#3: start worker process 6
2024/08/28 13:19:04 [notice] 3#3: start worker process 7

[1]+  Done                    nginx
# apt update && apt install -y procps python
...
# ps xau | grep nginx
root           3  0.0  0.0  11404  1892 ?        Ss   13:19   0:00 nginx: master process nginx
nginx          4  0.0  0.0  11872  3044 ?        S    13:19   0:00 nginx: worker process
nginx          5  0.0  0.0  11872  3044 ?        S    13:19   0:00 nginx: worker process
nginx          6  0.0  0.0  11872  3044 ?        S    13:19   0:00 nginx: worker process
nginx          7  0.0  0.0  11872  3044 ?        S    13:19   0:00 nginx: worker process
# nproc
4
# cat /sys/devices/system/cpu/online
0-3
```

Nội dung file này được mang từ máy host vào, vì vậy dù container được set bao nhiêu CPU thì NGINX (hay các ngôn ngữ lập trình ví dụ Python) vẫn đọc giá trị là số CPU của máy host.

```
# python3
Python 3.11.2 (main, Aug 26 2024, 07:20:54) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.cpu_count()
4
```
## Kết luận
NGINX hay các ngôn ngữ lập trình khi chạy trong container đếm số CPU của máy host, không phải giá trị CPU request/limit cấp cho container.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
