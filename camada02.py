import json
import glob
import csv

arquivos = glob.glob("bronze/*.json")

dados = []
colunas = set()

for arquivo in arquivos:
    with open(arquivo, "r") as f:
        dado = json.load(f)

    dados.append(dado)


# Ordenar por horário
dados.sort(key=lambda x: x["timestamp"])

# Guarda o ultimo bytes de cada antena
ultimo_bytes = {}


for dado in dados:
    if "id_antena" in dado:
        id_antena = dado["id_antena"]

        if id_antena in ultimo_bytes:
            diferenca = dado["bytes_sent"] - ultimo_bytes[id_antena]

            if diferenca < 0:
                diferenca = 0


            vazao_mbps = (diferenca * 8)/ 60 / 1_000_000

            dado["vazao_mbps"] = round(vazao_mbps,2)

        else:
            dado["vazao_mbps"] = 0


        ultimo_bytes[id_antena] = dado["bytes_sent"]



for dado in dados:

    if "id_antena" in dado:

        if dado["active_connections"] > 40:
            dado["status"] = "Alta densidade"

        elif dado["cpu_use_percent"] > 85:
            dado["status"] = "Gargalo de processamento"

        elif dado["ram_use_gb"] > 12:
            dado["status"] = "OOM"

        else:
            dado["status"] = "Normal"

    else:

        if dado["cpu_use_percent"] > 85:
            dado["status"] = "Gargalo de processamento"

        elif dado["ram_use_gb"] > 12:
            dado["status"] = "OOM"

        else:
            dado["status"] = "Normal"


colunas = set()

for dado in dados:
    colunas.update(dado.keys())

colunas = list(colunas)


# Cria CSV
with open("silver/dados_consolidados.csv", "w", newline="") as arquivo:
    escritor = csv.DictWriter(
        arquivo, 
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in dados:
        escritor.writerow(dado)


print("Dados consolidados com sucesso!")
print(f"Quantidade de arquivos processados: {len(dados)}")

############################################


trafego_por_minuto = {}

for dado in dados:
    minuto = dado["timestamp"][:16]

    if minuto not in trafego_por_minuto:
        trafego_por_minuto[minuto] = {
            "antenas":0,
            "firewall":0
        }


    if "id_antena" in dado:
        trafego_por_minuto[minuto]["antenas"] += int(dado["bytes_sent"])
    else:
        trafego_por_minuto[minuto]["firewall"] += int(dado["bytes_sent"])


with open("silver/consistencia_trafego.csv", "w", newline="") as arquivo:
    colunas = [
        "timestamp",
        "bytes_antenas",
        "bytes_firewall",
        "diferenca_bytes"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for minuto in trafego_por_minuto:
        bytes_antenas = trafego_por_minuto[minuto]["antenas"]
        bytes_firewall = trafego_por_minuto[minuto]["firewall"]

        diferenca = bytes_firewall - bytes_antenas

        escritor.writerow({
            "timestamp": minuto,
            "bytes_antenas": bytes_antenas,
            "bytes_firewall": bytes_firewall,
            "diferenca_bytes": diferenca
        })


print("Análise de consistência de tráfego concluída!")