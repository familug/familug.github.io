Title: tại sao CA ok trên Chrome còn Firefox báo không hợp lệ
Date: 2023-11-12
Category: frontpage
Tags: Firefox, Chrome, Certificate

Trên MacOS, nếu một trang web nội bộ khi vào bằng Chrome thì bình thường, còn Firefox báo private certificate authorities không hợp lệ (CA không hợp lệ), tại sao?

## Mặc định không giống nhau
Chrome (119) mặc định lấy CA từ Apple keystore, và Macbook được cài sẵn các CA của công ty.

Firefox mặc định set

```
security.enterprise_roots.enabled = false
```

cần vào trang `about:config` rồi tìm và set option này thành 1.

<https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox>

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
