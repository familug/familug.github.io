Title: [TIL] Lấy memory page size với CIL, Python, Rust, C
Date: 2025/07/19
Category: frontpage
Tags: pagesize, python, rust, c, cli
Slug: til-pagesize

## page size là gì?
```
$ apropos pagesize
getpagesize (2)      - get memory page size

$ man 2 getpagesize
       getpagesize - get memory page size

SYNOPSIS
       #include <unistd.h>

       int getpagesize(void);

..

DESCRIPTION
       The  function  getpagesize()  returns the number of bytes in a memory page,
       where "page" is a fixed-length block, the unit for  memory  allocation  and
       file mapping performed by mmap(2).

```

C function `getpagesize` trả về số bytes trong một `memory page`, trong đó `page` là một block có độ dài cố định, là đơn vị để cấp phát bộ nhớ (memory allocation).

## Lấy page size bằng CLI, Python, Rust, C

### CLI

```
$ whatis getconf
getconf (1)          - Query system configuration variables
getconf (1posix)     - get configuration values
$ getconf PAGESIZE
4096
```

### Python
```
$ python3 -c 'import resource; print(resource.getpagesize())'
4096
```

Code C của lib `resource`:

```c
#include <unistd.h>               // getpagesize()
...
static int
resource_getpagesize_impl(PyObject *module)
/*[clinic end generated code: output=9ba93eb0f3d6c3a9 input=546545e8c1f42085]*/
{
    long pagesize = 0;
#if defined(HAVE_GETPAGESIZE)
    pagesize = getpagesize();
#elif defined(HAVE_SYSCONF) && defined(_SC_PAGE_SIZE)
    pagesize = sysconf(_SC_PAGE_SIZE);
#else
#   error "unsupported platform: resource.getpagesize()"
#endif
    return pagesize;
}
```

<https://github.com/python/cpython/blob/53aeb821d4d656ac224c17f48e20af9072a01414/Modules/resource.c#L331-L348>


### C

```
$ cat main.c
#include <unistd.h>
#include <stdio.h>

int main() {
    printf("Page size is %d bytes", getpagesize());
}
$ cc main.c && ./a.out
Page size is 4096 bytes
```

### Rust

```rs
$ cargo new pagesize
    Creating binary (application) `pagesize` package
note: see more `Cargo.toml` keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
$ cd pagesize/
$ cargo add libc
...
```
```rs
# src/main.rs
fn get_page_size() -> usize {
    unsafe { libc::sysconf(libc::_SC_PAGESIZE) as usize }
}
fn main() {
    println!("Page size is {} bytes", get_page_size());
}
```

Cargo.toml
```
[package]
name = "pagesize"
version = "0.1.0"
edition = "2021"

[dependencies]
libc = "0.2.174"
```

Kết quả:
```
$ cargo run
   Compiling libc v0.2.174
   Compiling pagesize v0.1.0 (/home/me/pagesize)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.77s
     Running `target/debug/pagesize`
Page size is 4096 bytes
```

## Kết luận

Hầu hết các Linux OS đều dùng page size 4096 bytes hay **4k**, thì MacOS M1, M2, M4 lại có page size là 16384 == **16k**.
Sự khác biệt này dẫn tới nhiều vấn đề **thú vị** như [16k kernel page builds to support Apple Silicon (ARM64)](https://github.com/k3s-io/k3s/issues/7335).

> 4K pages made sense back when the Intel 386 came out. They are thoroughly obsolete, and the only reason they are the default on typical ARM64 distros is because 4K is the lowest common denominator supported everywhere and the Linux kernel's poor design does not allow deciding the page size at boot time. 16K is unarguably beneficial for all but the smallest embedded systems, and 64K is the logical choice for large servers. 4K pages increase overhead and do not provide a measurable memory savings. There's a reason Apple went with 16K for their entire 64-bit ARM ecosystem (because it's better, and because they control it all so they can make that decision).

Quote [marcan](https://github.com/k3s-io/k3s/issues/7335#issuecomment-1518600436)

Bài viết thực hiện trên:

```
$ lsb_release -d; uname -rm
Description:	Ubuntu 22.04.5 LTS
6.8.0-64-generic x86_64
```

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
