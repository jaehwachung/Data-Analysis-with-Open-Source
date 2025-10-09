import json
import os

import pandas as pd
import requests


def collect_data(api_key,year):
    """
    연도를 입력으로 받아서, 매년 1월에서 12월까지 해당 API의 데이터를 가져오는 함수임
    """
    monthly_list = []
    for month in range(1,13):
        month= f'{month:02}'
        #API 페이지에서 0으로 패딩할 것을 명시하고 있음
        url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/energyUseDataSummaryInfo/1/5/{year}/{month}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            returned_json = response.json()
            #try:
            #왠지 모르겠는데, 한번씩 키에 "User" 대신 Use가 들어가  있음...
            #반환된 딕셔너리에 키가 하나 뿐이니 그냥 딕셔너리의 첫번째 값을 쓰자 
            returned_json = list(response.json().values())[0]
            with open("result.txt",'a',encoding='utf-8') as k:
                for each in range(len(returned_json)):
                    if "개인" not in returned_json['row'][each].values():
                        k.write(returned_json['row'][each]['MM_TYPE'])
                        print(returned_json['row'][each])
                    #k.write(str(response.json()))
            if returned_json['RESULT']['CODE']== "INFO-000":
                #print(returned_json['row']['MM_TYPE'])
                monthly_list += [row for row in returned_json['row'] if row['MM_TYPE']=="개인"]
            else:
                print("서버가 응답은 했는데, 오류를 반환했어요..." )
            #except KeyError as e:
            #    #print(returned_json)
            #    with open("result.txt",'w',encoding='utf-8') as k:
            #        k.write(str(response.json()))
            #    #print(f"{year}.{month}.")
            #    #print("응답이 JSON 데이터가 맞나요?\n디버깅용으로 응답 첫 100글자를 출력합니다.")
            #    #print(response.text[0:100])
        else:
            print(f"요청 실패. 상태코드:{response.status_code}\n자세한\
                  내용은 https://http.cat/{response.status_code}를 참조해주세요.")
            #-i에서 디버깅할 목적으로 response를 반환함.
            print(response.url)
            return None
    print(len(monthly_list))
    return monthly_list
    ## 데이터 수집
if __name__== "__main__":
    #우선 저장해 둔 api 키를 불러온다. 만약 파일이 없으면 명령줄로 받아들임
    api_file = ".key"
    if api_file in os.listdir(os.getcwd()):
        with open(api_file, 'r', encoding='utf-8') as f:
            api_key = f.read()
    else:
        api_key = input("API키를 붙여넣으세요.")
    start_year = 2015
    end_year = 2024
    merged_result=[]
    for year in range(start_year, end_year+1):
        #print(type(collect_data(api_key,year)))
        result=collect_data(api_key,year)
        print(len(result))
        merged_result+= result
    print(len(merged_result))