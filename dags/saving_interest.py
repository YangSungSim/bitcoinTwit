# 저축 이율 수집 모듈
# 코드 실행에 필요한 모듈 import
# 금융감독원 Openapi 활용 예적금 정보 수집
import pprint
import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import datetime
import psycopg2
from psycopg2 import sql
import re

# 인증키 번호 : 98b67378fb7abacb85f4be584a6cf70c

bucket= "interest"

KEY = '98b67378fb7abacb85f4be584a6cf70c'
url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.xml?auth={}&topFinGrpNo=020000&pageNo=1".format(KEY)
# http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.xml?auth=98b67378fb7abacb85f4be584a6cf70c&topFinGrpNo=020000&pageNo=1

response = requests.get(url).content.decode('euc-kr')
pprint.pprint(response)

# 개별 상품정보를 뜻하는 <proudct> 태그를 달고 있는 데이터 모두 추출: findAll 함수
xml_obj = BeautifulSoup(response, 'html.parser') # html이나 xml 파싱할 때 html.parser(lxml-xml 사용해도 무방)
rows = xml_obj.findAll("product") # <product>에 nested된 데이터 모두 추출
rows # 결과물 확인

def get_product(KEY, FINGROUP, PAGE):
	import requests
	from bs4 import BeautifulSoup
	from lxml import html
	from urllib.request import Request, urlopen
	from urllib.parse import urlencode, quote_plus, unquote

	url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.xml?auth={}&topFinGrpNo={}&pageNo={}".format(KEY, FINGROUP, PAGE)
	response = requests.get(url).content.decode('euc-kr')
    
	# html을 파싱할 때는 html.parser를,
	# xml을 파싱할 때는 lxml-xml을 사용
	xml_obj = BeautifulSoup(response, 'html.parser')
	rows = xml_obj.findAll("product")
	return rows

# API 호출에 필요한 파라미터(필수)
# 금융기관별 코드 list: 데이터 명세 참고
fin_grp_list = [
    '020000' # 은행
    , '030200' # 여신전문
    , '030300' # 저축은행
    , '050000' # 보험회사
    , '060000' # 금융투자
]

# API 호출에 필요한 파라미터(필수)
PAGE = 1 # 조회하고자 하는 페이지 번호(5page로 충분한 듯)

# 수집할 상품 스펙의 태그명 list: 데이터 명세 참고
item_list = [
'dcls_month' # 공시제출월
, 'kor_co_nm' # 금융회사명
, 'fin_prdt_nm' # 금융상품명
, 'join_way' # 가입방법
, 'mtrt_int' # 만기 후 이자율
, 'spcl_cnd' # 우대조건
, 'join_deny' # 가입제한 1:제한X, 2:서민전용, 3:일부제한
, 'join_member' # 가입대상
, 'max_limit' # 최고한도
, 'intr_rate_type_nm' # 저축 금리 유형명
, 'rsrv_type_nm' # 적립유형명
, 'save_tm' # 저축 기간
, 'intr_rate' # 저축금
, 'intr_rate2' # 최고 우대금리
]

# 스크래핑한 데이터를 담을 빈 list 정의
bank_savings_list = list()

# 금융기관별로 상품 정보를 호출한 후 의도한 스펙을 스크래핑하는 for-loop 구문
for grp in fin_grp_list:
	products = get_product(KEY, grp, PAGE)
    
	for p in range(0, len(products)):
		savings_product_list = list()
		for i in item_list:
			try:
				savings_info = products[p].find(i).text # 특정 스펙을 수집하는 중에 어떤 종류든 error 발생시
			except:
				savings_info = "" # 해당 값은 ""로 대체                
			savings_product_list.append(savings_info)
            
		bank_savings_list.append(savings_product_list)


# 위 과정의 결과물은 list이기 때문에 이것을 dataframe으로 변형
# DF로 변형하면서 컬럼명을 국문으로 지정
import pandas as pd
from pandas import DataFrame

bank_savings_df = DataFrame(bank_savings_list, columns=[
'공시제출월'
, '금융회사명' 
, '금융상품명' 
, '가입방법' 
, '만기후이자율' 
, '우대조건'
, '가입제한' # 1:제한X, 2:서민전용, 3:일부제한
, '가입대상'  
, '최고한도'  
, '저축금리유형명'  
, '적립유형명' 
, '저축기간' 
, '저축금리'  
, '최고우대금리' 
])

bank_savings_df.replace('', '-',regex=True, inplace=True)
bank_savings_df.replace(r'\n', ' ',regex=True, inplace=True)
# 모든 특수기호를 제거하는 함수 정의
def remove_special_characters(text):
    return re.sub(r'[^\w\s]', '', text)  # 모든 특수기호 제거

# DataFrame의 각 요소에 함수 적용
bank_savings_df = bank_savings_df.applymap(lambda x: remove_special_characters(x) if isinstance(x, str) else x)

def create_table_to_postgres(host, database, user, password, table_name, data):
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        drop_table_query= """
        DROP TABLE IF EXISTS interest;
        """
        cursor.execute(drop_table_query)
        print("table droped successfully")

        create_table_if_not_exist_query = """
        CREATE TABLE IF NOT EXISTS interest (
            id SERIAL PRIMARY KEY,
            submitpn TEXT NOT NULL,
            banknm TEXT NOT NULL,
            goodnm TEXT NOT NULL,
            wayre TEXT NOT NULL,
            materityinterest TEXT NOT NULL,
            priority TEXT NOT NULL,
            limit_rate TEXT NOT NULL,
            retarget TEXT NOT NULL,
            atmost TEXT NOT NULL,
            interestnm TEXT NOT NULL,
            typesave TEXT NOT NULL,
            period TEXT NOT NULL,
            interestrate TEXT NOT NULL,
            maxinterest TEXT NOT NULL
        );
        """ 
        cursor.execute(create_table_if_not_exist_query)

        print(f"1 table created successfully.")

        insert_query = sql.SQL(
            'INSERT INTO interest (submitpn, banknm, goodnm, wayre, materityinterest, priority, limit_rate, retarget, atmost, interestnm, typesave, period, interestrate, maxinterest) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        ).format(table=sql.Identifier(table_name))

        cursor.execute(insert_query, data[0])
        connection.commit()

    except Exception as error:
        print(f"Error inserting data: {error}")
        if connection:
            connection.rollback()
    
    finally:
        if connection:
            cursor.close()
            connection.close()

create_table_to_postgres('localhost', 'postgres', 'admin', 'postgres', bucket, bank_savings_df.values.tolist())