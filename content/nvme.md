Title: SSD NVMe vs SATA, DisplayPort vs HDMI, USB downstream port
Date: 2023-07-12
Category: frontpage
Tags: SSD, NVMe, SATA, DP, HDMI, USB, hardware, PCIe, M.2

<center>
![USB Downstream - DisplayPort]({static}/images/dp_usbdownstream.jpg)

^---- USB Downstream | DisplayPort ----^
</center>
## SSD NVMe khác gì SSD SATA
Solid-state Drive (SSD) là thế hệ ổ cứng mới, không sử dụng đĩa quay như Hard Disk Drive (HDD),
SSD tốc độ nhanh gấp 5 tới vài trăm lần so với HDD.
### SATA là gì
Serial ATA (SATA) (~2004) là công nghệ sử dụng AHCI driver giao tiếp với ổ cứng HDD, công nghệ này cũng được
dùng với SSD giúp cắm được vào các máy tính đời cũ, nhưng cản trở SSD bung mình bứt phá.

Các ổ cứng SATA **THƯỜNG** có hình chữ nhật giống bao thuốc lá.

### NVMe là gì
Non-Volatile Memory Express (NVMe) (~2011) driver được thiết kế cho SSD, kết hợp sử dụng khe cắm PCIe, cho tốc độ nhanh hơn SATA có thể lên tới 100 lần.

Các ổ cứng NVMe **THƯỜNG** dài thon như 2 ngón tay, hay phong kẹo cao su.

```sh
$ mount | grep ' on / '
/dev/nvme0n1p1 on / type ext4 (rw,relatime,errors=remount-ro)
```

## M.2 2280 vs 2.5 inch
NVMe và SATA là các chuẩn giao tiếp, không phải hình dáng của ổ cứng. Hình dáng (form factor) có 2 loại phổ biến:

- 2.5 inch: hình dáng truyền thống của ổ HDD cho laptop, sau đó là SSD sử dụng SATA.
- M.2 2280: (đọc là m dot two) 22 80: rộng 22mm dài 80mm, là kiểu dáng phổ biến của SDD sử dụng NVMe.

Giao thức có ảnh hưởng tới hình dáng, nhưng không quyết định. Vẫn có SSD có dáng M.2 dùng SATA mặc dù ngày càng ít.
M.2 SATA sẽ có 2 "khe" thay vì M.2 NVMe chỉ có 1 "khe", xem hình tại [kingston](https://www.kingston.com/en/blog/pc-performance/two-types-m2-vs-ssd) hay các trang web bán phần cứng máy tính.

## PCIe 3x4
PCI Express (Peripheral Component Interconnect Express) PCIe, là giao diện phần cứng để lắp các thiết bị máy tính (VGA, SSD, ...) ngày nay.

- PCIe thế hệ 3 gọi là PCIe 3, phiên bản 3.0 có từ 2010 và được sản xuất phổ biến nhất tại 2023, với giá rẻ nhất.
- PCIe 4 đã xuất hiện với các thiết bị tầm trung.
- PCIe 5 còn hiếm.
- PCIe 6 đã có ở đâu đó và 7 đang được lên kế hoạch.

PCIe có thể chứa nhiều lane cùng gửi nhận tín hiệu cùng lúc làm tăng tốc độ, x4 là 4 lane, x16 là 16 lane về lý thuyết nhanh hơn x4 4 lần.
M.2 có thể sử dụng tối đa 4 lane (x4).

<https://en.wikipedia.org/wiki/PCI_Express#History_and_revisions>

## Đọc thông số 1 ổ cứng SSD
Tới đây đã có thể giải mã thông số khi mua ổ cứng SSD, ví dụ:
`XPG SPECTRIX PCIe Gen3x4 M.2 2280 Solid State Drive`:

- PCIe 3 với 4 lane
- M.2 form rộng 22mm dài 80mm

## DisplayPort (DP) vs HDMI
Các cổng/dây cắm truyền hình ảnh từ máy tính qua màn hình:

```
VGA -> DVI -> HDMI -> DP
```

DisplayPort (DP) là công nghệ mới hơn HDMI, với các chỉ số vượt trội. Ngày nay hầu hết các màn hình đều có kèm dây DP nhưng người dùng vẫn quen dùng dây HDMI. DisplayPort cũng có thể sử dụng qua khe cắm USB-C (VD: MacBook).

### USB Downstream port sau màn hình máy tính
USB Downstream là cổng cắm sau các màn hình ngày nay, có hình gần vuông, để với đầu kia cắm vào 1 cổng USB trên máy tính, cho phép sử dụng các cổng USB trên màn hình thay vì cắm trực tiếp vào máy tính, hoạt động như 1 USB Hub.

## Tham khảo
- <https://www.kingston.com/en/blog/pc-performance/nvme-vs-sata>
- <https://www.kingston.com/en/blog/pc-performance/pcie-gen-4-explained>
- <https://hackaday.com/2023/07/11/displayport-a-better-video-interface/>
- <https://downloads.dell.com/manuals/all-products/esuprt_electronics_accessories/esuprt_electronics_accessories_monitors/dell-p2319h-monitor_user%27s-guide_en-us.pdf>
- <https://superuser.com/questions/856297/what-do-the-upstream-downstream-usb-ports-on-a-monitor-do#856348>

## Kết luận
Khi phần mềm thay đổi mỗi 2 năm thì phần cứng cũng không thua kém gì, không update, sẽ bị dated.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
