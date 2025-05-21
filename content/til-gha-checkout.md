Title: [TIL] GitHub Action actions/checkout mặc định checkout merge commit với pull_request
Date: 2025/05/21
Category: frontpage
Tags: github action, gha, checkout
Slug: til-gha-checkout

GitHub Action [@actions/checkout](https://github.com/actions/checkout)
xuất hiện ở gần như mọi GitHub Action workflow.

Khi người dùng tạo Repository, GitHub sẽ gợi ý bằng 1 nút bấm trên giao diện để add GitHub action phù hợp với ngôn ngữ lập trình dùng chính trong repo.
Ví dụ Python <https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python>
```
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: Python application

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
# ...
```
Nó có vẻ làm những gì người dùng mong đợi: chứa các file code ở branch đã push lên, vì vậy, không mấy ai thực sự xem doc/code hay biết nó thực sự làm gì.

Thậm chí bấm vào GitHub repo  <https://github.com/actions/checkout> dòng đầu viết:

>This action checks-out your repository under $GITHUB_WORKSPACE, so your workflow can access it.
>Only a single commit is fetched by default, for the ref/SHA that triggered the workflow. Set fetch-depth: 0 to fetch all history for all branches and tags. Refer [here](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows) to learn which commit $GITHUB_SHA points to for different events.

và nếu người dùng chịu bấm vào link "here" sẽ thấy 1 bảng tương đối khó hiểu.

- Action này khi được trigger bằng event `push` - tức người dùng push lên, trong  ví dụ trên, sẽ chỉ trigger nếu người dùng push lên `main`, action sẽ  checkout branch `main` tại 1 commit mới nhất được push lên - HEAD).
- Còn khi được trigger bằng event `pull_request` - tức người dùng tạo/thay đổi pull request (push lên branch cũng tính là 1 `synchronize` event của pull_request) thì action sẽ checkout merge commit.

Theo tài liệu [here](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#pull_request) nói trên: 
> Last merge commit on the GITHUB_REF branch	PR merge branch refs/pull/PULL_REQUEST_NUMBER/merge

Đọc HẾT tài liệu [README checkout v4](https://github.com/actions/checkout/blob/85e6279cec87321a52edac9c87bce653a07cf6c2/README.md) có viết

> Checkout pull request HEAD commit instead of merge commit

sẽ thấy có viết mặc định action checkout merge commit, ví dụ như sau:

```
  commit ab735464a83c5cd8efbd09888fce2168c8f5e49b
Merge: 3c771ec 80992e0
Author: GitHub user
Date:   Wed May 21 09:45:29 2025 +0000

    Merge 80992e095099699f3191c038070742a3ef78e435 into 3c771ec7abd340d7382bd4129a0c62a1be3e7c66
```

Đây là commit sau khi merge branch tạo Pull Request (còn gọi là pull request head) vào merge target (còn gọi là pull request base, thường là `main` hay `master` branch).

Merge commit này chứa thông tin về quá trình merge, tức có thể biết các file nào đã thay đổi (nhưng không biết nội dung thay đổi), nên có thể dùng để tìm các file đã thay đổi chỉ cần fetch-depth 2 commit mới nhất:

```
- name: Checkout
  uses: actions/checkout@v3
  with:
     fetch-depth: 2
- name: Get changes
  run: git diff --name-only HEAD^1 HEAD
```
### Kết luận
Nhiều lúc không cần dùng tới <https://github.com/tj-actions/changed-files>

### Tham khảo
<https://stackoverflow.com/a/74268200/807703>

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
