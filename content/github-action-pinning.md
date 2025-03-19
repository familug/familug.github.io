Title: [TIL] Bài học từ vụ GitHub Action tj-actions/changed-file bị hack
Date: 2025/03/19
Category: frontpage
Tags: GHA, GitHub, security, pinning
Slug: github-action-pinning

Ngày 14/3/2025, cộng đồng mạng hoảng loạn vì 1 GitHub Action có tên [tj-actions/changed-file](https://github.com/tj-actions/changed-files) bị hack, thay đổi code, để in ra các token dùng khi chạy GitHub action.
Lý do hoảng loạn: có tới hơn 23 nghìn repo sử dụng action này... để tìm các file đã đổi trong pull request.

Bài viết report sự việc:
<https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised>

### Các vấn về GitHub Action
Có rất nhiều vấn đề khi nhìn lại ở đây, đơn giản như:

- tj-actions là ai?
- gõ mấy câu lệnh để tìm được file đã thay đổi trong 1 git pull request?
- `uses: tj-actions/changed-files@v45` đã cố định ở v45?

### git tag không cố định (mutable)
`@v45` là sử dụng git tag [`v45`](https://github.com/tj-actions/changed-files/releases/tag/v45). `v45` là 1 git tag, và có thể thay đổi, có thể point tới commit khác. Theo `git tag --help`:

> On Re-tagging
> What should you do when you tag a wrong commit and you would want to
> re-tag?
> ..
>  2. The insane thing. You really want to call the new version "X" too, even though others have already seen the old one. So just use git tag -f again, as if you hadn’t already published the old one.

### Giải pháp phòng chống
#### Pinning to SHA commit hash
Vì vậy, để cố định 1 version (gọi là pinning version, phổ biến trong mọi ngôn ngữ lập trình), Theo tài liệu security [best practice của GitHub Action](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-third-party-actions):

> You can help mitigate this risk by following these good practices:
>
>    Pin actions to a full length commit SHA
>
>    Pinning an action to a full length commit SHA is currently the only way to use an action as an immutable release. Pinning to a particular SHA helps mitigate the risk of a bad actor adding a backdoor to the action's repository, as they would need to generate a SHA-1 collision for a valid Git object payload. When selecting a SHA, you should verify it is from the action's repository and not a repository fork.

Tức là viết:

```
uses: tj-actions/changed-files@48d8f15b2aaa3d255ca5af3eba4870f807ce6b3c #v45
```

#### fork action repo
1 giải pháp khác là fork github repo và sử dụng tại repo của mình thay vì repo gốc.

#### không dùng action
Nếu trường hợp không quá phức tạp, có thể viết lệnh git như `git diff main --name-only` để lấy các file thay đổi thay vì dùng github action.

<https://git-scm.com/docs/git-diff#Documentation/git-diff.txt-code--name-onlycode>

### Điều may mắn
vì 1 lý do nào đó, hacker chỉ in token ra mà không gửi nó tới 1 server để thu thập "bí mật" trên toàn cầu.

### Kết luận
git tag không cố định, hãy pin như pin dependency khi code.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
