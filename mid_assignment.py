import pandas as pd
import requests
import os
def collect_data(api_key,year):
    """
    연도를 입력으로 받아서, 매년 1월에서 12월까지 해당 API의 데이터를 가져오는 함수임
    """
    for month in range(1,13):
        month= f'{month:02}'
        url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/energyUseDataSummaryInfo/1/5/{year}/{month}"
        """
        파라미터를 url 파라미터로 넣는게 아닌 듯...에러 응답이 돌아와서 주석처리함
        url = f"http://openapi.seoul.go.kr:8088/"
        params = {
            'KEY': api_key,
            'TYPE': 'json',
            'SERVICE': 'energyUseDataSummaryInfo',
            'START_INDEX': '1',
            'END_INDEX': '5',
            'YEAR':year,
            'MONTH':month
        }
        response = requests.get(url,params=params)
        """
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()
            except "JSONDecodeError":
                print("응답이 JSON 데이터가 맞나요?\n디버깅용으로 응답 첫 100글자를 출력합니다.")
                print(response.text()[0:100])
                return None
        else:
            print(f"요청 실패. 상태코드:{response.status_code}\n자세한 내용은 https://http.cat/{response.status_code}를 참조해주세요.")
            #-i에서 디버깅할 목적으로 response를 반환함.
            print(response.url)
            return None
    ## 데이터 수집
if __name__== "__main__":
    #우선 저장해 둔 api 키를 불러온다. 만약 파일이 없으면 명령줄로 받아들임
    api_file = ".key"
    if api_file in os.listdir(os.getcwd()):
        with open(api_file, 'r') as f:
            api_key = f.read()
    else:
        api_key = input("API키를 붙여넣으세요.")
    start_year = 2015
    end_year = 2024
    for year in range(start_year, end_year+1):
        response = collect_data(api_key,year)
