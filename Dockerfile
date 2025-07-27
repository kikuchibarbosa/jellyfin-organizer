# Dockerfile para Jellyfin Organizer
FROM python:3.11-slim

# Metadados
LABEL maintainer="Hevertton Kikuchi Barbosa <kikuchibarbosa@gmail.com>"
LABEL version="2.0.0"
LABEL description="Sistema de Organização Automática de Animes"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DOWNLOAD_FOLDER=/downloads
ENV ANIME_FOLDER=/anime
ENV LOG_LEVEL=INFO

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -r anime && useradd -r -g anime anime

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Criar diretórios necessários
RUN mkdir -p /downloads /anime /logs

# Definir permissões
RUN chown -R anime:anime /app /downloads /anime /logs
RUN chmod +x scripts/*.sh

# Mudar para usuário não-root
USER anime

# Expor volume para configuração
VOLUME ["/downloads", "/anime", "/logs"]

# Comando padrão
CMD ["python3", "-m", "src.monitor_downloads"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)" || exit 1