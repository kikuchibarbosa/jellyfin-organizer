#!/bin/bash

# Script de instalação do Sistema de Organização Automática de Animes
# Para integração com Jellyfin/Plex e qBittorrent

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎬 Instalador do Sistema de Organização Automática de Animes${NC}"
echo -e "${BLUE}=================================================================${NC}"
echo

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ Este script não deve ser executado como root!${NC}"
   echo -e "${YELLOW}Execute como usuário normal: ./install.sh${NC}"
   exit 1
fi

# Verificar dependências
echo -e "${YELLOW}🔍 Verificando dependências...${NC}"

# Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado!${NC}"
    echo -e "${YELLOW}Instale com: sudo apt install python3 python3-pip${NC}"
    exit 1
fi

# Pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 não encontrado!${NC}"
    echo -e "${YELLOW}Instale com: sudo apt install python3-pip${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependências verificadas${NC}"

# Instalar bibliotecas Python
echo -e "${YELLOW}📦 Instalando bibliotecas Python...${NC}"
pip3 install --user watchdog
echo -e "${GREEN}✅ Bibliotecas instaladas${NC}"

# Solicitar configurações
echo
echo -e "${YELLOW}⚙️ Configuração do sistema:${NC}"
echo

# Pasta de downloads
read -p "📁 Pasta de downloads do qBittorrent [/mnt/samsung/Downloads]: " DOWNLOAD_PATH
DOWNLOAD_PATH=${DOWNLOAD_PATH:-/mnt/samsung/Downloads}

# Pasta de destino
read -p "📺 Pasta de destino para animes [/mnt/samsung/Shares/Anime]: " ANIME_PATH
ANIME_PATH=${ANIME_PATH:-/mnt/samsung/Shares/Anime}

# Verificar se as pastas existem
if [[ ! -d "$DOWNLOAD_PATH" ]]; then
    echo -e "${RED}❌ Pasta de downloads não existe: $DOWNLOAD_PATH${NC}"
    exit 1
fi

if [[ ! -d "$ANIME_PATH" ]]; then
    echo -e "${YELLOW}📁 Criando pasta de destino: $ANIME_PATH${NC}"
    mkdir -p "$ANIME_PATH"
fi

# Criar diretório de instalação
INSTALL_DIR="/opt/anime-organizer"
echo -e "${YELLOW}📦 Criando diretório de instalação...${NC}"
sudo mkdir -p "$INSTALL_DIR"

# Atualizar paths nos arquivos
echo -e "${YELLOW}🔧 Configurando paths...${NC}"

# Atualizar auto_organize_anime.py
sed -i "s|/mnt/samsung/Downloads|$DOWNLOAD_PATH|g" auto_organize_anime.py
sed -i "s|/mnt/samsung/Shares/Anime|$ANIME_PATH|g" auto_organize_anime.py

# Atualizar monitor_downloads.py
sed -i "s|/mnt/samsung/Downloads|$DOWNLOAD_PATH|g" monitor_downloads.py

# Atualizar organize-anime.sh
sed -i "s|/mnt/samsung/Downloads|$DOWNLOAD_PATH|g" organize-anime.sh

# Atualizar qbittorrent-completion.sh
sed -i "s|/mnt/samsung/Downloads|$DOWNLOAD_PATH|g" qbittorrent-completion.sh

# Copiar arquivos para o diretório de instalação
echo -e "${YELLOW}📋 Copiando arquivos...${NC}"
sudo cp auto_organize_anime.py "$INSTALL_DIR/"
sudo cp monitor_downloads.py "$INSTALL_DIR/"
sudo cp qbittorrent-completion.sh "$INSTALL_DIR/"
sudo cp teste_temporadas.py "$INSTALL_DIR/"

# Tornar scripts executáveis
sudo chmod +x "$INSTALL_DIR/qbittorrent-completion.sh"

# Copiar CLI para /usr/local/bin
sudo cp organize-anime.sh /usr/local/bin/organize-anime
sudo chmod +x /usr/local/bin/organize-anime

# Configurar serviço systemd
echo -e "${YELLOW}⚙️ Configurando serviço systemd...${NC}"
sudo cp anime-organizer.service /etc/systemd/system/
sudo systemctl daemon-reload

# Configurar rotação de logs
echo -e "${YELLOW}📝 Configurando rotação de logs...${NC}"
sudo tee /etc/logrotate.d/anime-organizer > /dev/null <<EOF
/var/log/anime-organizer.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF

# Executar organização inicial
echo -e "${YELLOW}🔄 Executando organização inicial...${NC}"
sudo -u $USER python3 "$INSTALL_DIR/auto_organize_anime.py" --organize-all

# Habilitar e iniciar serviço
echo -e "${YELLOW}🚀 Habilitando serviço...${NC}"
sudo systemctl enable anime-organizer
sudo systemctl start anime-organizer

# Verificar status
echo -e "${YELLOW}🔍 Verificando status...${NC}"
if systemctl is-active --quiet anime-organizer; then
    echo -e "${GREEN}✅ Serviço está funcionando!${NC}"
else
    echo -e "${RED}❌ Erro ao iniciar serviço${NC}"
    sudo systemctl status anime-organizer
fi

echo
echo -e "${GREEN}🎉 Instalação concluída com sucesso!${NC}"
echo
echo -e "${BLUE}📋 Configuração do qBittorrent:${NC}"
echo -e "1. Abra qBittorrent"
echo -e "2. Vá em Ferramentas → Opções"
echo -e "3. Na aba 'Downloads':"
echo -e "   - Pasta padrão: ${DOWNLOAD_PATH}"
echo -e "4. Na aba 'Conexão':"
echo -e "   - ✅ Executar programa externo ao completar"
echo -e "   - Comando: /opt/anime-organizer/qbittorrent-completion.sh"
echo -e "   - Parâmetros: %N %F"
echo
echo -e "${BLUE}🔧 Comandos disponíveis:${NC}"
echo -e "   organize-anime status    - Ver status do serviço"
echo -e "   organize-anime organize  - Organizar arquivos manualmente"
echo -e "   organize-anime logs      - Ver logs em tempo real"
echo -e "   organize-anime restart   - Reiniciar serviço"
echo
echo -e "${BLUE}📁 Estrutura criada:${NC}"
echo -e "   ${ANIME_PATH}/"
echo -e "   ├── Nome do Anime/"
echo -e "   │   └── Season 01/"
echo -e "   │       └── Nome do Anime - S01E01.mkv"
echo -e "   └── ..."
echo
echo -e "${GREEN}✅ Sistema pronto para uso!${NC}"