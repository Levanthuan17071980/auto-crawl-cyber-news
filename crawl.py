import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://baomoi.com"

# Trang tìm kiếm / tổng hợp theo từ khóa
SEARCH_URLS = [
    "https://baomoi.com/search?q=lừa%20đảo%20trực%20tuyến",
    "https://baomoi.com/search?q=không%20gian%20mạng",
    "https://baomoi.com/search?q=công%20nghệ%20cao",
    "https://baomoi.com/search?q=an%20ninh%20mạng",
    "https://baomoi.com/search?q=facebook",
    "https://baomoi.com/search?q=đánh%20bạc%20trực%20tuyến"
]

KEYWORDS = [
    "lừa đảo",
    "trực tuyến",
    "công nghệ cao",
    "không gian mạng",
    "mạng xã hội",
    "facebook",
    "đánh bạc",
    "an ninh mạng"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def crawl_baomoi():
    data = []
    stt = 1
    visited_links = set()

    for url in SEARCH_URLS:
        print("Đang crawl:", url)
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")

        # Card bài viết của Báo Mới
        articles = soup.select("a[href^='/']")

        for a in articles:
            title = a.get_text(strip=True)
            link = a.get("href")

            if not title or len(title) < 20:
                continue

            if not any(k.lower() in title.lower() for k in KEYWORDS):
                continue

            full_link = BASE_URL + link
            if full_link in visited_links:
                continue

            visited_links.add(full_link)

            data.append([
                stt,
                title,
                full_link,
                datetime.now().strftime("%d/%m/%Y"),
                "Báo Mới (tổng hợp)",
                "Tuyên truyền / Cảnh báo",
                "Nội dung liên quan không gian mạng"
            ])
            stt += 1

        time.sleep(2)  # tránh crawl quá nhanh

    return data

def main():
    rows = crawl_baomoi()

    if not rows:
        print("Không tìm thấy bài phù hợp.")
        return

    df = pd.DataFrame(rows, columns=[
        "STT",
        "Bài tuyên truyền",
        "Link",
        "Ngày",
        "Đơn vị",
        "Loại",
        "Ghi chú"
    ])

    filename = f"baomoi_khong_gian_mang_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df.to_excel(filename, index=False)

    print("✅ Đã tạo file:", filename)

if __name__ == "__main__":
    main()
