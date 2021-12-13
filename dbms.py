import sqlite3
import pandas as pd
import os

DB_FILEPATH = './weather.db'

CSV_FILEPATH = os.path.join(os.path.dirname(__file__), '2011_2021.csv')

def engineer2(df):
  df = df.copy()
  df['일시'] = pd.to_datetime(df['일시'])
  df['월'] = 0
  df.set_index('지점', inplace=True)
  df.reset_index(inplace=True)
  for i in df.index:
    df['월'].iloc[i] = df['일시'].iloc[i].month

  df['우산 필요'] = 0
  umb_index = df[df['일강수량(mm)']>=10].index
  df['우산 필요'].iloc[umb_index] = 1
  df.drop('일강수량(mm)', axis=1, inplace=True)


  return df


def init_database(DB_FILEPATH):

    df = pd.read_csv(CSV_FILEPATH, encoding='cp949')
    drop_feature = ['합계 일조시간(hr)',	'합계 일사량(MJ/m2)','평균 5cm 지중온도(°C)',	'평균 10cm 지중온도(°C)',	'평균 20cm 지중온도(°C)',	'평균 30cm 지중온도(°C)',	'0.5m 지중온도(°C)',	'1.0m 지중온도(°C)',	'1.5m 지중온도(°C)',	'3.0m 지중온도(°C)',	'5.0m 지중온도(°C)',
                '합계 대형증발량(mm)',	'합계 소형증발량(mm)',	'안개 계속시간(hr)', '최소 상대습도 시각(hhmi)', '최고 해면기압 시각(hhmi)', '최저 해면기압 시각(hhmi)', '1시간 최다일사 시각(hhmi)', '1시간 최다일사량(MJ/m2)','최대 풍속 시각(hhmi)',
                '최대 순간풍속 시각(hhmi)','최고기온 시각(hhmi)','최저기온 시각(hhmi)', '강수 계속시간(hr)',	'10분 최다 강수량(mm)',	'10분 최다강수량 시각(hhmi)',	'1시간 최다강수량(mm)',	'일 최심신적설(cm)', '일 최심적설(cm)','합계 3시간 신적설(cm)','1시간 최다 강수량 시각(hhmi)',
                '일 최심신적설 시각(hhmi)',	'일 최심적설 시각(hhmi)','9-9강수(mm)', '기사','풍정합(100m)','최다풍향(16방위)', '평균 증기압(hPa)', '가조시간(hr)',	'평균 전운량(1/10)',	'평균 중하층운량(1/10)',	'평균 지면온도(°C)',	'최저 초상온도(°C)',
                '최대 순간 풍속 풍향(16방위)','최대 풍속 풍향(16방위)']
    df = df.drop(drop_feature, axis=1)
    drop_index = df[df['일강수량(mm)'].isnull()].index
    df  = df.drop(index=drop_index)
    df = engineer2(df)

    num = pd.unique(df['지점'])
    name = pd.unique(df['지점명'])
    temp = {}
    for n1, n2 in zip(name, num):
        temp[n1] = n2
    df = df.drop(['지점명',	'일시'], axis=1)
    conn = sqlite3.connect(DB_FILEPATH)
    df.to_sql('weather.db', conn, if_exists='replace', index=False)
    conn.close()

    df.drop('우산 필요', axis=1, inplace=True)

    return df.mean(), temp



def pipe(json_data, DB_FILEPATH):
    conn = sqlite3.connect(DB_FILEPATH)
    cur = conn.cursor()
    for data in json_data:
        cur.execute(f"INSERT OR IGNORE INTO User VALUES('{data['user']['id']}','{data['user']['login']}','{data['user']['node_id']}');")


    conn.commit()

    cur.close()
    conn.close()
