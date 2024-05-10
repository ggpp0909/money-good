# 가상환경 생성
```bash
python -m venv venv
```
- git ignore로 venv는 깃에 안올리게 해뒀으니 반드시 로컬에 직접 설치하기

## 가상환경 활성화
macOS 및 Linux:

```bash
source venv/bin/activate
```

Windows:
```bash
source venv/Scripts/activate
```

## 가상환경 비활성화
```bash
deactivate
```

## 라이브러리 requirments에 저장
```bash
pip freeze > requirements.txt
```

## requirments로부터 install
```bash
pip install -r 파일이름.txt
```

# 가상환경 개발 프로세스
1. 개발 시작 전 가상환경 활성화.
2. 라이브러리 다운시 requiments에 저장
3. 개발 후 가상환경 비활성화
4. 나중에 pull 받고 requirments로부터 install