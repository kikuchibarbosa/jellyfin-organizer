#!/usr/bin/env python3
"""
Arquivo de configuração para o Sistema de Organização Automática de Animes
"""

import os
from pathlib import Path

# ============================================================================
# CONFIGURAÇÕES PRINCIPAIS
# ============================================================================

# Pastas do sistema
DOWNLOAD_FOLDER = "/mnt/samsung/Downloads"  # Pasta onde o qBittorrent baixa os arquivos
ANIME_FOLDER = "/mnt/samsung/Shares/Anime"  # Pasta onde os animes serão organizados

# Arquivo de log
LOG_FILE = "/var/log/anime-organizer.log"

# ============================================================================
# CONFIGURAÇÕES DE PROCESSAMENTO
# ============================================================================

# Extensões de arquivo suportadas
SUPPORTED_EXTENSIONS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']

# Tempo de espera para verificar se o arquivo parou de ser modificado (segundos)
FILE_STABILITY_WAIT = 30

# Intervalo de verificação do monitor (segundos)
MONITOR_INTERVAL = 5

# ============================================================================
# CONFIGURAÇÕES DE NOMENCLATURA
# ============================================================================

# Formato do nome do arquivo final
# Disponível: {anime_name}, {season:02d}, {episode}
FILENAME_FORMAT = "{anime_name} - S{season:02d}E{episode}.{extension}"

# Formato do nome da pasta de temporada
# Disponível: {season:02d}
SEASON_FOLDER_FORMAT = "Season {season:02d}"

# ============================================================================
# CONFIGURAÇÕES DE LOG
# ============================================================================

# Nível de log (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

# Formato do log
LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================================================
# CONFIGURAÇÕES AVANÇADAS
# ============================================================================

# Criar links simbólicos ao invés de mover arquivos
USE_SYMLINKS = True

# Remover arquivos originais após criar links simbólicos
REMOVE_ORIGINALS_AFTER_SYMLINK = False

# Permitir sobrescrever arquivos existentes
ALLOW_OVERWRITE = False

# Criar pastas automaticamente se não existirem
CREATE_DIRECTORIES = True

# ============================================================================
# PADRÕES DE EXCLUSÃO
# ============================================================================

# Padrões de arquivo para ignorar (regex)
IGNORE_PATTERNS = [
    r'.*\.part$',        # Arquivos temporários do qBittorrent
    r'.*\.!qB$',         # Arquivos temporários do qBittorrent
    r'.*\.tmp$',         # Arquivos temporários
    r'.*\.crdownload$',  # Arquivos do Chrome
    r'\..*',             # Arquivos ocultos (começam com ponto)
]

# Pastas para ignorar
IGNORE_FOLDERS = [
    '.torrent',
    'temp',
    'tmp',
    '.incomplete',
]

# ============================================================================
# FUNÇÕES DE UTILIDADE
# ============================================================================

def get_config_value(key, default=None):
    """Obtém valor de configuração, priorizando variáveis de ambiente"""
    return os.environ.get(f"ANIME_ORGANIZER_{key.upper()}", default)

def validate_config():
    """Valida se as configurações estão corretas"""
    errors = []
    
    # Verificar se as pastas existem
    if not Path(DOWNLOAD_FOLDER).exists():
        errors.append(f"Pasta de downloads não existe: {DOWNLOAD_FOLDER}")
    
    if not Path(ANIME_FOLDER).exists():
        if CREATE_DIRECTORIES:
            try:
                Path(ANIME_FOLDER).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Não foi possível criar pasta de animes: {e}")
        else:
            errors.append(f"Pasta de animes não existe: {ANIME_FOLDER}")
    
    # Verificar permissões
    if not os.access(DOWNLOAD_FOLDER, os.R_OK):
        errors.append(f"Sem permissão de leitura na pasta: {DOWNLOAD_FOLDER}")
    
    if not os.access(ANIME_FOLDER, os.W_OK):
        errors.append(f"Sem permissão de escrita na pasta: {ANIME_FOLDER}")
    
    return errors

# ============================================================================
# CONFIGURAÇÕES ESPECÍFICAS DO AMBIENTE
# ============================================================================

# Sobrescrever configurações com variáveis de ambiente se existirem
DOWNLOAD_FOLDER = get_config_value("DOWNLOAD_FOLDER", DOWNLOAD_FOLDER)
ANIME_FOLDER = get_config_value("ANIME_FOLDER", ANIME_FOLDER)
LOG_FILE = get_config_value("LOG_FILE", LOG_FILE)
USE_SYMLINKS = get_config_value("USE_SYMLINKS", "true").lower() == "true"

# ============================================================================
# EXIBIR CONFIGURAÇÃO ATUAL (para debug)
# ============================================================================

def print_config():
    """Imprime a configuração atual"""
    print("=" * 60)
    print("CONFIGURAÇÃO ATUAL")
    print("=" * 60)
    print(f"Pasta de Downloads: {DOWNLOAD_FOLDER}")
    print(f"Pasta de Animes:    {ANIME_FOLDER}")
    print(f"Arquivo de Log:     {LOG_FILE}")
    print(f"Usar Links:         {USE_SYMLINKS}")
    print(f"Formato do Arquivo: {FILENAME_FORMAT}")
    print(f"Formato da Pasta:   {SEASON_FOLDER_FORMAT}")
    print("=" * 60)

if __name__ == "__main__":
    print_config()
    errors = validate_config()
    if errors:
        print("ERROS DE CONFIGURAÇÃO:")
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print("✅ Configuração válida!")