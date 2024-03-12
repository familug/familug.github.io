Title: đọc source code xem systemd chạy chương trình mở được tối đa bao nhiêu file? 
Date: 2024-03-12
Category: frontpage
Tags: systemd, linux, kernel, LimitNOFILE, C

Mặc định  

hvn@mini ~ % systemctl status cron | grep PID
   Main PID: 464 (cron)
hvn@mini ~ % cat /proc/464/limits 
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

hvn@mini ~ % systemctl show cron| grep NOFILE   
LimitNOFILE=524288
LimitNOFILESoft=1024


% git clone --depth 1 --branch v249 https://github.com/systemd/systemd
Cloning into 'systemd'...
remote: Enumerating objects: 4600, done.
remote: Counting objects: 100% (4600/4600), done.
remote: Compressing objects: 100% (4063/4063), done.
remote: Total 4600 (delta 765), reused 1588 (delta 287), pack-reused 0
Receiving objects: 100% (4600/4600), 11.05 MiB | 2.92 MiB/s, done.
Resolving deltas: 100% (765/765), done.
Note: switching to 'f6278558da0304ec6b646bb172ce4688c7f162a5'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false




% grep -Rin LimitNOFILE | grep '.c:' | grep -v test
grep: test/testdata: warning: recursive directory loop
src/core/main.c:681:                { "Manager", "DefaultLimitNOFILE",           config_parse_rlimit,                RLIMIT_NOFILE, arg_default_rlimit         },
src/core/dbus-manager.c:2706:        SD_BUS_PROPERTY("DefaultLimitNOFILE", "t", bus_property_get_rlimit, offsetof(Manager, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
src/core/dbus-manager.c:2707:        SD_BUS_PROPERTY("DefaultLimitNOFILESoft", "t", bus_property_get_rlimit, offsetof(Manager, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
src/core/dbus-execute.c:1073:        SD_BUS_PROPERTY("LimitNOFILE", "t", bus_property_get_rlimit, offsetof(ExecContext, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),
src/core/dbus-execute.c:1074:        SD_BUS_PROPERTY("LimitNOFILESoft", "t", bus_property_get_rlimit, offsetof(ExecContext, rlimit[RLIMIT_NOFILE]), SD_BUS_VTABLE_PROPERTY_CONST),


Follow RLIMIT_NOFILE in `src/core/main.c` we found:

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

It read from kernel:

```c
        /* Get the underlying absolute limit the kernel enforces */
        nr = read_nr_open();
```

Find this function:

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

In `src/basic/fd-util.c` we see definition of `int read_nr_open(void) {`

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

It reads one line file `/proc/sys/fs/nr_open` or default to value 1024 * 1024. Let check the file:
```
% cat /proc/sys/fs/nr_open
1048576
```

