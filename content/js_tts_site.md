Title: Làm website đọc chữ phát ra loa với 10 dòng code (no lib, no install)
Date: 2024-02-08
Category: frontpage
Tags: javascript, JS, browser api, TTS, text-to-speech

Sau khi có thể [đọc text bằng 5 dòng code]({filename}/js_tts.md), làm luôn trang web.

## Tạo site HTML 
Tạo 1 ô nhập text (textarea) và 1 nút bấm (button)

```html
<html>
	<body>
		<textarea id="text" rows="24" cols="100">
		 In my younger and more vulnerable years my father gave me some advice that I’ve been turning over in my mind ever since.

		“Whenever you feel like criticizing anyone,” he told me, “just remember that all the people in this world haven’t had the advantages that you’ve
		</textarea>
		<br>
		<button id="speak">Speak</button>
	<body>
</html>
```

## Đọc text khi click chuột
```js
button = document.getElementById("speak");

function speak() {
    synth = window.speechSynthesis
    text = document.getElementById("text").value;
    utter = new SpeechSynthesisUtterance(text)
    voices = synth.getVoices()
    utter.rate = 0.9 // speed - tốc độ
    synth.speak(utter)
}

button.addEventListener('click', speak);
```

Dòng `text = document.getElementById("text").value` lấy nội dung trong ô textarea để đọc.
## Kết quả
Xem tại <https://hvnsweeting.github.io/js-toys/tts.html>

## Kết luận
Giờ đã có thể dùng điện thoại để đọc text trên trang web dựa trên 5 dòng code ban đầu.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
