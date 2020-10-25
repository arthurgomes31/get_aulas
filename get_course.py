import os
import urllib.request
import unicodedata
import socket
import sys
import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

socket.setdefaulttimeout(60)


def removercaractespeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavran = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    ajuste = re.sub('[^a-zA-Z0-9 \\\]', '', palavran)
    return str(ajuste)


destination_file = sys.path[0]

prefs = {'profile.default_content_setting_values.automatic_downloads': 1,
         "download.prompt_for_download": False,
         "download.default_directory": destination_file,
         "download.directory_upgrade": True,
         "safebrowsing.enabled": True
         }

mobile_emulation = {
    "deviceMetrics": {"width": 320, "height": 500},
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"}

options = Options()
options.add_experimental_option("prefs", prefs)
options.add_argument("user-data-dir=C:/Users/arthur.gomes.d.silva/AppData/Local/Google/Chrome/User Data")
# options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)

lista_cursos = ['https://cursos.alura.com.br/course/unity-2d-criando-jogo-multiplayer',
                'https://cursos.alura.com.br/course/trabalhando-unity-mobile',
                'https://cursos.alura.com.br/course/unity-mobile-interface-responsiva-desempenho',
                'https://cursos.alura.com.br/course/unity-mobile-aprofundando-jogos'
                'https://cursos.alura.com.br/course/shellscripting',
                'https://cursos.alura.com.br/course/shellscripting-parte-2',
                'https://cursos.alura.com.br/course/git-github-branching-conflitos-pull-requests',
                'https://cursos.alura.com.br/course/git-github-controle-de-versao',
                'https://cursos.alura.com.br/course/javascript-introducao',
                'https://cursos.alura.com.br/course/javascritpt-orientacao-objetos',
                'https://cursos.alura.com.br/course/javascript-polimorfismo',
                'https://cursos.alura.com.br/course/api-rest-javascript',
                'https://cursos.alura.com.br/course/spa-javascript-puro',
                'https://cursos.alura.com.br/course/react-js',
                'https://cursos.alura.com.br/course/react-ciclo-de-vida',
                'https://cursos.alura.com.br/course/react-function-components',
                'https://cursos.alura.com.br/course/react-hooks-e-formularios',
                'https://cursos.alura.com.br/course/svg-css-animacao']

for curso in lista_cursos:

    driver.get(curso)
    time.sleep(3)
    lista_urls = re.findall(string=driver.page_source, pattern='href="(/course.+/tasks)"')

    for link in lista_urls:

        driver.get(url=f'https://cursos.alura.com.br{link}')
        time.sleep(3)
        lista_aulas = re.findall(string=driver.page_source, pattern='href="(/course.+/task/[0-9]+)')
        lista_aulas = set(lista_aulas)
        for aula in lista_aulas:
            try:
                aula = 'https://cursos.alura.com.br' + aula.split('\n')[0]
                driver.get(aula)
                time.sleep(3)
                title = removercaractespeciais(driver.title)
                title = title.replace(' ', '_')
                url_video = re.findall(string=driver.page_source, pattern='https://video.+[0-9]')[0]
                url_video = url_video.replace('amp;', '')
                driver.get(url_video)
                time.sleep(3)
                urllib.request.urlretrieve(url_video, f'{title}.mp4')
                tentativa = 0
                while tentativa < 10:
                    if f'{title}.mp4' in os.listdir(sys.path[0]):
                        print(f'Arquivo Baixado {title}')
                        break
                    print('Aguardando Download')
                    tentativa += 1
                    time.sleep(1)

                
            except Exception as erro:
                erro_geral = {'Motivo do erro': erro,
                              'Na Aula': aula,
                              'Title': title,
                              'Dt Execução': datetime.datetime.today()
                              }
                print(erro_geral)

print('Finalizado')
driver.close()
