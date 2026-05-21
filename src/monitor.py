#!/usr/bin/env python3
import subprocess
import datetime
import sys

def pingar(host):
    try:
        resultado = subprocess.run(
            ['ping', '-c', '1', '-W', '1', host],
            capture_output=True
        )
        return resultado.returncode == 0
    except:
        return False

def main():
    print(f"[{datetime.datetime.now()}] Monitoramento Iniciado")
    print("=" * 40)
    
    hosts = ['localhost', '172.31.128.253', '8.8.8.8', 'google.com']
    
    for host in hosts:
        status = pingar(host)
        if status:
            print(f"✅ {host:20} - ONLINE")
        else:
            print(f"❌ {host:20} - OFFLINE")
    
    print("=" * 40)

if __name__ == "__main__":
    main()
