#!/usr/bin/env python3
"""
Monitor de Rede Profissional - Versão 2.0
Autor: SRSALLES
Funcionalidades: Scanner de rede, descoberta de dispositivos, monitoramento contínuo
"""

import subprocess
import re
import socket
import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

class MonitorRedeProfissional:
    def __init__(self):
        self.ip_local = self.obter_ip_local()
        self.rede = self.obter_rede()
        self.data_dir = Path("/app/data") if os.path.exists("/app/data") else Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
    def obter_ip_local(self):
        """Obtém o IP local do computador"""
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "192.168.1.100"
    
    def obter_rede(self):
        """Determina a rede (ex: 192.168.1.0/24)"""
        partes = self.ip_local.split('.')
        return f"{partes[0]}.{partes[1]}.{partes[2]}"
    
    def identificar_fabricante(self, mac):
        """Identifica fabricante pelo MAC"""
        if not mac or mac == 'Desconhecido':
            return 'Desconhecido'
        
        mac_clean = mac.replace('-', '').replace(':', '')[:6].upper()
        
        fabricantes = {
            # Roteadores
            'C83A35': 'TP-Link (Roteador)',
            'F4F26D': 'TP-Link (Roteador)',
            '50C7BF': 'TP-Link (Roteador)',
            'D48564': 'TP-Link (Roteador)',
            '0022BD': 'Intelbras (Roteador)',
            '90E6BA': 'Intelbras (Roteador)',
            '8CDCE4': 'MikroTik (Roteador)',
            '6C3BE5': 'Ubiquiti (AP)',
            '80A589': 'Ubiquiti (AP)',
            '00155D': 'Hyper-V (Virtual)',
            '000C29': 'VMware (Virtual)',
            '005056': 'VMware (Virtual)',
            
            # Smartphones
            'B8A44F': 'Xiaomi (Smartphone)',
            'E8A04B': 'Xiaomi (Smartphone)',
            'A4C138': 'Xiaomi (Smartphone)',
            '88C255': 'Xiaomi (Smartphone)',
            '9CADEF': 'Xiaomi (Smartphone)',
            '8886A5': 'Apple (iPhone)',
            '801F02': 'Apple (iPhone)',
            'F8FFC2': 'Apple (iPhone)',
            'B4345B': 'Apple (iPhone)',
            '689C70': 'Samsung (Smartphone)',
            'D49A20': 'Samsung (Smartphone)',
            'A4B197': 'Samsung (Smartphone)',
            '505A45': 'Samsung (Smartphone)',
            'FCAAA5': 'LG (Smartphone)',
            '0C434A': 'OnePlus (Smartphone)',
            'D00EA4': 'Google (Pixel)',
            '58CF4B': 'Huawei (Smartphone)',
            
            # Smart TVs
            '0026BE': 'Samsung (Smart TV)',
            '08C541': 'LG (Smart TV)',
            '001D32': 'Sony (Smart TV)',
            'DC430A': 'Amazon (FireTV)',
            '88C6D1': 'Roku (Streaming)',
            '942A82': 'TCL (Smart TV)',
            
            # Computadores
            '001EC2': 'Apple (Mac)',
            '002500': 'Apple (Mac)',
            '3CBD92': 'Dell (Computador)',
            '002219': 'Dell (Computador)',
            'F0DEF1': 'HP (Computador)',
            '64F987': 'HP (Computador)',
            'B42E99': 'Lenovo (Computador)',
            'C8F733': 'Lenovo (Computador)',
            '00D861': 'Acer (Computador)',
            'E0D55E': 'Asus (Computador)',
            
            # Impressoras
            '0021B7': 'HP (Impressora)',
            '000C6E': 'Brother (Impressora)',
            '008063': 'Epson (Impressora)',
            '0019F2': 'Canon (Impressora)',
            
            # IoT/Outros
            'B827EB': 'Raspberry Pi (Servidor)',
            'DC4421': 'ESP8266 (IoT)',
            '0018FE': 'Nest/Google Home',
            '6883C0': 'Amazon (Alexa/Echo)',
            '7076FF': 'Microsoft (Xbox)',
            '001CBA': 'Sony (PlayStation)',
            '68D234': 'Câmera IP',
        }
        
        return fabricantes.get(mac_clean, 'Dispositivo')
    
    def scan_arp(self):
        """Scan via tabela ARP"""
        dispositivos = []
        try:
            resultado = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            linhas = resultado.stdout.split('\n')
            
            for linha in linhas:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', linha)
                mac_match = re.search(r'([0-9A-Fa-f]{2}[-:][0-9A-Fa-f]{2}[-:][0-9A-Fa-f]{2}[-:][0-9A-Fa-f]{2}[-:][0-9A-Fa-f]{2}[-:][0-9A-Fa-f]{2})', linha, re.IGNORECASE)
                
                if ip_match and mac_match and not ip_match.group(1).endswith('.255'):
                    mac = mac_match.group(1).upper()
                    dispositivos.append({
                        'ip': ip_match.group(1),
                        'mac': mac,
                        'fabricante': self.identificar_fabricante(mac),
                        'metodo': 'ARP'
                    })
        except Exception as e:
            print(f"Erro no scan ARP: {e}")
        return dispositivos
    
    def scanner_completo(self):
        """Scanner completo que detecta TUDO na rede"""
        print(f"\n{'='*60}")
        print(f"🔍 SCANNER DE REDE PROFISSIONAL v2.0")
        print(f"{'='*60}")
        print(f"📍 Seu IP: {self.ip_local}")
        print(f"📍 Rede: {self.rede}.0/24")
        print(f"{'-'*60}")
        
        # Método: ARP (rápido e confiável)
        print("\n📡 Escaneando via ARP...")
        dispositivos = self.scan_arp()
        
        print(f"\n✅ Encontrados {len(dispositivos)} dispositivos na rede\n")
        return dispositivos
    
    def salvar_inventario(self, dispositivos):
        """Salva inventário em JSON"""
        data = {
            'versao': '2.0',
            'data_scan': datetime.now().isoformat(),
            'ip_local': self.ip_local,
            'rede': f"{self.rede}.0/24",
            'total_dispositivos': len(dispositivos),
            'dispositivos': dispositivos
        }
        
        arquivo = self.data_dir / f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return arquivo
    
    def exibir_tabela(self, dispositivos):
        """Exibe resultados em tabela formatada"""
        if not dispositivos:
            print("❌ Nenhum dispositivo encontrado!")
            return
        
        # Organiza por categoria
        categorias = {}
        for d in dispositivos:
            fab = d.get('fabricante', 'Desconhecido')
            if '(Roteador)' in fab or '(AP)' in fab:
                cat = '🌐 Roteadores/Acess Points'
            elif '(Smartphone)' in fab or '(iPhone)' in fab:
                cat = '📱 Smartphones'
            elif '(Smart TV)' in fab or '(FireTV)' in fab or '(Streaming)' in fab:
                cat = '📺 Smart TVs/Streaming'
            elif '(Computador)' in fab or '(Mac)' in fab or '(Virtual)' in fab:
                cat = '💻 Computadores/Servidores'
            elif '(Impressora)' in fab:
                cat = '🖨️ Impressoras'
            else:
                cat = '🔌 Outros Dispositivos'
            
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(d)
        
        print(f"\n{'='*70}")
        print("📱 DISPOSITIVOS DETECTADOS NA REDE")
        print(f"{'='*70}")
        print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*70}")
        
        for categoria, devices in categorias.items():
            print(f"\n{categoria} ({len(devices)}):")
            print(f"{'-'*50}")
            for d in devices:
                print(f"   📍 {d['ip']:<18} | {d['fabricante']}")
                if d.get('mac'):
                    print(f"      🔑 MAC: {d['mac']}")
        
        print(f"\n{'='*70}")
        print(f"✅ TOTAL: {len(dispositivos)} dispositivos ativos")
        print(f"{'='*70}\n")
    
    def gerar_relatorio_html(self, dispositivos):
        """Gera relatório HTML bonito"""
        html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Rede v2.0 - {datetime.now().strftime('%d/%m/%Y')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 15px; padding: 25px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        h1 {{ color: #667eea; margin-bottom: 10px; }}
        .info {{ color: #666; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 2px solid #eee; }}
        .stats {{ display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }}
        .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; flex: 1; min-width: 150px; text-align: center; }}
        .stat-number {{ font-size: 32px; font-weight: bold; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; }}
        .categoria {{ margin-bottom: 25px; }}
        .categoria h3 {{ color: #667eea; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 2px solid #667eea; }}
        .device-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; }}
        .device {{ background: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .device-ip {{ font-family: monospace; font-weight: bold; color: #667eea; }}
        .device-fab {{ font-size: 12px; color: #666; margin-top: 5px; }}
        .device-mac {{ font-family: monospace; font-size: 11px; color: #999; margin-top: 3px; }}
        .footer {{ text-align: center; color: white; margin-top: 20px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🌐 Monitor de Rede Profissional v2.0</h1>
            <div class="info">
                <strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br>
                <strong>IP Local:</strong> {self.ip_local}<br>
                <strong>Rede:</strong> {self.rede}.0/24
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{len(dispositivos)}</div>
                    <div class="stat-label">Dispositivos</div>
                </div>
            </div>
"""
        
        # Organiza por categoria
        categorias = {'🌐 Roteadores/Acess Points': [], '📱 Smartphones': [], 
                      '📺 Smart TVs/Streaming': [], '💻 Computadores/Servidores': [],
                      '🖨️ Impressoras': [], '🔌 Outros Dispositivos': []}
        
        for d in dispositivos:
            fab = d.get('fabricante', 'Desconhecido')
            if '(Roteador)' in fab or '(AP)' in fab:
                categorias['🌐 Roteadores/Acess Points'].append(d)
            elif '(Smartphone)' in fab or '(iPhone)' in fab:
                categorias['📱 Smartphones'].append(d)
            elif '(Smart TV)' in fab or '(FireTV)' in fab or '(Streaming)' in fab:
                categorias['📺 Smart TVs/Streaming'].append(d)
            elif '(Computador)' in fab or '(Mac)' in fab or '(Virtual)' in fab:
                categorias['💻 Computadores/Servidores'].append(d)
            elif '(Impressora)' in fab:
                categorias['🖨️ Impressoras'].append(d)
            else:
                categorias['🔌 Outros Dispositivos'].append(d)
        
        for categoria, devices in categorias.items():
            if devices:
                html += f"""
            <div class="categoria">
                <h3>{categoria} ({len(devices)})</h3>
                <div class="device-list">"""
                for d in devices:
                    html += f"""
                    <div class="device">
                        <div class="device-ip">{d['ip']}</div>
                        <div class="device-fab">{d['fabricante']}</div>
                        <div class="device-mac">{d.get('mac', 'MAC não disponível')}</div>
                    </div>"""
                html += """
                </div>
            </div>
"""
        
        html += f"""
        </div>
        <div class="footer">
            Monitor de Rede Profissional v2.0 | Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        
        arquivo = self.data_dir / f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return arquivo
    
    def executar(self, salvar=True):
        """Executa o monitor completo"""
        dispositivos = self.scanner_completo()
        self.exibir_tabela(dispositivos)
        
        if salvar and dispositivos:
            arquivo_json = self.salvar_inventario(dispositivos)
            arquivo_html = self.gerar_relatorio_html(dispositivos)
            print(f"💾 Inventário salvo: {arquivo_json}")
            print(f"📄 Relatório HTML: {arquivo_html}")
        
        return dispositivos

def main():
    parser = argparse.ArgumentParser(description='Monitor de Rede Profissional v2.0')
    parser.add_argument('--json', action='store_true', help='Salvar apenas em JSON')
    parser.add_argument('--html', action='store_true', help='Gerar apenas HTML')
    
    args = parser.parse_args()
    
    monitor = MonitorRedeProfissional()
    dispositivos = monitor.executar()
    
    return 0 if dispositivos else 1

if __name__ == "__main__":
    sys.exit(main())
