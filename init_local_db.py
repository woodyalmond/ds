import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import sys
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 MongoDB 연결 정보 가져오기
mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/ds')
client = MongoClient(mongodb_uri)
db = client.ds

def insert_star():
    print("후보자 데이터를 가져오는 중...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    try:
        data = requests.get('http://localhost:5000/data', headers=headers)
    except requests.exceptions.ConnectionError:
        print("오류: Flask 서버가 실행 중이지 않습니다.")
        print("먼저 다른 터미널에서 'python app.py'를 실행한 후 다시 시도하세요.")
        sys.exit(1)

    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select('body > div')
    
    count = 0
    for tr in trs:
        name_element = tr.select_one('a')
        if not name_element:
            continue
            
        name = name_element.text.strip()

            
        img_element = tr.select_one('img')
        if not img_element:
            continue
            
        img_url = img_element.get('src', '')
        
        p_element = tr.select_one('p')
        if not p_element:
            continue
            
        slogan = p_element.text.strip()
        
        url = name_element.get('href', '')

        doc = {
            'name': name,
            'img_url': img_url,
            'slogan': slogan,
            'url': url,
            'like': 0
        }

        db.ds.insert_one(doc)
        count += 1
        print(f"후보자 추가: {name}")

    return count

def insert_all():
    # 기존 컬렉션 삭제 (있는 경우)
    db.ds.drop()
    db.idlist.drop()
    db.idlists.drop()
    
    print("Flask 서버가 실행 중인지 확인 중...")
    time.sleep(2)  # 서버가 준비될 때까지 잠시 대기
    
    count = insert_star()
    
    print('\n로컬 MongoDB 초기화 완료')
    print(f'총 {count}명의 후보자 데이터가 추가되었습니다.')

if __name__ == "__main__":
    insert_all() 