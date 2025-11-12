Title: Thẻ HTML link rel=alternate
Date: 2025/11/12
Category: frontpage
Tags: html, link, alternate
Slug: til-html-link-rel-alternate

Trong HTML, thẻ `<link>` thường dùng để chỉ định việc dùng file CSS hay favicon:

```html
<link rel="stylesheet" type="text/css" href="./theme/css/custom.css" media="screen">
<link rel="icon" href="favicon.ico" />
```
> The `<link>` HTML element specifies relationships between the current document and an external resource. This element is most commonly used to link to stylesheets, but is also used to establish site icons (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things. <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/link>

Ngoài hai [`rel` (relation)](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel) `stylesheet`, `icon` nói trên, còn nhiều giá trị khác, trong đó đáng chú ý là `alternate`

> The rel attribute defines the relationship between a linked resource and the current document
> Alternate representations of the current document.

`rel="alternate"` dùng để link tới các biểu diễn khác của trang web hiện tại:

- trang dành riêng cho ngôn ngữ khác
- biểu diễn khác thay vì HTML: RSS/XML - RSS feed

Ví dụ trên <https://wordpress.com>:

```html
<link rel="alternate" hreflang="ja" href="https://wordpress.com/ja/" />
<link rel="alternate" hreflang="vi" href="https://wordpress.com/vi/" />
<link rel="alternate" type="application/rss+xml" title="WordPress.com Blog" href="https://wordpress.com/blog/feed/" />
<link rel="alternate" type="application/rss+xml" title="WordPress.com Discover" href="//discover.wordpress.com/feed/" />
```

Các chương trình đọc RSS có thể tự tìm trong pagesource các thẻ link để tìm ra đường dẫn tới feed, kể cả chúng không hiện lên trang chủ.

### Kết luận
`<link rel="alternate">` là nơi chứa thông tin bất ngờ, dù không hiện lên màn hình.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
