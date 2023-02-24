from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    # URL để truy cập trang web 24h.com.vn
    url = 'https://www.24h.com.vn/du-bao-thoi-tiet-c568.html'
    response = requests.get(url)

    # Sử dụng BeautifulSoup để parse HTML response từ server
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Tìm các bài báo trên trang web
    articles = soup.select('.cate-24h-foot-home-latest-list > .cate-24h-foot-home-latest-list__box > .cate-24h-foot-home-latest-list__ava > a')
    article_list = []

    # Lặp qua các bài báo và lấy thông tin cần thiết
    for article in articles:
        # print(article)
        # Lấy link ảnh
        img_url = article['data-urlimg']

        # Lấy link bài báo
        # article_link = article['href']
        full_link = article['href']

        # Lấy ngày xuất bản
        # date = article.find('span', class_='tgb_date').text.strip()
        response1 = requests.get(full_link)

        soup1 = BeautifulSoup(response1.content, 'html.parser')
        articles1 = soup1.select('.cate-24h-foot-arti-deta-cre-post')
        date = articles1[0].text
        # print(articles1)
        
        # Lấy tiêu đề
        title = article['title']

        # Thêm thông tin của bài báo vào danh sách
        article_list.append({
            'coverImg': img_url,
            'url': full_link,
            'publishAt': date,
            'describe': title
        })

    return jsonify(article_list)

if __name__ == '__main__':
    app.run(debug=True)