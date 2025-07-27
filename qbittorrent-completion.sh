#!/bin/bash
# Script chamado pelo qBittorrent quando download completa
# Argumentos: %N (nome) %F (caminho completo)

ANIME_ORGANIZER="/opt/anime-organizer/auto_organize_anime.py"
FILE_PATH="$2"

# Log da execução
echo "[$(date)] qBittorrent completion: $FILE_PATH" >> /var/log/anime-organizer.log

# Aguardar um pouco para garantir que arquivo está completo
sleep 5

# Organizar o arquivo
python3 "$ANIME_ORGANIZER" "$FILE_PATH" >> /var/log/anime-organizer.log 2>&1
