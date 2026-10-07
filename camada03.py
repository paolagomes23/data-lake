import csv

with open("silver/dados_consolidados.csv","r") as arquivo:
    leitor = csv.DictReader(arquivo)
    dados = list(leitor)


# ZONAS MORTAS ################################################

antenas = {}

for dado in dados:
    if dado["id_antena"] != "":
        id_antena = dado["id_antena"]
        vazao = float(dado["vazao_mbps"])


        if id_antena not in antenas:
            antenas[id_antena] = []

        antenas[id_antena].append(vazao)



resultado = []

for id_antena in antenas:
    vazoes = antenas[id_antena]
    media = sum(vazoes)/len(vazoes)

    resultado.append({
        "id_antena": id_antena,
        "vazao_media_mbps":round(media,2)
    })


resultado.sort(key=lambda x: x["vazao_media_mbps"])

with open("gold/zonas_mortas.csv", "w", newline="") as arquivo:
    colunas = [
        "id_antena",
        "vazao_media_mbps"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in resultado:
        escritor.writerow(dado)

print("Análise de zonas mortas concluída!")

#  RANKING DE EFICIÊNCIA  ###################################################

eficiencia = {}

for dado in dados:
    if dado["id_antena"] != "":
        id_antena = dado["id_antena"]
        vazao = float(dado["vazao_mbps"])
        cpu = float(dado["cpu_use_percent"])

        if id_antena not in eficiencia:
            eficiencia[id_antena] = {
                "vazao_total": 0,
                "cpu_total": 0,
                "quantidade": 0
            }

        eficiencia[id_antena]["vazao_total"] += vazao
        eficiencia[id_antena]["cpu_total"] += cpu
        eficiencia[id_antena]["quantidade"] += 1


resultado_eficiencia = []

for id_antena in eficiencia:
    quantidade = eficiencia[id_antena]["quantidade"]
    vazao_media = (eficiencia[id_antena]["vazao_total"] / quantidade)
    cpu_media = (eficiencia[id_antena]["cpu_total"] / quantidade)


# Eficiencia: maior vazão utilizando menos CPU
    if cpu_media > 0:
        eficiencia_media = vazao_media / cpu_media
    else:
        eficiencia_media = 0



    resultado_eficiencia.append({
        "id_antena": id_antena,
        "vazao_media_mbps": round(vazao_media,2),
        "cpu_media_percent": round(cpu_media,2),
        "eficiencia": round(eficiencia_media,4)
    })


resultado_eficiencia.sort(key=lambda x: x["eficiencia"],reverse=True)

with open("gold/ranking_eficiencia.csv", "w", newline="") as arquivo:
    colunas = [
        "id_antena",
        "vazao_media_mbps",
        "cpu_media_percent",
        "eficiencia"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in resultado_eficiencia:
        escritor.writerow(dado)

print("Ranking de eficiência concluído!")   


#  ANÁLISE DE SEGURANÇA  ##############################################

seguranca = []

for dado in dados:
    if dado["most_blocked_ip"] != "":
        seguranca.append({
            "timestamp": dado["timestamp"],
            "most_blocked_ip": dado["most_blocked_ip"],
            "dropped_packets": int(dado["dropped_packets"]),
            "active_sessions": int(dado["active_sessions"])
        })


seguranca.sort(key=lambda x: x["dropped_packets"], reverse=True)

with open("gold/analise_seguranca.csv", "w", newline="") as arquivo:
    colunas = [
        "timestamp",
        "most_blocked_ip",
        "dropped_packets",
        "active_sessions"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in seguranca:
        escritor.writerow(dado)

print("Análise de segurança concluída!")


#  VISÃO GERAL  #########################################################

total_registros = len(dados)
total_antenas = 0
total_firewall = 0
soma_cpu = 0
soma_ram = 0
soma_conexoes = 0
soma_sessoes = 0

for dado in dados:
    soma_cpu += float(dado["cpu_use_percent"])
    soma_ram += float(dado["ram_use_gb"])


    if dado["id_antena"] != "":
        total_antenas += 1
        soma_conexoes += int(dado["active_connections"])

    else:
        total_firewall += 1
        soma_sessoes += int(dado["active_sessions"])


cpu_media = soma_cpu / total_registros
ram_media = soma_ram / total_registros


if total_antenas > 0:
    conexoes_media = soma_conexoes / total_antenas
else:
    conexoes_media = 0

if total_firewall > 0:
    sessoes_media = soma_sessoes / total_firewall
else:
    sessoes_media = 0



with open("gold/visao_geral.csv", "w", newline="") as arquivo:
    colunas = [
        "total_registros",
        "total_registros_antenas",
        "total_registros_firewall",
        "cpu_media_percent",
        "ram_media_gb",
        "conexoes_media",
        "sessoes_media"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    escritor.writerow({
        "total_registros": total_registros,
        "total_registros_antenas": total_antenas,
        "total_registros_firewall": total_firewall,
        "cpu_media_percent": round(cpu_media, 2),
        "ram_media_gb": round(ram_media, 2),
        "conexoes_media": round(conexoes_media, 2),
        "sessoes_media": round(sessoes_media, 2)
    })


print("Visão geral concluída!")

#  PRODUTIVIDADE  ########################################################

produtividade = {}

for dado in dados:
    if dado["id_antena"] != "":
        id_antena = dado["id_antena"]
        vazao = float(dado["vazao_mbps"])
        conexoes = int(dado["active_connections"])


        if id_antena not in produtividade:
            produtividade[id_antena] = {
                "vazao_total": 0,
                "conexoes_total": 0,
                "quantidade": 0
            }

        produtividade[id_antena]["vazao_total"] += vazao
        produtividade[id_antena]["conexoes_total"] += conexoes
        produtividade[id_antena]["quantidade"] += 1



resultado_produtividade = []

for id_antena in produtividade:
    quantidade = produtividade[id_antena]["quantidade"]
    vazao_media = (produtividade[id_antena]["vazao_total"] / quantidade)
    conexoes_media = (produtividade[id_antena]["conexoes_total"] / quantidade)

# quanto tráfego a antena consegue transmitir x quantas conexões ela atende
    produtividade_media = vazao_media * conexoes_media

    resultado_produtividade.append({
        "id_antena": id_antena,
        "vazao_media_mbps": round(vazao_media, 2),
        "conexoes_media": round(conexoes_media, 2),
        "produtividade": round(produtividade_media, 2)
    })


resultado_produtividade.sort(key=lambda x: x["produtividade"],reverse=True)

with open("gold/produtividade.csv", "w", newline="") as arquivo:
    colunas = [
        "id_antena",
        "vazao_media_mbps",
        "conexoes_media",
        "produtividade"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in resultado_produtividade:
        escritor.writerow(dado)


print("Análise de produtividade concluída!")


#  GARGALO DE SAÍDA  #################################################

with open("silver/consistencia_trafego.csv", "r") as arquivo:
    leitor = csv.DictReader(arquivo)
    trafego = list(leitor)


resultado_gargalo = []

for dado in trafego:
    bytes_antenas = int(dado["bytes_antenas"])
    bytes_firewall = int(dado["bytes_firewall"])
    diferenca = bytes_firewall - bytes_antenas



    if bytes_antenas > 0:
        percentual_perda = (abs(diferenca) / bytes_antenas) * 100
    else:
        percentual_perda = 0

    if percentual_perda > 10:
        status = "Gargalo de saída"
    else:
        status = "Normal"



    resultado_gargalo.append({
        "timestamp": dado["timestamp"],
        "bytes_antenas": bytes_antenas,
        "bytes_firewall": bytes_firewall,
        "diferenca_bytes": diferenca,
        "percentual_perda": round(percentual_perda, 2),
        "status": status
    })


with open("gold/gargalo_saida.csv", "w", newline="") as arquivo:
    colunas = [
        "timestamp",
        "bytes_antenas",
        "bytes_firewall",
        "diferenca_bytes",
        "percentual_perda",
        "status"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in resultado_gargalo:
        escritor.writerow(dado)


print("Análise de gargalo de saída concluída!")


#  MAPA DE CALOR  ########################################################

mapa_calor = {}

for dado in dados:
    if dado["id_antena"] != "":
        id_antena = dado["id_antena"]

        if id_antena not in mapa_calor:
            mapa_calor[id_antena] = {
                "conexoes_total": 0,
                "cpu_total": 0,
                "ram_total": 0,
                "vazao_total": 0,
                "quantidade": 0
            }


        mapa_calor[id_antena]["conexoes_total"] += int(dado["active_connections"])
        mapa_calor[id_antena]["cpu_total"] += float(dado["cpu_use_percent"])
        mapa_calor[id_antena]["ram_total"] += float(dado["ram_use_gb"])
        mapa_calor[id_antena]["vazao_total"] += float(dado["vazao_mbps"])
        mapa_calor[id_antena]["quantidade"] += 1



resultado_mapa = []

for id_antena in mapa_calor:
    quantidade = mapa_calor[id_antena]["quantidade"]
    conexoes_media = (mapa_calor[id_antena]["conexoes_total"] / quantidade)
    cpu_media = (mapa_calor[id_antena]["cpu_total"] / quantidade)
    ram_media = (mapa_calor[id_antena]["ram_total"] / quantidade)
    vazao_media = (mapa_calor[id_antena]["vazao_total"] / quantidade)


    pontos = 0


    if conexoes_media > 40:
        pontos += 1

    if cpu_media > 85:
        pontos += 1

    if ram_media > 12:
        pontos += 1



    if pontos >= 3:
        nivel = "Critica"

    elif pontos == 2:
        nivel = "Alta"

    elif pontos == 1:
        nivel = "Media"

    else:
        nivel = "Baixa"



    resultado_mapa.append({
        "id_antena": id_antena,
        "conexoes_media": round(conexoes_media, 2),
        "cpu_media_percent": round(cpu_media, 2),
        "ram_media_gb": round(ram_media, 2),
        "vazao_media_mbps": round(vazao_media, 2),
        "nivel_carga": nivel
    })


with open("gold/mapa_calor_logistico.csv", "w", newline="") as arquivo:
    colunas = [
        "id_antena",
        "conexoes_media",
        "cpu_media_percent",
        "ram_media_gb",
        "vazao_media_mbps",
        "nivel_carga"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    escritor.writeheader()

    for dado in resultado_mapa:
        escritor.writerow(dado)


print("Mapa de calor logístico concluído!")