Title: [TIL] RFC cho định dạng CSV chỉ có 7 dòng 
Date: 2025-04-04
Category: frontpage
Tags: csv, rfc
Slug: csv-rfc

RFC mô tả các tài tiêu chuẩn kỹ thuật trên internet.

> RFC - Requests for Comments. They describe the Internet's technical foundations, such as addressing, routing, and transport technologies. RFCs also specify protocols like TLS 1.3, QUIC, and WebRTC that are used to deliver services used by billions of people every day, such as real-time collaboration, email, and the domain name system.
<https://www.ietf.org/process/rfcs/>

RFC thường dài, chi tiết và khô khan khó đọc (như RFC cho HTTP1.1 <https://www.rfc-editor.org/rfc/rfc2616> gần 180 pages), nhưng RFC cho CSV (không) ngạc nhiên ngắn gọn đơn giản trong 7 dòng:

<https://www.rfc-editor.org/rfc/rfc4180#section-2>
```
 1.  Each record is located on a separate line, delimited by a line
       break (CRLF).  For example:

       aaa,bbb,ccc CRLF
       zzz,yyy,xxx CRLF

   2.  The last record in the file may or may not have an ending line
       break.  For example:

       aaa,bbb,ccc CRLF
       zzz,yyy,xxx

   3.  There maybe an optional header line appearing as the first line
       of the file with the same format as normal record lines.  This
       header will contain names corresponding to the fields in the file
       and should contain the same number of fields as the records in
       the rest of the file (the presence or absence of the header line
       should be indicated via the optional "header" parameter of this
       MIME type).  For example:

       field_name,field_name,field_name CRLF
       aaa,bbb,ccc CRLF
       zzz,yyy,xxx CRLF


   4.  Within the header and each record, there may be one or more
       fields, separated by commas.  Each line should contain the same
       number of fields throughout the file.  Spaces are considered part
       of a field and should not be ignored.  The last field in the
       record must not be followed by a comma.  For example:

       aaa,bbb,ccc

   5.  Each field may or may not be enclosed in double quotes (however
       some programs, such as Microsoft Excel, do not use double quotes
       at all).  If fields are not enclosed with double quotes, then
       double quotes may not appear inside the fields.  For example:

       "aaa","bbb","ccc" CRLF
       zzz,yyy,xxx

   6.  Fields containing line breaks (CRLF), double quotes, and commas
       should be enclosed in double-quotes.  For example:

       "aaa","b CRLF
       bb","ccc" CRLF
       zzz,yyy,xxx

   7.  If double-quotes are used to enclose fields, then a double-quote
       appearing inside a field must be escaped by preceding it with
       another double quote.  For example:

       "aaa","b""bb","ccc"
```
### Tham khảo 
- [A love letter to the CSV format](https://github.com/medialab/xan/blob/master/docs/LOVE_LETTER.md)

### Kết luận

CSV đơn giản.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
