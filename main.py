import datetime

import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

founding_date = datetime.datetime(1920, 1, 1)
this_year = datetime.datetime.now()
earlier_datetime = this_year.year - founding_date.year


def generate_correct_inclination(number):
    if number % 10 == 1 and number % 100 != 11:
        return "год"
    elif number % 10 in [2, 3, 4] and number % 100 not in [12, 13, 14]:
        return "года"
    else:
        return "лет"




excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', usecols=['Категория','Название', 'Цена', 'Картинка','Акция'],na_values=['N/A', 'NA'], keep_default_na=False)


grouped_wine = defaultdict(list)
for index, row in excel_data_df.iterrows():
    wine_info = {
        'Категория': row["Категория"],
        'Название': row['Название'],
        'Цена': row['Цена'],
        'Картинка': row['Картинка'],
        'Акция': row['Акция']
    }
    grouped_wine[row['Категория']].append(wine_info)

grouped_wine_dict = dict(grouped_wine)
print(grouped_wine_dict)
rendered_page = template.render(grouped_wine=grouped_wine_dict,
                                age_winery=f"Уже {earlier_datetime} {generate_correct_inclination(earlier_datetime)} c вами",)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
