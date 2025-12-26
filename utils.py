import requests
from bs4 import BeautifulSoup
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def crawl_urls(page_url):
    r = requests.get(page_url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for item in soup.select("article"):
        a = item.find("a", href=True)
        if not a:
            continue

        title = a.get_text(strip=True)
        link = a["href"]
        if not link.startswith("http"):
            link = "https://conganquangninh.gov.vn" + link

        date_tag = item.find("time")
        date = date_tag.get_text(strip=True) if date_tag else ""

        if title:
            results.append((title, link, date))
    return results


def classify_with_openai(article_url):
    try:
        html = requests.get(article_url, headers=HEADERS, timeout=15).text
    except:
        return {"is_relevant": False}

    soup = BeautifulSoup(html, "html.parser")
    content = " ".join(p.get_text(strip=True) for p in soup.select("article p"))

    if len(content) < 200:
        return {"is_relevant": False}

    prompt = f"""
Bạn là cán bộ Công an, nhiệm vụ là sàng lọc bài viết liên quan KHÔNG GIAN MẠNG.

Chỉ đánh giá CÓ nếu bài liên quan:
- Lừa đảo, đánh bạc trực tuyến
- Tội phạm sử dụng công nghệ cao
- Mạng xã hội (Facebook, Zalo, TikTok...)
- Tuyên truyền, cảnh báo an ninh mạng

Nếu không liên quan → ghi: KHÔNG PHÙ HỢP

Nếu có → ghi đúng mẫu:

PHÙ HỢP
Loại: (Tội phạm công nghệ cao / Mạng xã hội / Tuyên truyền – An ninh mạng)
Ghi chú: (1 câu ngắn)

Nội dung:
\"\"\"{content[:3500]}\"\"\"
"""

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    answer = resp.choices[0].message["content"]

    if answer.startswith("KHÔNG"):
        return {"is_relevant": False}

    loai, note = "", ""
    for line in answer.splitlines():
        if line.startswith("Loại:"):
            loai = line.replace("Loại:", "").strip()
        if line.startswith("Ghi chú:"):
            note = line.replace("Ghi chú:", "").strip()

    if not loai:
        return {"is_relevant": False}

    return {"is_relevant": True, "type": loai, "note": note}
