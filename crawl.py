from utils import crawl_urls, classify_with_openai
from drive_upload import upload_to_drive
import pandas as pd

URLS = [
    "https://conganquangninh.gov.vn/tin-antt-va-canh-bao-toi-pham/",
    "https://conganquangninh.gov.vn/pctp-tren-khong-gian-mang/",
    "https://conganquangninh.gov.vn/thong-bao/thu-doan-toi-pham/"
]

def main():
    rows = []
    stt = 1

    for url in URLS:
        articles = crawl_urls(url)
        for title, link, date in articles:
            result = classify_with_openai(link)
            if result["is_relevant"]:
                rows.append({
                    "STT": stt,
                    "Bài tuyên truyền": title,
                    "Link": link,
                    "Ngày": date,
                    "Đơn vị": "Công an Quảng Ninh",
                    "Loại": result["type"],
                    "Ghi chú": result["note"]
                })
                stt += 1

    if not rows:
        print("Không có bài phù hợp")
        return

    df = pd.DataFrame(rows)
    filename = "tong_hop_khong_gian_mang.xlsx"
    df.to_excel(filename, index=False)

    upload_to_drive(filename)

if __name__ == "__main__":
    main()
