Title: [TIL] Docker trên MacOS share toàn bộ thư mục $HOME /Users/you với Docker Machine
Date: 2025/09/26
Category: frontpage
Tags: docker, podman, container, vm, macos
Slug: til-docker-desktop-mount

Docker chạy được trên các hệ điều hành không phải Linux là 1 điều kỳ diệu.
Điều kỳ diệu ấy nhờ việc các hệ điều hành tạo ra một máy ảo Linux rồi chạy container trên đó. Máy ảo này thường gọi là Docker machine, Podman machine, hay cái gì đó machine.

Nhưng làm thế nào khi bind mount: `-v $PWD:/app`, thư mục hiện tại trên MacOS, ví dụ `/Users/pikachu/fml` lại xuất hiện trong container?

### Share /Users cho máy ảo
Hầu hết người dùng đều mount từ 1 thư mục nào đó trong "$HOME" của user vào container, vậy nên mặc định Docker machine share sẵn thư mục này, bao gồm tất cả mọi thứ, kể cả .bashrc hay .ssh, ...

> Virtual file shares
> By default the /Users, /Volumes, /private, /tmp and /var/folders directory are shared.
> If your project is outside this directory then it must be added to the list, otherwise you may get Mounts denied or cannot start service errors at runtime.
> <https://docs.docker.com/desktop/settings-and-maintenance/settings/#virtual-file-shares>

Vì thư mục được mount nằm trong `/Users`, đã được share với máy ảo cũng tại path `/Users`, nên từ máy ảo cứ thế bind mount file vào container mà dùng.

```
-v, --volume stringArray Bind mount a volume into the container
```

Code [Podman](https://github.com/containers/podman/blob/a118fdf4e2343dcafa6b14331fc99a8d68dd761b/vendor/go.podman.io/common/pkg/config/default_darwin.go#L16-L22):
```
#vendor/go.podman.io/common/pkg/config/default_darwin.go
// getDefaultMachineVolumes returns default mounted volumes (possibly with env vars, which will be expanded)
func getDefaultMachineVolumes() []string {
        return []string{
                "/Users:/Users",
                "/private:/private",
                "/var/folders:/var/folders",
        }
}
```

### Kết luận
Người dùng Podman Desktop cũng có thể gõ `podman machine ssh` rồi `ls /Users` để khám phá mọi thứ như trên MacOS.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
