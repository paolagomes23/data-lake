import json
import random
import time
import os
from datetime import datetime


PASTA_BRONZE = "./bronze"
os.makedirs(PASTA_BRONZE, exist_ok=True)
  

def coletar_antena(id_antena):
        bytes_antena[id_antena] += random.randint(100000, 1000000)
        
        dados = {
            "id_antena": id_antena,
            "timestamp": datetime.now().isoformat(),
            "bytes_sent": bytes_antena[id_antena],
            "bytes_recv": random.randint(100000,1000000),
            "active_connections": random.randint(1,50),
            "cpu_use_percent": random.randint(0,100),
            "ram_use_gb": random.randint(0,16)
        }

        return dados


def coletar_firewall():
        total_bytes_antenas = sum(bytes_antena.values())
        
        dados = {
            "timestamp": datetime.now().isoformat(),
            "active_sessions": random.randint(100,1000),
            "dropped_packets": random.randint(0,500),
            "most_blocked_ip": f"192.168.0.{random.randint(1, 254)}",
            "cpu_use_percent": random.randint(0, 100),
            "ram_use_gb": random.randint(0, 16),
            "bytes_sent": total_bytes_antenas,
            "bytes_recv": random.randint(100000, 1000000)
        }

        return dados



bytes_antena = {
    "AP01": 0,
    "AP02": 0,
    "AP03": 0,
    "AP04": 0
}


while True:

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for i in range(1,5):
        id_antena = f"AP0{i}"
        antena = coletar_antena(id_antena)
        file_name = f"{PASTA_BRONZE}/{agora}_{id_antena.lower()}.json"

        with open(file_name, "w") as arquivo:
            json.dump(antena, arquivo, indent=4)

        print(f"{id_antena} salvo localmente!")

        


    firewall = coletar_firewall()
    file_name = f"{PASTA_BRONZE}/{agora}_firewall.json"


    with open(file_name, "w") as arquivo:
        json.dump(firewall, arquivo, indent=4)


    print("Firewall salvo localmente e enviado para S3!")
    print(f"Coleta realizada: {agora}")
    time.sleep(60)