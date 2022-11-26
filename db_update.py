import shutil
import pandas as pd
from models import *


def load_filenames(start: str, end: str, route: str = '.'):
    return [filename for filename in os.listdir(route) if filename.endswith(end) and filename.startswith(start)]


def db_init():

    if not os.path.exists('db.sqlite'):
        print('db create!')
        db.create_all()
    query = '''
        select count(*)
        from location
    '''
    if db.engine.execute(query).all()[0][0] == 0:
        route = 'climate_data/new'
        filenames = load_filenames('OBS_ASOS_ANL', '.csv', route)
        if len(filenames) == 0:
            route = 'climate_data/old'
            filenames = load_filenames('OBS_ASOS_ANL', '.csv', route)
            if len(filenames) == 0:
                return
        df = pd.read_csv(route + '/' + filenames[0], encoding='CP949')[['지점', '지점명']].drop_duplicates().reset_index(drop=True)
        for i, row in df.iterrows():
            query = f'''
                insert into location
                values ({row[0]}, '{row[1]}');
            '''
            db.engine.execute(query)
    db.session.commit()
    db_update()


def db_update():
    from_route = 'climate_data/new'
    to_route = 'climate_data/old'
    filenames = load_filenames('OBS_ASOS_', '.csv', from_route)
    # filenames = ['OBS_ASOS_ANL_20221115205709.csv']
    if len(filenames) > 0:
        for filename in filenames:
            if file_to_db(from_route, filename):
                shutil.move(from_route + '/' + filename, to_route)
                print('import:', filename, 'done!')
            else:
                continue
    print('update done!')


def file_to_db(route: str, filename: str) -> bool:
    if filename.startswith('OBS_ASOS_ANL'):
        datetype = 'year'
        column_names = ['지점', '일시',
                        '평균기온(°C)', '최저기온(°C)', '최고기온(°C)',
                        '합계 강수량(mm)', '일 최다 강수량(mm)', '평균 상대습도(%)',
                        '평균 풍속(m/s)', '일조율(%)']
    elif filename.startswith('OBS_ASOS_MNH'):
        datetype = 'month'
        column_names = ['지점', '일시',
                        '평균기온(°C)', '최저기온(°C)', '최고기온(°C)',
                        '월합강수량(00~24h만)(mm)', '일최다강수량(mm)', '평균상대습도(%)',
                        '평균풍속(m/s)', '최대풍속(m/s)', '일조율(%)']
    elif filename.startswith('OBS_ASOS_DD'):
        datetype = 'day'
        column_names = ['지점', '일시',
                        '평균기온(°C)', '최저기온(°C)', '최고기온(°C)',
                        '일강수량(mm)', '평균 상대습도(%)',
                        '평균 풍속(m/s)', '최대 풍속(m/s)', '합계 일조시간(hr)']
    else:
        return False

    try:
        df = pd.read_csv(route + '/' + filename, encoding='CP949')[column_names]
    except FileNotFoundError:
        return False

    df = df.loc[df[['지점', '일시']].dropna().index]

    for i, row in df.iterrows():
        query = f'''
            insert or ignore into climate_{datetype}
            values ({int(row[0])}, '{str(row[1]).split('.')[0]}', {', '.join([str(elm) if str(elm) != 'nan' else 'null' for elm in row[2:]])});
        '''
        db.engine.execute(query)

    db.session.commit()
    return True
