import sys
import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime
import logging


if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class BaoMoiCrawler:
    def __init__(self):
        self.base_url = "https://baomoi.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data = []
        
    def get_article_links(self, page=1):
        """Lấy các link bài viết từ trang chủ hoặc trang phân trang"""
        try:
            url = self.base_url if page == 1 else f"{self.base_url}/trang{page}.epi"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Thử nhiều cách select khác nhau
            articles = soup.find_all('div', class_='story') or \
                      soup.find_all('div', class_='bm_Article') or \
                      soup.find_all('article') or \
                      soup.select('div[class*="story"], div[class*="Article"], article')
            
            links = []
            for article in articles:
                link = article.find('a')
                if link and link.get('href'):
                    href = link['href']
                    if not href.startswith('http'):
                        href = f"{self.base_url}{href}"
                    links.append(href)
            
            return links
            
        except Exception as e:
            logging.error(f"Lỗi khi lấy link bài viết trang {page}: {str(e)}")
            return []
    
    def get_article_data(self, url):
        """Lấy dữ liệu chi tiết từ bài viết"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Lấy tiêu đề - thử nhiều selector khác nhau
            title = (soup.find('h1', class_='article__header') or 
                    soup.find('h1', class_='bm_Article__header') or
                    soup.find('h1')).get_text(strip=True) if soup.find('h1') else ''
            
            # Lấy mô tả
            description = (soup.find('div', class_='article__sapo') or
                         soup.find('div', class_='bm_Article__sapo') or
                         soup.find('meta', attrs={'name': 'description'})).get_text(strip=True) if soup.find('div', class_='article__sapo') or soup.find('div', class_='bm_Article__sapo') else ''
            
            # Lấy hình ảnh
            image = (soup.find('div', class_='article__figure') or
                    soup.find('div', class_='bm_Article__figure') or
                    soup.find('meta', property='og:image'))
            image = image.find('img')['src'] if image and image.find('img') else ''
            
            # Lấy nội dung
            content_div = (soup.find('div', class_='article__body') or
                         soup.find('div', class_='bm_Article__body') or
                         soup.find('article'))
            if content_div:
                paragraphs = content_div.find_all('p')
                content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
            else:
                content = ''
            
            return {
                'title': title,
                'description': description,
                'image': image,
                'content': content,
                'url': url,
                'crawled_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logging.error(f"Lỗi khi lấy dữ liệu từ {url}: {str(e)}")
            return None
    
    def crawl(self, max_pages=1):  # Giảm xuống 1 trang để test
        """Thu thập dữ liệu từ nhiều trang"""
        try:
            for page in range(1, max_pages + 1):
                logging.info(f"Đang thu thập trang {page}")
                print(f"\nĐang thu thập trang {page}...")
                
                article_links = self.get_article_links(page)
                print(f"Tìm thấy {len(article_links)} link bài viết")
                
                for i, link in enumerate(article_links[:5]):  # Giới hạn 5 bài đầu để test
                    print(f"  Đang xử lý bài {i+1}/{len(article_links)}: {link[:50]}...")
                    article_data = self.get_article_data(link)
                    if article_data:
                        self.data.append(article_data)
                    time.sleep(1)  # Tránh bị chặn trang
                
                time.sleep(2)  # Nghỉ giữa các trang
            
            self.save_to_csv()
            logging.info(f"Hoàn thành thu thập {len(self.data)} bài viết")
            print(f"\n==== HOÀN THÀNH ====")
            print(f"Đã thu thập được {len(self.data)} bài viết")
            if self.data:
                print("\n5 bài viết đầu tiên:")
                for i, item in enumerate(self.data[:5]):
                    print(f"\n{i+1}. {item['title']}")
                    print(f"URL: {item['url']}")
        except Exception as e:
            logging.error(f"Lỗi trong quá trình thu thập: {str(e)}")
            print(f"Lỗi: {e}")
    
    def save_to_csv(self):
        """Lưu dữ liệu vào file CSV"""
        try:
            os.makedirs('data/output', exist_ok=True)
            filename = f"data/output/baomoi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logging.info(f"Dữ liệu đã lưu vào {filename}")
            print(f"\nDữ liệu đã lưu vào: {filename}")
        except Exception as e:
            logging.error(f"Lỗi khi lưu CSV: {str(e)}")
            print(f"Lỗi khi lưu file: {e}")

if __name__ == "__main__":
    # Cấu hình logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/crawler.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    crawler = BaoMoiCrawler()
    crawler.crawl(max_pages=1)  # Bắt đầu với 1 trang để test