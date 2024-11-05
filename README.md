# bitcoinTwit


![image](https://github.com/YangSungSim/bitcoinTwit/assets/49933934/c3a63fae-e6e2-46aa-8fa9-22e1e16677a3)

![image](https://github.com/YangSungSim/bitcoinTwit/assets/49933934/b2059654-b0b5-454c-b922-4bbdfa3c58bf)

![image](https://github.com/YangSungSim/bitcoinTwit/assets/49933934/701de001-1a16-43ef-b373-0314b0a37b69)

# 텍스트 데이터 및 기술, 가치 평가 베이스 종합 포트폴리오 트레이딩 플랫폼
## 대상: [은행금리, 채권, p2p, 부동산, 주식, 코인]

## 1. 은행금리: 15일
## 2. 채권: 15일(한국 채권, 미국 채권)
## 3. p2p: 일주일
## 4. 부동산: 3일
## 5. 주식: 매일(미국 지수, 한국 지수, ETF)
## 6. 코인: 실시간

## 저장일자: 2년

# [preprocess]
# DB:influxDB 시계열 데이터 저장 데이터 베이스
# grafana: influxDB 에 쿼리 날릴 때 사용하거나 몽고디비 두루 살펴보는 대시보드
# kafka: 실시간 시계열 데이터 정제 후 저장
# zookeepter: kafka 사용시 필요한 스택
# elastic-search: text data search 할 때 사용할 스택


# django
## 트레이딩 거래 플랫폼
## 포트 폴리오 대시보드(이거 먼저)
## redis: 임시 비밀번호, 로그인세션, JWT 등

# react
## 웹화면 및 포트폴리오 대시보드

## 추후 사용할 기술 스택
### - crawling: 이건 그냥 코드만들어서 계속 돌리기. 실시간 용
### - mongoDb: 기사 데이터 정제 후 저장(2차 정제 과정 필요)
  
# [preprocess]
# airflow: 
### id: airflow password: airflow
### - 일정기간 이전의 데이터 삭제 용으로 사용(일배치 사용)
### - 주마다 포트폴리오 재 갱신할 배치용으로 사용.
### - pandas 랑 numpy로 기업가치 재계산 혹은 머신러닝 분석(감성분석) 일 배치로 사용.
### - spark, crawling: 매일 기사 데이터 오전 8시 와 오후 5시 수집 후 정제 처리 후 저장
### - spark: 시계열 데이터 기간 별 rolling 후 저장 시 사용.(짧은 시간(거의 실시간) ETL)
### - 매일의 은행 이율, 해외 지수, 채권 이율, 종합주가지수, p2p, 부동산 펀드 등 데이터 저장.

# web cicd- git cicd heroku 



# [mongodb]
## docker compose 사용시 유의점:
### 다시 올릴 때는 /mongo-data 하단의 데이터를 다 지우고 실행한다.
### docker compose에 비번은 설정 안하는 게 낫다. 어차피 mongosh 후에 createuser를 해줘야 하기 때문에
### createUser 코드는 그냥 구글 검색해서 create 해주면 된다.
### 해주면 안돌아가는 mongo-express를 다시 run 해주면 잘 돌아간다.
#### mongosh -u root -p password --authenticationDatabase admin
db.createUser({
  user: 'root',
  pwd: 'password',
  roles: [
    { role: 'userAdminAnyDatabase', db: 'admin' },
    { role: 'readWriteAnyDatabase', db: 'admin' },
  ],
});

#### basicAuth credentials are "admin:pass", it is recommended you change this in your config.js!
#### mongo express 처음로그인시 id: admin password: pass로 로그인해야 한다.
#### create database와 create Collection 해준다.
#### 그러면 파이썬 코드가 잘 돌아간다. 

<!-- >>> client = MongoClient('mongodb://root:password@localhost:27017/')                              
>>> db = client['news_database']
>>> news_post = db['newsdb']
>>> post = {
...   "date": 1
... }
>>> news_post.insert_one(post)
InsertOneResult(ObjectId('66619b0cbae93c4dc1663308'), acknowledged=True) -->



### airflow docker compose 파일 출처
#### https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


### airflow 초기 user 생성 방법
##### airflow users create -u admin -p admin -f Clueless -l Coder -r Admin -e admin@admin.com 