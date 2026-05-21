# Monitor de Rede Profissional - Versão 2.0
FROM python:3.9-slim

# Informações do mantenedor
LABEL maintainer="SRSALLES"
LABEL version="2.0"
LABEL description="Scanner de rede profissional com detecção de dispositivos"

# Instalar ferramentas necessárias
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    arp-scan \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Copiar o código
COPY src/ ./src/
COPY data/ ./data/

# Criar diretório para dados
RUN mkdir -p /app/data

# Volume para persistir dados
VOLUME ["/app/data"]

# Porta para futura API (opcional)
EXPOSE 5000

# Comando padrão
CMD ["python", "src/monitor_v2.py"]
