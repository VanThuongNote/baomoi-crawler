import schedule
import time
from crawler.baomoi_crawler import BaoMoiCrawler
import logging

# Cấu hình logging
logging.basicConfig(
    filename='logs/scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def crawl_job():
    """Công việc thu thập dữ liệu tự động"""
    logging.info("Bắt đầu công việc thu thập tự động")
    try:
        crawler = BaoMoiCrawler()
        crawler.crawl(max_pages=5)
        logging.info("Hoàn thành công việc thu thập")
    except Exception as e:
        logging.error(f"Lỗi trong công việc tự động: {str(e)}")

# Thiết lập lịch chạy vào 6h sáng hàng ngày
schedule.every().day.at("06:00").do(crawl_job)

if __name__ == "__main__":
    logging.info("Bộ lập lịch đã khởi động")
    while True:
        schedule.run_pending()
        time.sleep(60)  