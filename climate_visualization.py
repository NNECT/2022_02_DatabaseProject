from flask import Flask, render_template, escape, request, redirect, url_for
from flask_cors import cross_origin
from datetime import datetime
from db_update import db_init
from db_load import db_load
from models import *


@app.route("/")
def page_main():
    db_init()
    return render_template('index.html')


@app.route("/table")
@app.route("/table", methods=['POST'])
@cross_origin(origins='*')
def table():
    if request.method == 'POST':
        loc = request.form.getlist('loc')
        datetype = request.form.get('datetype')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        if datetype == 'year':
            data = request.form.getlist('dataYear')
        elif datetype == 'month':
            data = request.form.getlist('dataMonth')
        elif datetype == 'day':
            data = request.form.getlist('dataDay')
        else:
            print('datetype error')
            return redirect(url_for('page_main'))
    else:
        return render_template('s_table.html')

    loc = [int(elm) for elm in loc]
    data = ['location_name', 'chk_date'] + data
    df = db_load(data, loc, datetype, datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d"))

    columns = df.columns
    rows = df.reset_index().values.tolist()

    return render_template('table.html', columns=columns, rows=rows)


@app.route("/graph", methods=['GET', 'POST'])
@cross_origin(origins='*')
def graph():
    if request.method == 'GET':
        print('get method')
        loc = request.args.get('loc')
        if loc == '1' or loc == 1:
            return render_template('s_graph.html')
        elif loc == '0' or loc == 0:
            return render_template('v_graph.html')
        else:
            print('get method error')
            return redirect(url_for('page_main'))
    elif request.method == 'POST':
        print('post method')

        graphtype = request.form.get('graphtype')
        datetype = request.form.get('datetype')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')

        if graphtype == '1' or graphtype == 1:
            loc = request.form.get('loc')
            if datetype == 'year':
                data = request.form.getlist('dataYear')
            elif datetype == 'month':
                data = request.form.getlist('dataMonth')
            elif datetype == 'day':
                data = request.form.getlist('dataDay')
            else:
                print('datetype error')
                return redirect(url_for('page_main'))
        elif graphtype == '0' or graphtype == 0:
            loc = request.form.getlist('loc')
            if datetype == 'year':
                data = request.form.get('dataYear')
            elif datetype == 'month':
                data = request.form.get('dataMonth')
            elif datetype == 'day':
                data = request.form.get('dataDay')
            else:
                print('datetype error')
                return redirect(url_for('page_main'))
        else:
            print('post graphtype error')
            return redirect(url_for('page_main'))

    else:
        print('method error')
        return redirect(url_for('page_main'))

    if graphtype == '1' or graphtype == 1:
        data = ['location_name', 'chk_date'] + data
        df = db_load(data, int(loc), datetype,
                     datetime.strptime(start_date, "%Y-%m-%d"),
                     datetime.strptime(end_date, "%Y-%m-%d"))
        df_dict = df.iloc[:, 2:].to_dict('list')
        data = []
        for key in df_dict:
            data.append(
                {
                    'label': key,
                    'data': df_dict[key],
                    'borderWidth': 2
                }
            )
        return render_template('graph.html', date=list(df.iloc[:, 1]), df=data)

    elif graphtype == '0' or graphtype == 0:
        loc = [int(elm) for elm in loc]
        loc_names = []
        for loc_id in loc:
            query = f'''
                select location_name
                from location
                where location_id = {loc_id}
            '''
            loc_names.append(db.engine.execute(query).one()[0])
        if len(loc) != len(loc_names) or len(loc) == 0:
            print('location name error')
            return redirect(url_for('page_main'))

        data = ['chk_date'] + [data]
        df_dict = {loc_name: None for loc_name in loc_names}
        for loc_name, loc_id in zip(loc_names, loc):
            df = db_load(data, loc_id, datetype,
                         datetime.strptime(start_date, "%Y-%m-%d"),
                         datetime.strptime(end_date, "%Y-%m-%d"))
            df_dict[loc_name] = df.iloc[:, 1].values.tolist()

        data = []
        for key in df_dict:
            data.append(
                {
                    'label': key,
                    'data': df_dict[key],
                    'borderWidth': 2
                }
            )

        return render_template('graph.html', date=list(df.iloc[:, 0]), df=data)

    else:
        print('post graphtype error')
        return redirect(url_for('page_main'))


def main():
    app.run(port=5000)
    # app.run(debug=True)
    # app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
