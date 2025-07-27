#!/usr/bin/env python3
"""
Configurador para qBittorrent integrar com organizador de anime
"""

import os
import json
from pathlib import Path

def configure_qbittorrent():
    """Configura qBittorrent para usar o organizador automático"""
    
    # Caminho do arquivo de configuração do qBittorrent
    config_dir = Path.home() / ".config" / "qBittorrent"
    config_file = config_dir / "qBittorrent.conf"
    
    print("🔧 Configurando qBittorrent...")
    
    # Criar diretório se não existir
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Script que será executado quando download completar
    completion_script = """#!/bin/bash
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
"""
    
    # Salvar script de completion
    completion_script_path = "/opt/anime-organizer/qbittorrent-completion.sh"
    os.makedirs("/opt/anime-organizer", exist_ok=True)
    
    with open(completion_script_path, "w") as f:
        f.write(completion_script)
    
    os.chmod(completion_script_path, 0o755)
    
    print(f"✅ Script de completion salvo em: {completion_script_path}")
    
    # Instruções para configuração manual
    print("\n📋 Configuração manual no qBittorrent:")
    print("1. Abra qBittorrent")
    print("2. Vá em Ferramentas → Opções")
    print("3. Na aba 'Downloads':")
    print(f"   - Pasta padrão: /mnt/samsung/Downloads")
    print("4. Na aba 'Conexão':")
    print("   - Habilite 'Executar programa externo ao completar'")
    print(f"   - Comando: {completion_script_path}")
    print("   - Parâmetros: %N %F")
    print("\n5. Alternativamente, use a configuração automática abaixo:")
    
    # Configuração automática (se possível)
    if config_file.exists():
        print(f"\n🔧 Aplicando configuração automática em: {config_file}")
        
        # Backup do arquivo original
        backup_file = config_file.with_suffix('.conf.backup')
        if not backup_file.exists():
            config_file.rename(backup_file)
            print(f"✅ Backup criado: {backup_file}")
        
        # Configurações para qBittorrent
        config_content = f"""[BitTorrent]
Session\\DefaultSavePath=/mnt/samsung/Downloads
Session\\TempPath=/mnt/samsung/Downloads/temp

[Preferences]
Downloads\\SavePath=/mnt/samsung/Downloads
Downloads\\TempPath=/mnt/samsung/Downloads/temp
Downloads\\FinishedTorrentExportDir=
Downloads\\TorrentExportDir=
Downloads\\UseIncompleteExtension=false

[AutoRun]
enabled=true
program={completion_script_path} %N %F
"""
        
        with open(config_file, "w") as f:
            f.write(config_content)
        
        print("✅ Configuração aplicada!")
        print("⚠️ Reinicie o qBittorrent para aplicar as mudanças")
    
    else:
        print("⚠️ Arquivo de configuração do qBittorrent não encontrado")
        print("Configure manualmente conforme instruções acima")

def create_log_rotation():
    """Cria configuração de rotação de logs"""
    logrotate_config = """/var/log/anime-organizer.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    su kikuchi kikuchi
}"""
    
    with open("/etc/logrotate.d/anime-organizer", "w") as f:
        f.write(logrotate_config)
    
    print("✅ Rotação de logs configurada")

if __name__ == "__main__":
    configure_qbittorrent()
    create_log_rotation()
    
    print("\n🎯 Configuração do qBittorrent concluída!")
    print("\nTeste o sistema:")
    print("1. Faça download de um anime")
    print("2. Verifique se aparece em /mnt/samsung/Shares/Anime")
    print("3. Monitore com: tail -f /var/log/anime-organizer.log")