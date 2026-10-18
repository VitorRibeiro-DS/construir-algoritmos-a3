
import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

# 1. Autenticação
load_dotenv(".env")

url = "https://api.olhovivo.sptrans.com.br/v2.1"
s = requests.Session()

res = s.post(
    f"{url}/Login/Autenticar",
    params={"token": os.getenv("SPTRANS_TOKEN")}
)

if res.json() != True:
    raise ValueError("Erro na autenticação")

print("Autenticado com sucesso!")

# 2. Buscar linha
res = s.get(
    f"{url}/Linha/Buscar?termosBusca=118Y"
)

linhas = res.json()

if not linhas:
    raise ValueError("Linha não encontrada")

codigo = linhas[0]["cl"]

print("Código da linha:", codigo)

# 3. Buscar paradas
res = s.get(
    f"{url}/Parada/BuscarParadasPorLinha?codigoLinha={codigo}"
)

paradas = res.json()

print("Paradas encontradas:", len(paradas))

# 4. Buscar posições dos ônibus
res = s.get(
    f"{url}/Posicao/Linha?codigoLinha={codigo}"
)

posicoes = res.json()
onibus = posicoes["vs"]

print("Ônibus encontrados:", len(onibus))

# 5. Criar o mapa
if paradas:
    centro = paradas[0]
elif onibus:
    centro = onibus[0]
else:
    raise ValueError("Nenhuma parada ou ônibus encontrado")

m = Map(
    location=[centro["py"], centro["px"]],
    zoom_start=13,
    tiles="OpenStreetMap"
)

# Pins azuis para as paradas
for i in paradas:
    Marker(
        location=[i["py"], i["px"]],
        popup=i["np"],
        icon=Icon(color="blue")
    ).add_to(m)

# Pins vermelhos para os ônibus
for i in onibus:
    Marker(
        location=[i["py"], i["px"]],
        popup=f"Ônibus: {i['p']}",
        icon=Icon(color="red")
    ).add_to(m)

# 6. Salvar e abrir o mapa
m.save("mapa_onibus.html")
m.show_in_browser()

print("Mapa criado com sucesso!")

s.close()