Title: [TIL] docker COPY không giống lệnh cp
Date: 2025-02-11
Category: frontpage
Tags: til, docker
Slug: dockercopy

Trong Dockerfile có lệnh (instruction) COPY dùng để copy file, thư mục. Nhưng cách hoạt động hơi khác lệnh cp trên UNIX.

```
cp file destdir
```
khi destdir là 1 thư mục đã tồn tại, cp sẽ copy file `file` tới `destdir/file`.

Còn COPY thì khác <https://docs.docker.com/reference/dockerfile/#copy>. Tất nhiên không ai đọc doc của syntax Dockerfile cả!

> The COPY instruction copies new files or directories from <src> and adds them to the filesystem of the image at the path <dest>
> You can specify multiple source files or directories with COPY. The last argument must always be the destination.
> If the destination path begins with a forward slash, it's interpreted as an absolute path, and the source files are copied into the specified destination relative to the root of the current build stage.

```
# create /abs/test.txt
COPY test.txt /abs/
```
>
> Trailing slashes are significant. For example, COPY test.txt /abs creates a file at /abs, whereas COPY test.txt /abs/ creates /abs/test.txt.
>
> If the destination path doesn't begin with a leading slash, it's interpreted as relative to the working directory of the build container.

```
WORKDIR /usr/src/app
# create /usr/src/app/rel/test.txt
COPY test.txt rel/
```
> If destination doesn't exist, it's created, along with all missing directories in its path.

**If the source is a file, and the destination doesn't end with a trailing slash, the source file will be written to the destination path as a file.**

Khi build, `COPY file destdir` sẽ copy `file`, tạo 1 file mới tên là `destdir`.


Để có kết quả giống lệnh cp, cần thêm dấu `/` vào cuối destdir

```
COPY file destdir/
```

**Trailing slashes are significant. For example, COPY test.txt /abs creates a file at /abs, whereas COPY test.txt /abs/ creates /abs/test.txt.**


### Kết luận
Hơi hơi giống không phải là giống, lệnh COPY có sự khác biệt khi thêm dấu `/` vào destination.


Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
