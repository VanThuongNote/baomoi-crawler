# BaoMoi Crawler - Công cụ thu thập tin tức tự động

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.9+-green.svg)
![Pandas](https://img.shields.io/badge/pandas-1.2+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Công cụ thu thập dữ liệu tin tức từ Báo Mới (baomoi.com) bằng Python, tự động lưu dữ liệu dạng CSV.
## Cách sử dụng

Chạy thủ công:
```bash
python -m crawler.baomoi_crawler
```

Chạy scheduler (tự động 6h sáng hàng ngày):
```bash
python -m crawler.scheduler

## Tính năng nổi bật

- ✔️ Thu thập tin tức từ trang chủ và các trang phân trang
- ✔️ Tự động phát hiện và xử lý lỗi encoding UTF-8
- ✔️ Lấy đầy đủ thông tin bài viết:
  - Tiêu đề
  - Mô tả
  - Hình ảnh đại diện
  - Nội dung chính
  - URL gốc
  - Thời gian thu thập
- ✔️ Hệ thống logging chi tiết
- ✔️ Tự động lưu dữ liệu dạng CSV (hỗ trợ Unicode)
- ✔️ Cơ chế tránh bị chặn với random delay

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/VanThuongNote/baomoi-crawler.git
cd baomoi-crawler