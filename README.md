# 블록체인 기반 투표 시스템

## 프로젝트 개요

이 프로젝트는 블록체인 기술을 활용한 공정하고 투명한 투표 시스템을 구현한 웹 애플리케이션입니다. 소셜 로그인(BBaton)을 통해 사용자 인증을 수행하며, 투표 결과는 MongoDB에 저장됩니다.

## 기술 스택

- **백엔드**: Flask (Python)
- **데이터베이스**: MongoDB
- **인증**: BBaton OAuth API
- **프론트엔드**: HTML, CSS, JavaScript, jQuery

## 시작하기

### 환경 설정

1. Python 가상 환경 설정
```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate
# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate
```

2. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

3. MongoDB 설정
   - Docker로 MongoDB 실행
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```

4. .env 파일 설정
```
MONGODB_URI=mongodb://localhost:27017/ds
FLASK_DEBUG=1
OAUTH_CLIENT_ID=your_client_id
OAUTH_SECRET_KEY=your_secret_key
OAUTH_REDIRECT_URI=http://localhost:5000/oauth/callback
```

### 애플리케이션 실행

1. MongoDB 데이터베이스 초기화
```bash
python init_local_db.py
```

2. Flask 애플리케이션 실행
```bash
python app.py
```

3. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 로컬 테스트 안내

### 인증 없이 투표 테스트하기

로컬 개발 환경에서는 블록체인 인증 과정을 건너뛰고 바로 투표 화면으로 이동할 수 있는 추가 엔드포인트를 제공합니다.

1. 다음 URL로 접속하여 인증 없이 바로 투표 화면으로 이동:
```
http://localhost:5000/direct-vote
```

2. 테스트용 가상 사용자 ID(local_test_user)로 투표 페이지에 접근합니다.

3. 정상적으로 투표를 진행하고 결과를 확인할 수 있습니다.

※ 참고: 이 기능은 로컬 개발/테스트 환경에서만 사용하는 것이 좋습니다. 실제 배포 환경에서는 보안을 위해 비활성화하는 것을 권장합니다.

## 데이터베이스 구조

MongoDB 데이터베이스에는 다음과 같은 컬렉션이 있습니다:

1. **ds 컬렉션**: 후보자 정보 및 득표수 관리
   - `name`: 후보자 이름
   - `img_url`: 후보자 이미지 URL
   - `slogan`: 후보자 슬로건
   - `like`: 득표 수

2. **idlist/idlists 컬렉션**: 투표한 사용자 ID 저장 (중복 투표 방지)
   - `is`: 사용자 ID

## 문제 해결

### MongoDB 연결 문제
- MongoDB 컨테이너가 실행 중인지 확인: `docker ps`
- MongoDB에 인증이 필요한 경우 올바른 사용자 이름과 비밀번호 제공

### Python 인터프리터 문제
- VS Code에서 Python 인터프리터 선택: settings.json 파일에 경로 지정
```json
{
    "python.defaultInterpreterPath": "/path/to/venv/bin/python"
}
``` 