Title: Tính hash cho hostname trong SSH known_hosts
Date: 20260428
Category: frontpage
Tags: ssh, hash, hmac, sha1
Slug: hash_ssh_known_hosts


### SSH known host là gì 
SSH client lưu trữ danh sách các host key của tất cả các host mà người dùng đã truy cập (ssh vào) trong `~/.ssh/known_hosts` để kiểm tra giá trị này vào lần SSH sau (ngoại lệ xem cuối bài).

> ~/.ssh/known_hosts
> Contains a list of host keys for all hosts the user has logged into that are not already in the systemwide list of known host keys.

Ví dụ 2 dòng trong file known_hosts:

```
github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz
```

Mỗi dòng có định dạng: tên host đã dùng khi kết nối, loại key, và dạng base64 của public host key của host được ssh vào, ngoài ra có thể có comment, mỗi phần cách nhau bởi dấu khoảng trắng (space).
> Each line in these files contains the following fields: marker (optional), hostnames, keytype, base64-encoded key, comment.


### Host key
Mỗi OpenSSH server đều tự sinh (nhiều) cặp host key trong lần đầu chạy. Các cặp host key này nằm trong `/etc/ssh/ssh_host*`
```
$ ls -la /etc/ssh/ssh_host_*                                                                                                                                                                    
-rw------- 1 root root  505 Apr 27 21:18 /etc/ssh/ssh_host_ecdsa_key
-rw-r--r-- 1 root root  173 Apr 27 21:18 /etc/ssh/ssh_host_ecdsa_key.pub
-rw------- 1 root root  399 Apr 27 21:18 /etc/ssh/ssh_host_ed25519_key
-rw-r--r-- 1 root root   93 Apr 27 21:18 /etc/ssh/ssh_host_ed25519_key.pub
-rw------- 1 root root 2590 Apr 27 21:18 /etc/ssh/ssh_host_rsa_key
-rw-r--r-- 1 root root  565 Apr 27 21:18 /etc/ssh/ssh_host_rsa_key.pub
```
Nhiều hệ thống tạo các host key cho các thuật toán như rsa, ecdsa và ed25519.
Khi ssh vào một host, ssh server chọn rồi hiển thị một pub key cho ssh client, client sẽ ghi nội dung này vào file known_hosts.

```sh
ssh 127.0.0.1                                                                                                                                                                                 
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ED25519 key fingerprint is: SHA256:pyugW2eDd0Zdb0cpDUNXQltJQSsIudBGrRgnedlL5lg
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:4: localhost
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '127.0.0.1' (ED25519) to the list of known hosts.
```
Tương tự nếu ssh localhost, sẽ có thêm một dòng trong file known_hosts:

```
127.0.0.1 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIENupkYnPGH10sMOBKaABnYSfVl8KSNo2bO2B83QYRWJ
localhost ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIENupkYnPGH10sMOBKaABnYSfVl8KSNo2bO2B83QYRWJ
```

2 dòng này dù có hostname/IP khác nhau (của cùng 1 server), nhưng cùng một public host key (nội dung /etc/ssh/ssh_host_ed25519_key.pub trên server).


### Dùng hash để ẩn hostname và địa chỉ IP
Để tránh bị lộ các hostname/IP mà người dùng đã truy cập, trong trường hợp bị hacker chiếm quyền SSH vẫn không biết có thể SSH vào các địa chỉ nào, OpenSSH có thêm tính năng cho phép thay domain/IP ở phần đầu mỗi dòng thành dạng hash.

Chạy `ssh-keygen -H` để thực hiện hash các tên hostname/IP trong file known_hosts, và chuyển file ban đầu tới file có thêm đuôi `.old`:
>  -H      Hash a known_hosts file.  This replaces all hostnames and addresses with hashed representations within the specified file; the original content is moved to a file with a .old suffix. 

```sh
$ ssh-keygen -H -f ~/.ssh/known_hosts                                                                                                                                                         
/home/hvn/.ssh/known_hosts updated.
Original contents retained as /home/hvn/.ssh/known_hosts.old
WARNING: /home/hvn/.ssh/known_hosts.old contains unhashed entries
Delete this file to ensure privacy of hostnames
```

Ví dụ sau khi hash:

```
|1|1yLv1MYg3e3HDK+8IKFfJhtCNCw=|CrQpRw2fNTP3SZJ+povIK/ko2Ys= ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
|1|om6Oxzr+1drcW1yy15GKEjwZe/o=|Nxqyg7tgIHut5QsMJWbuwDLbRis= ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk=
```

Định dạng sau khi hash: `|1|SALT|hashed_hostname|key_type b64_public_host_key comment`. Với |1| là đánh dấu phiên bản cho HMAC-SHA1.

### Tự tính hashed hostname bằng Python
Hashed hostname được tính bằng `hmac_sha1(SALT, hostname)`, với SALT được sinh ngẫu nhiên khi tính.

Trong ví dụ: 
`|1|1yLv1MYg3e3HDK+8IKFfJhtCNCw=|CrQpRw2fNTP3SZJ+povIK/ko2Ys= ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl`
Salt đã được biểu diễn ở dạng base64, giá trị: `1yLv1MYg3e3HDK+8IKFfJhtCNCw=`.
Code Python:

```py
import hmac
import hashlib
import base64

def calculate_ssh_hash(hostname, salt_base64):
    # 1. Decode the salt from base64
    salt = base64.b64decode(salt_base64)
    
    # 2. Compute HMAC-SHA1(salt, hostname)
    # The hostname must be encoded as bytes
    hasher = hmac.new(salt, hostname.encode('utf-8'), hashlib.sha1)
    
    # 3. Base64 encode the result
    digest = hasher.digest()
    return base64.b64encode(digest).decode('utf-8')

# Example Usage
# Salt found in known_hosts (after |1|)
salt_b64 = "1yLv1MYg3e3HDK+8IKFfJhtCNCw="
hostname = "github.com"

hashed_host = calculate_ssh_hash(hostname, salt_b64)
print(f"Hashed Hostname: {hashed_host}")
# python3 gen.py                                                                                                                                                                    
Hashed Hostname: CrQpRw2fNTP3SZJ+povIK/ko2Ys=
```

Hoặc dùng một câu lệnh openssl:

```sh
$ echo -n "github.com" | openssl sha1 -binary -mac HMAC -macopt hexkey:$(echo "1yLv1MYg3e3HDK+8IKFfJhtCNCw=" | base64 --decode | xxd -p) | base64
CrQpRw2fNTP3SZJ+povIK/ko2Ys=
```

### Đọc code ssh-keygen xem code C để tính hashed host key
```C
/* XXX hmac is too easy to dictionary attack; use bcrypt? */
char *
host_hash(const char *host, const char *name_from_hostfile, u_int src_len)
{
	struct ssh_hmac_ctx *ctx;
	u_char salt[256], result[256];
	char uu_salt[512], uu_result[512];
	char *encoded = NULL;
	u_int len;

	len = ssh_digest_bytes(SSH_DIGEST_SHA1);

	if (name_from_hostfile == NULL) {
		/* Create new salt */
		arc4random_buf(salt, len);
	} else {
		/* Extract salt from known host entry */
		if (extract_salt(name_from_hostfile, src_len, salt,
		    sizeof(salt)) == -1)
			return (NULL);
	}

	if ((ctx = ssh_hmac_start(SSH_DIGEST_SHA1)) == NULL ||
	    ssh_hmac_init(ctx, salt, len) < 0 ||
	    ssh_hmac_update(ctx, host, strlen(host)) < 0 ||
	    ssh_hmac_final(ctx, result, sizeof(result)))
		fatal_f("ssh_hmac failed");
	ssh_hmac_free(ctx);

	if (__b64_ntop(salt, len, uu_salt, sizeof(uu_salt)) == -1 ||
	    __b64_ntop(result, len, uu_result, sizeof(uu_result)) == -1)
		fatal_f("__b64_ntop failed");
	xasprintf(&encoded, "%s%s%c%s", HASH_MAGIC, uu_salt, HASH_DELIM,
	    uu_result);

	return (encoded);
}
```
[openssh/openssh-portable/hostfile.c](https://github.com/openssh/openssh-portable/blob/b9ccca0edfbd46b3114192956d9aaea3e7bc3c08/hostfile.c#L115-L151)

### Khi ssh không dùng known host
Câu lệnh ssh có option để chọn file known_hosts, chọn file khác sẽ khiến ssh không update file mặc định ~/.ssh/known_hosts:

```
ssh -o UserKnownHostsFile=/dev/null 192.168.1.15
```

### Kết luận
Hashed hostname không dịch ngược được, nhưng khi có danh sách domain/IP để làm đầu vào, hoàn toàn có thể tính ra.

### Tham khảo
- HMAC tại [python hmac stdlib](https://docs.python.org/3.14/library/hmac.html).

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
