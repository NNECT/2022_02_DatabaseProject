from __future__ import annotations
import pandas as pd
from datetime import datetime
from models import *


def db_load(select: list, location: list | int | str = None, datetype: int | str = None, start_date: str | datetime = None, end_date: str | datetime = None):
    '''
    데이터베이스에서 데이터를 불러오는 함수
    데이터프레임의 형식으로 반환

    :param select: <리스트> 반환할 데이터의 종류
    :param location: <리스트/숫자/문자열> 반환할 데이터 지역. 기본적으로 location_id의 리스트를 입력해야 하지만, 문자열로 입력해도 자동으로 변환됨.
    :param datetype: <숫자/문자열> 반환할 데이터의 날짜 단위. 연간/월간/일간.
    :param start_date: <문자열/datetime> 반환할 데이터의 시작 날짜.
    :param end_date: <문자열/datetime> 반환할 데이터의 종료 날짜.
    :return:
    '''

    if location is None:
        query = f'''
            select distinct location_id
            from location
        '''
        location = db.engine.execute(query).all()
        for i, elm in enumerate(location):
            location[i] = elm[0]
    elif type(location) == int:
        location = [location]
    elif type(location) == str:
        query = f'''
            select location_id
            from location
            where location_name = '{location}'
        '''
        location = [db.engine.execute(query).one()[0]]
    else:
        for i, elm in enumerate(location):
            if type(elm) == str:
                query = f'''
                    select location_id
                    from location
                    where location_name = '{location}'
                '''
                location[i] = db.engine.execute(query).one()[0]

    if datetype is None:
        if start_date is None:
            print('날짜 형태 확인 안 됨')
            return None
        if type(start_date) == str:
            if len(start_date) > 7:
                datetype = 'day'
            elif len(start_date) > 4:
                datetype = 'month'
            else:
                datetype = 'year'
        else:
            datetype = 'day'

    if datetype == 'year':
        datestr = '%Y'
        column_str = {
            "location_name": "지역",
            "chk_date": "일시",
            "tavg": "평균기온",
            "tmin": "최저기온",
            "tmax": "최고기온",
            "rain_total": "총강수량",
            "rain_max": "일최다강수량",
            "humid_avg": "평균상대습도",
            "wind_avg": "평균풍속",
            "light_time": "일조율",
        }
    elif datetype == 'month':
        datestr = '%Y-%m'
        column_str = {
            "location_name": "지역",
            "chk_date": "일시",
            "tavg": "평균기온",
            "tmin": "최저기온",
            "tmax": "최대기온",
            "rain_total": "총강수량",
            "rain_max": "일최다강수량",
            "humid_avg": "평균상대습도",
            "wind_avg": "평균풍속",
            "wind_max": "최대풍속",
            "light_time": "일조율",
        }
    elif datetype == 'day':
        datestr = '%Y-%m-%d'
        column_str = {
            "location_name": "지역",
            "chk_date": "일시",
            "tavg": "평균기온",
            "tmin": "최저기온",
            "tmax": "최대기온",
            "rain": "일강수량",
            "humid_avg": "평균습도",
            "wind_avg": "평균풍속",
            "wind_max": "최대풍속",
            "light_time": "일조시간",
        }
    else:
        print('날짜 형태 확인 안 됨')
        return

    if start_date is None:
        start_date = datetime.today()
    elif type(start_date) == str:
        start_date = datetime.strptime(start_date, datestr)
    if end_date is None:
        end_date = datetime.today()
    elif type(end_date) == str:
        end_date = datetime.strptime(end_date, datestr)

    query = f'''
        select {', '.join([col for col in select])}
        from climate_{datetype} natural join location
                where ({' or '.join([f'location_id = {elm}' for elm in location])})
                    and chk_date >= '{start_date.strftime(datestr)}' and chk_date <= '{end_date.strftime(datestr)}';
    '''
    data = pd.DataFrame(db.engine.execute(query).all(), columns=[column_str[col] for col in select])
    print('load done!')
    return data

