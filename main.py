import requests
from bs4 import BeautifulSoup
import sys
from fastapi import FastAPI

app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/luka")
async def root():

    with requests.Session() as s:
        headers = {
    'authority': 'sei.tjdft.jus.br',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'pt-BR,pt;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PHPSESSID=6agca27e0gcrf5brbu4b73hev1; cf64d0a6bc5588ae104b92e0cd41237f=7b6d90251b9641aaa817817660b6f6dc',
    'origin': 'https://sei.tjdft.jus.br',
    'referer': 'https://sei.tjdft.jus.br/sip/login.php?sigla_orgao_sistema=TJDFT&sigla_sistema=SEI&infra_url=L3NlaS8=',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
}

        data = {
    'txtUsuario': 't315124',
    'pwdSenha': 'Marina25',
    'selOrgao': '0',
    'sbmLogin': 'Acessar',
    'hdnTokenddb5d507b4c1d96d0c71237970ee214c': '',
}
        try:
            pagina_login = 'https://sei.tjdft.jus.br/sip/login.php?sigla_orgao_sistema=TJDFT&sigla_sistema=SEI&infra_url=L3NlaS8='
            r = s.get (pagina_login)
            soup = BeautifulSoup (r.text, 'html.parser')
            token = soup.find (id = 'hdnTokenddb5d507b4c1d96d0c71237970ee214c')['value']
            data['hdnTokenddb5d507b4c1d96d0c71237970ee214c']= token
            pagina2 = s.post (pagina_login, data = data, headers= headers)
            soup = BeautifulSoup (pagina2.text, 'html.parser')
            PA = soup.select ('td:nth-child(3) a')
            RESP = soup.select ('td:nth-child(4)')

            mat_cordenadora = '(t314922)'

            aux = PA
            resultado = []
            for i in aux:
                resultado.append (i.get_text())

            PA_coordenadora= []

            for i in range (0, len(RESP)):
                aux = RESP[i].get_text()
                if aux == mat_cordenadora:
                    PA_coordenadora.append(i)


            resultado_final = []
            for i in range (len(resultado)):
                if i not in PA_coordenadora:
                    resultado_final.append(resultado[i])

            #teste = sys.argv[1]
            #teste = "123,123,123" #teste
            #lsvbaentrada = teste.split(",") # transforma a lista do vba em um vetor


            #lsvbasaida = []
            #for i in resultado_final: #tira todos os PA's da resultado_final ( tds PA's SEI - os que estão com a coordenadora) que já estão cadastrados no acces
            #    if i not in lsvbaentrada:
            #        lsvbasaida.append(i)
            return resultado_final
        except Exception as e:
            return e


