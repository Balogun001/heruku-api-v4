from flask import Flask
app = Flask(__name__)
import requests
from scrapy import Selector
from flask import jsonify, request, redirect, url_for, flash
from datetime import datetime
from pytz import timezone
from flask import render_template


month_map = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre',
}

# action_data = {
#     "Marca1":"Marca1",
#     "Medida1":"Medida1",
#     "Precio1":"Precio1",
#     "Link1":"Link1",
#     "Marca2":"Marca2",
#     "Medida2":"Medida2",
#     "Precio2":"Precio2",
#     "Link2":"Link2",
#     "Marca3":"Marca3",
#     "URL":"URL",
#     "Total":"Total",
#     "Count":"Count",
#     "Date":"Date",
#     "Mes":"Mes",
# }


# tag_data = {
#     "CotSolicitada": "CotSolicitada",
#     "CotEnviada": "CotEnviada",
# }


# @app.route('/')
# def home_page():
#     return render_template('index.html', action_data=[k for k in action_data.values()])


# @app.route('/update', methods=['POST'])
# def update():
#     action_data[request.form['key']] = request.form['action']
#     return redirect(url_for('home_page'))


@app.route('/<id>')
def hello_world(id):
    response = requests.get(f'https://seikotires-mx.com/cotizacion_p.php?id_c={id}')
    response = Selector(text=response.text)
    table_data = response.css('.table tbody tr')[1:-1]
    data_list = []
    count = 1
    if not table_data:
        return jsonify({"No Data": {}, "Count": 0})
    for data in table_data:
        row_data = [d.css('a::text').get() for d in  data.css('td')]
        data_list.append({"action": "set_field_value", "field_name": f"Marca1 {count}", "value": row_data[0] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"Medida1 {count}", "value": row_data[1] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"Precio1 {count}", "value": row_data[2] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"Link1 {count}", "value": row_data[3] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"Marca2{count}", "value": int(row_data[5]) or 0})
        data_list.append({"action": "set_field_value", "field_name": f"Medida2 {count}", "value": float(row_data[6]) or 0})
        data_list.append({"action": "set_field_value", "field_name": f"Precio2 {count}", "value": row_data[7] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"Link2 {count}", "value": row_data[8] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"Marca3 {count}", "value": row_data[9] or ""})
        data_list.append({"action": "set_field_value", "field_name": f"URL {count}", "value": row_data[10] or 0})
        data_list.append({"action": "set_field_value", "field_name": f"Total {count}", "value": int(row_data[11]) or 0})
        count += 1
    
    date_format = '%Y-%m-%dT%H:%M:%S.000Z'
    eastern = timezone('Africa/Abidjan')

    loc_dt = datetime.now(eastern)
    required_date= loc_dt.strftime(date_format)


    month_name = loc_dt.strftime("%B")
    month_name = month_map.get(month_name)
    data_list.append({"action": "set_field_value", "field_name": f"Count", "value": count-1})
    data_list.append({"action": "set_field_value", "field_name": f"Date", "value": required_date})
    data_list.append({"action": "set_field_value", "field_name": f"Mes", "value": month_name})
    data_list.append({"action": "remove_tag", "tag_name": "CotSolicitada"})
    data_list.append({"action": "add_tag", "tag_name": "CotEnviada"})
    return jsonify({"content": {"actions": data_list}, "version": "v2"})


if __name__ == '__main__':
   app.run(debug=True)
