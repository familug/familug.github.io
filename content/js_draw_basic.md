Title: Vẽ hình vuông hình tròn: bánh chưng và mặt trời
Date: 2024-02-11
Category: frontpage
Tags: javascript, JS, browser api, canvas, html5,

HTML5 xuất hiện từ 2008 và đến nay sau 16 năm đã được phổ cập trên mọi trình duyệt. Điển hình nhất là ngày nay xem video trên Youtube không còn phải cài Adobe Flash nữa mà cứ bấm là xem.

HTML5 có thể làm rất nhiều việc mà trước đây cần phần mềm khác/JavaScript:
- xem video
- nghe nhạc
- vẽ hình 2D 3D
- tạo hình động
- ... vậy nên người ta có thể làm game với HTML5 + JavaScript

Bài này khám phá thẻ canvas trong HTML5 và vẽ bánh chưng mừng tuổi mọi người, hello 2024!

![banh chung va mat troi]({static}/images/rect_arc.png)
## Canvas - vẽ hình 
Thẻ [canvas](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas) chỉ có 2 thuộc tính width (300) và height (150), việc vẽ hình được thực hiện bằng JavaScript.

Tạo cặp thẻ HTML canvas rồi lấy object "context" 2D để vẽ hình 2D.

```html
    <canvas id="banh" width=300 height=300></canvas>
    </div>
    
    <script>
      canvas = document.getElementById("banh");
      ctx = canvas.getContext("2d");
      //...
    </script>
```

Vẽ hình chữ nhật với `fillRect` (rectangle), chọn màu bằng gán giá trị cho `ctx.fillStyle`.

Vẽ cái bánh chưng: trước tiên là đổ màu lá full hình vuông, 
sau đó đổi màu rồi vẽ 4 cái lạt, cuối cùng thêm dòng chữ vào góc cho giống VTV:

```js
      //ctx.fillRect(x, y, width, height);
      ctx.fillStyle = '#44583b';
      ctx.fillRect(0, 0, 300, 300);

      ctx.fillStyle = '#c7cab8';
      ctx.fillRect(95, 0, 10, 300);
      ctx.fillRect(195, 0, 10, 300);
      ctx.fillRect(0, 95, 300, 10);
      ctx.fillRect(0, 195, 300, 10);
      
      ctx.fillText("Chung cake", 240, 20)
```

## Vẽ hình tùy ý
Vẽ hình tự do bằng cách bắt đầu với `beginPath()`, di chuyển "bút", khi xong thì `fill()` để tô màu hình kính tạo bởi đường vẽ.

Dùng `arc` để vẽ hình tròn 

`arc(x, y, radius, startAngle, endAngle, counterclockwise)`

Vẽ cờ nước Nhật: tỷ lệ h:w 3:2, đường kính mặt trời 3/5 chiều cao:

```js
      canvas = document.getElementById("jp");
      ctx = canvas.getContext("2d");
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, 300, 200);

      ctx.fillStyle = '#ff2b2a';
      ctx.beginPath();
      ctx.arc(150, 100, 60, 0, 2 * 3.14, false);
      ctx.fill();
      ctx.fillText("JP", 280, 20)
```
## Tham khảo
- <https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Drawing_graphics>

## Kết luận
Vẽ vuông vẽ tròn thật đơn giản, thế còn vẽ lá cờ đỏ sao vàng Việt Nam? xem như 1 bài tập về nhà.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
