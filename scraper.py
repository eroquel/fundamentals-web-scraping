import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_ARTICLE = '//text-fill[not(class="headline")]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]//text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('\n', '')
                title = title.replace('   ', '')
                # con esto lo que hacemos es que si el titulo tiene comillas "" las elimine.
                summary = parsed.xpath(XPATH_SUMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'data/{today}/{title}.txt', 'w', encoding='utf-8') as f:
                # with es un manejador contextual de Python, que ayuda en caso de que surja un error, el archivo no se corrompa.
                # crea un archivo en la carpeta llamada "today", es decir la fecha, y dentro estarán los archivos ".txt" con el nombre del artículo "title".
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        # Esto almacenará en **response** el documento HTML y todo lo que involucra HTTP incluyendo las cabeceras de este
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            # response.content devuelve el documento HTML de la respuesta y decode('utf-8') ayuda a Python a entender todos los caracteres especiasles como las ñ.

            parsed = html.fromstring(home)
            # Toma el contenido HTML almacenado en *home* en forma de texto y lo transforma en un documento especial en el que puedo usar XPATH.

            link_to_notices = parsed.xpath(XPATH_LINK_ARTICLE)
            # almacena en *link_to_notices* todos los links

            # print(link_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            # el Modulo "datetime" nos ayuda a trabajar con fechas, la función "date" no trae una fecha y "today()" nos trae la fecha acutal. todo esto devuel un objeto,
            # pero en este caso lo que quiero es un estring con la fecha y para esto uso ".strftime('%d-%m-%Y')" y guardamos todo en la variable  "today".

            if not os.path.isdir(today):
                os.mkdir(f'data/{today}')
            # Este if es para verificar si extiste en el mismo directorio de donde se ejecuta el escript una carpeta con el nombre de la fecha de hoy "today" y si no existe,
            # se creará la carpeta.

            for link in link_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
            # Esto es lo que lanzará el estado cuando el status code sea diferente a 200. esto es un Error personalizado.
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
