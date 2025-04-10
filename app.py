from pymongo import MongoClient
import base64
import requests
from flask import Flask, render_template, jsonify, request, url_for, redirect
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

app = Flask(__name__)

# 환경 변수에서 MongoDB 연결 정보 가져오기
mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/ds')
client = MongoClient(mongodb_uri)
db = client.ds


# API신청시의 Redirect uri : http://{REDIRECT_URI}?code={CODE}

@app.get('/oauth/callback')
async def login():
    code = request.args.get('code')
    url = "https://bauth.bbaton.com/oauth/token"
    # 환경 변수에서 OAuth 설정 가져오기
    client_id = os.environ.get('OAUTH_CLIENT_ID')
    secret_key = os.environ.get('OAUTH_SECRET_KEY')
    redirect_uri = os.environ.get('OAUTH_REDIRECT_URI')
    d = {"grant_type": "authorization_code", "redirect_uri": redirect_uri, "code": code}
    h = {"Content-Type": "application/x-www-form-urlencoded",
         "Authorization": "Basic %s" % base64.b64encode((client_id + ":" + secret_key).encode("utf-8")).decode("utf-8")}
    res = requests.post(url, headers=h, data=d)
    if res.status_code == 200:
        user_id = get_user_info(res.json()["token_type"], res.json()["access_token"])
        idlists = db.idlist.find({'is': user_id}, {'_id': False})
        if {'is': user_id} in idlists:
            return render_template('aftervote.html')
        else:
            return redirect(url_for('afterlogin', names=user_id))

def get_user_info(token_type, access_token):
    url = "https://bapi.bbaton.com/v2/user/me"
    auth = token_type + " " + access_token
    h = {"Authorization": auth}
    res = requests.get(url, headers=h)
    if res.status_code == 200:
        if res.json()["adult_flag"] == "Y":
            user_id = res.json()["user_id"]
            return str(user_id)
        else:
            return "Under age"
    else:
        return "get_user_info failed"


# HTML 화면 보여주기

@app.route('/')
def home():
    return render_template('loginpage.html',**locals())

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.xhtml',**locals())

@app.route('/robots.txt')
def robots():
    return render_template('robots.html',**locals())

@app.route('/afterlogins')
def afterlogin():
    return render_template('afterlogin.html')


@app.route('/api/likes',methods=['POST'])
def nomorestar():
    name_receiver = request.form['name_givers']
    idlistss = db.idlists.find({'is': name_receiver}, {'_id': False})
    if {'is': name_receiver} in idlistss:
        return jsonify({'msg3': '이미 투표했습니다!'})



@app.route('/aftervotes')
def aftervotes():
    return render_template('aftervote.html')


@app.route('/test-login')
def test_login():
    # 테스트용 가상 사용자 ID
    test_user_id = "test_user_123"
    return redirect(url_for('afterlogin', names=test_user_id))

# 로컬 테스트용 직접 투표 화면으로 이동하는 엔드포인트
@app.route('/direct-vote')
def direct_vote():
    # 테스트용 가상 사용자 ID
    test_user_id = "local_test_user"
    # 이미 투표한 사용자로 등록하지 않음
    return render_template('afterlogin.html', names=test_user_id)

@app.route('/data')
def database():
    return render_template('index3_wiki.html')


@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']
    target_star = db.ds.find_one({'name': name_receive})
    current_like = target_star['like']
    new_like = current_like + 1
    db.ds.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg1': '투표 완료!'})

@app.route('/afterlogins/like', methods=['POST'])
def save_star():
    name_receiver = request.form['name_giver']
    db.idlist.insert_one({'is': name_receiver})
    db.idlists.insert_one({'is': name_receiver})
    return jsonify({'msg2': '감사합니다!'})


@app.route('/api/listup', methods=['GET'])
def vote_stars():

    all_star = list(db.ds.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'all_stars': all_star})


if __name__ == '__main__':
    # 환경 변수에서 디버그 모드 가져오기
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run('0.0.0.0', port=5000, debug=debug_mode)
