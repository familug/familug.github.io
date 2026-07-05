Title: [TIL] requests đoán "có giáo dục" encoding và có thể sai
Date: 2025-10-04
Category: frontpage
Tags: python, requests, encoding, http
Slug: til_requests_encoding

`requests` là thư viện HTTP client phổ biến nhất của Python, nó phổ biến vì dễ dùng, chỉ cần `import requests; requests.get` là xong.
Trông dễ như vậy bởi `requests` đã cấu hình mặc định hết rất nhiều thứ như: connection, headers, adapter, session, encoding, ... mà mặc định thì nhiều khi đúng, đôi khi sai.

## Encoding
Vì Python mặc định encoding trên Linux là `utf-8`, người dùng dễ mặc định là `requests` cũng vậy, nhưng thực tế thì:

[Tài liệu](https://github.com/psf/requests/blob/v2.32.5/docs/user/quickstart.rst?plain=1#L84-L121) viết:

> When you make a request, Requests makes educated guesses about the encoding of the response based on the HTTP headers. The text encoding guessed by Requests is used when you access r.text. You can find out what encoding Requests is using, and change it, using the r.encoding property:

> r.encoding
> 'utf-8'

> r.encoding = 'ISO-8859-1'

> If you change the encoding, Requests will use the new value of r.encoding whenever you call r.text. You might want to do this in any situation where you can apply special logic to work out what the encoding of the content will be. For example, HTML and XML have the ability to specify their encoding in their body. In situations like this, you should use r.content to find the encoding, and then set r.encoding. This will let you use r.text with the correct encoding.

`requests` thực hiện "đoán một cách có học" (educated guesses) encoding của response dựa trên HTTP headers <https://github.com/psf/requests/blob/v2.32.5/src/requests/adapters.py#L355>.
```py
    response.encoding = get_encoding_from_headers(response.headers)
```

Xem code thấy nó chỉ dựa trên header `content-type`:
```py
def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    :rtype: str
    """

    content_type = headers.get("content-type")

    if not content_type:
        return None

    content_type, params = _parse_content_type_header(content_type)

    if "charset" in params:
        return params["charset"].strip("'\"")

    if "text" in content_type:
        return "ISO-8859-1"

    if "application/json" in content_type:
        # Assume UTF-8 based on RFC 4627: https://www.ietf.org/rfc/rfc4627.txt since the charset was unset
        return "utf-8"
# https://github.com/psf/requests/blob/v2.32.5/src/requests/utils.py#L529-L551
```
nếu có `charset` trong `content-type` `requests` sẽ dùng giá trị của charset. Ví dụ:

```
Content-Type: text/html; charset=utf-8
```
Khi không có `charset`, nếu `content-type` chứa `text` dùng `ISO-8859-1`, còn nếu là `json` dùng `utf-8`.
Vậy khi dùng với các JSON API, `requests` sẽ dùng `utf-8` nên kết quả luôn như mong đợi, nhưng nếu lấy trang HTML, khi header không set, encoding có thể bị sai.

### resp.content vs resp.text
`content` và `text` là 2 property của response object, `content` chứa byte và người dùng có thể tự `decode` với encoding tùy ý.
`text` đọc `.encoding` rồi decode:

```py
In [48]: url = 'https://podcasts.apple.com/jp/podcast/%E3%81%AA%E3%81%8C%E3%82%89%E6%97%A5%E7%B5%8C/id1627014612'
In [49]: resp = requests.get(url)
In [50]: print(resp.encoding)
ISO-8859-1
In [51]: print(resp.headers.get('Content-Type'))
text/html
```
do header `Content-Type` không có `charset`, lại chứa `text`, nên `requests` set `encoding = 'ISO-8859-1'`

```py
In [54]: resp.text.split("<title>")[1].split("</title>")[0]
Out[54]: 'ã\x81ªã\x81\x8cã\x82\x89æ\x97¥çµ\x8c - ã\x83\x9dã\x83\x83ã\x83\x89ã\x82\xadã\x83£ã\x82¹ã\x83\x88 - Apple Podcast'

In [55]: resp.content.split(b"<title>")[1].split(b"</title>")[0].decode("utf-8")
Out[55]: 'ながら日経 - ポッドキャスト - Apple Podcast'
```

tự set `encoding = 'utf-8'` để text hiển thị đúng:
```py
In [56]: resp.encoding = 'utf-8'

In [57]: resp.text.split("<title>")[1].split("</title>")[0]
Out[57]: 'ながら日経 - ポッドキャスト - Apple Podcast'

In [62]: resp.connection
Out[62]: <requests.adapters.HTTPAdapter at 0x772dba31ccd0>
```

PS: curl cũng encode đúng với utf-8:
```
$ curl -s https://podcasts.apple.com/jp/podcast/%E3%81%AA%E3%81%8C%E3%82%89%E6%97%A5%E7%B5%8C/id1627014612 | grep -o '<title>.*</title>'
<title>ながら日経 - ポッドキャスト - Apple Podcast</title>
```

Xem code method `text`:

```py
    @property
    def text(self):
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``charset_normalizer`` or ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """

        # Try charset from content-type
        content = None
        encoding = self.encoding

        if not self.content:
            return ""

        # Fallback to auto-detected encoding.
        if self.encoding is None:
            encoding = self.apparent_encoding

        # Decode unicode from given encoding.
        try:
            content = str(self.content, encoding, errors="replace")
        except (LookupError, TypeError):
            # A LookupError is raised if the encoding was not found which could
            # indicate a misspelling or similar mistake.
            #
            # A TypeError can be raised if encoding is None
            #
            # So we try blindly encoding.
            content = str(self.content, errors="replace")

        return content
```
<https://github.com/psf/requests/blob/v2.32.5/src/requests/models.py#L909>

### Kết luận
`requests` dễ nhưng không đơn giản.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
