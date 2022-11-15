import os
import pandas as pd
import numpy as np
import sqlite3


def load_filenames(start: str):
    return [filename for filename in os.listdir('.') if filename.endswith('.csv') and filename.startswith(start)]


def loader():
    if not os.path.exists('../db.sqlite'):
        conn = sqlite3.connect('../db.sqlite')
        cur = conn.cursor()

        query = '''
            create table location
            (
                location_id     integer primary key,
                location_name   text
            );
        '''
        conn.execute(query)

        query = '''
            create table climate_year
            (
                location_id     integer,
                chk_date        text,
                tavg            real,
                tmin            real,
                tmax            real,
                rain_total      real,
                rain_max        real,
                humid_avg       real,
                wind_avg        real,
                light_time      real,
                primary key (location_id, chk_date),
                foreign key (location_id) references location
            );
        '''
        conn.execute(query)

        query = '''
            create table climate_month
            (
                location_id     integer,
                chk_date        text,
                tavg            real,
                tmin            real,
                tmax            real,
                rain_total      real,
                rain_max        real,
                humid_avg       real,
                wind_avg        real,
                wind_max        real,
                light_time      real,
                primary key (location_id, chk_date),
                foreign key (location_id) references location
            );
        '''
        conn.execute(query)

        query = '''
            create table climate_day
            (
                location_id     integer,
                chk_date        text,
                tavg            real,
                tmin            real,
                tmax            real,
                rain            real,
                humid_avg       real,
                wind_avg        real,
                wind_max        real,
                light_time      real,
                primary key (location_id, chk_date),
                foreign key (location_id) references location
            );
        '''
        conn.execute(query)
        conn.commit()

        # 연도 기준
        filenames = load_filenames('OBS_ASOS_ANL')
        climate_year = None
        column_names = ['지점', '지점명', '일시',
                        '평균기온(°C)', '최저기온(°C)', '최고기온(°C)',
                        '합계 강수량(mm)', '일 최다 강수량(mm)', '평균 상대습도(%)',
                        '평균 풍속(m/s)', '일조율(%)']

        location = pd.DataFrame()
        for filename in filenames:
            file = pd.read_csv(filename, encoding='CP949')[column_names]
            location = file[['지점', '지점명']].drop_duplicates().reset_index(drop=True)
            file.drop(columns='지점명', inplace=True)
            if climate_year is None:
                climate_year = file
            else:
                climate_year = pd.concat([climate_year, file])
        climate_year.columns = ['location_id', 'chk_date',
                        'tavg', 'tmin', 'tmax',
                        'rain_total', 'rain_max', 'humid_avg',
                        'wind_avg', 'light_time']
        location.columns = ['location_id', 'location_name']

        for i, row in location.iterrows():
            query = f'''
                insert into location
                values ({row[0]}, '{row[1]}');
            '''
            conn.execute(query)

        for i, row in climate_year.iterrows():
            query = f'''
                insert into climate_year
                values ({row[0]}, '{row[1]}', {', '.join([str(elm) if not np.isnan(elm) else 'null' for elm in row[2:]])});
            '''
            conn.execute(query)
        conn.commit()

        # 월 기준
        filenames = load_filenames('OBS_ASOS_MNH')
        climate_month = None
        column_names = ['지점', '일시',
                        '평균기온(°C)', '최저기온(°C)', '최고기온(°C)',
                        '월합강수량(00~24h만)(mm)', '일최다강수량(mm)', '평균상대습도(%)',
                        '평균풍속(m/s)', '최대풍속(m/s)', '일조율(%)']

        for filename in filenames:
            file = pd.read_csv(filename, encoding='CP949')[column_names]
            if climate_month is None:
                climate_month = file
            else:
                climate_month = pd.concat([climate_month, file])
        climate_month.columns = ['location_id', 'chk_date',
                        'tavg', 'tmin', 'tmax',
                        'rain_total', 'rain_max', 'humid_avg',
                        'wind_avg', 'wind_max', 'light_time']

        for i, row in climate_month.iterrows():
            query = f'''
                insert into climate_month
                values ({row[0]}, '{row[1]}', {', '.join([str(elm) if not np.isnan(elm) else 'null' for elm in row[2:]])});
            '''
            conn.execute(query)
        conn.commit()

        # 일 기준
        filenames = load_filenames('OBS_ASOS_DD')
        climate_day = None
        column_names = ['지점', '일시',
                        '평균기온(°C)', '최저기온(°C)', '최고기온(°C)',
                        '일강수량(mm)', '평균 상대습도(%)',
                        '평균 풍속(m/s)', '최대 풍속(m/s)', '합계 일조시간(hr)']

        for filename in filenames:
            file = pd.read_csv(filename, encoding='CP949')[column_names]
            if climate_day is None:
                climate_day = file
            else:
                climate_day = pd.concat([climate_day, file])
        climate_day.columns = ['location_id', 'chk_date',
                        'tavg', 'tmin', 'tmax',
                        'rain', 'humid_avg',
                        'wind_avg', 'wind_max', 'light_time']

        for i, row in climate_day.drop_duplicates().iterrows():
            query = f'''
                insert into climate_day
                values ({row[0]}, '{row[1]}', {', '.join([str(elm) if not np.isnan(elm) else 'null' for elm in row[2:]])});
            '''
            conn.execute(query)

        conn.commit()
        conn.close()


def main():
    loader()


if __name__ == "__main__":
    main()


