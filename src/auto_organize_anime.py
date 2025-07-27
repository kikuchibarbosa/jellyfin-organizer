#!/usr/bin/env python3
"""
Sistema automático de organização de animes via links simbólicos
- Monitora /mnt/samsung/Downloads
- Cria estrutura organizada em /mnt/samsung/Shares
- Usa links simbólicos para não mover arquivos originais
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

def log_message(message):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def extract_anime_info(filename):
    """Extrai informações do anime do nome do arquivo"""
    original = filename
    
    # Remove extensão
    name = re.sub(r'\.(mkv|mp4|avi)$', '', filename, flags=re.IGNORECASE)
    
    # Padrão 1: Nome - SxxExx (já está correto)
    pattern1 = r'^(.+?)\s*-\s*S(\d+)E(\d+)$'
    match1 = re.match(pattern1, name)
    if match1:
        return match1.group(1).strip(), int(match1.group(2)), int(match1.group(3))
    
    # Padrão 2a: [Grupo] Nome SX - XX (com season explícita - PRIORIDADE)
    pattern2a = r'^\[.*?\]\s*(.+?)\s+S(\d+)\s*-\s*(\d+(?:\.\d+)?)\s*(?:\(.*?\))?\s*(?:\[.*?\])?$'
    match2a = re.match(pattern2a, name)
    if match2a:
        anime_name = match2a.group(1).strip()
        season = int(match2a.group(2))
        episode = match2a.group(3)
        return anime_name, season, episode
    
    # Padrão 2b: [Grupo] Nome - XX (formato fansub sem season explícita)
    pattern2b = r'^\[.*?\]\s*(.+?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:\(.*?\))?\s*(?:\[.*?\])?$'
    match2b = re.match(pattern2b, name)
    if match2b:
        anime_name = match2b.group(1).strip()
        episode = match2b.group(2)
        # Verifica se o nome já contém indicação de season (como "Nome S2")
        season_in_name = re.search(r'\s+S(\d+)$', anime_name)
        if season_in_name:
            season = int(season_in_name.group(1))
            anime_name = re.sub(r'\s+S\d+$', '', anime_name)  # Remove o SX do nome
        else:
            season = 1
        return anime_name, season, episode
    
    # Padrão 3a: Nome SX - XX (sem tags de grupo, com season)
    pattern3a = r'^(.+?)\s+S(\d+)\s*-\s*(\d+(?:\.\d+)?)\s*(?:\(.*?\))?$'
    match3a = re.match(pattern3a, name)
    if match3a:
        anime_name = match3a.group(1).strip()
        season = int(match3a.group(2))
        episode = match3a.group(3)
        return anime_name, season, episode
    
    # Padrão 3b: Nome - XX (sem tags de grupo, sem season explícita)
    pattern3b = r'^(.+?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:\(.*?\))?$'
    match3b = re.match(pattern3b, name)
    if match3b:
        anime_name = match3b.group(1).strip()
        episode = match3b.group(2)
        # Verifica se o nome já contém indicação de season
        season_in_name = re.search(r'\s+S(\d+)$', anime_name)
        if season_in_name:
            season = int(season_in_name.group(1))
            anime_name = re.sub(r'\s+S\d+$', '', anime_name)
        else:
            season = 1
        return anime_name, season, episode
    
    # Padrão 4: Nome XX (sem traço)
    pattern4 = r'^(.+?)\s+(\d+(?:\.\d+)?)\s*(?:\(.*?\))?$'
# Padrão 4a: Nome SXXEXX
    pattern4a = r'^(.+?)\s*S(\d+)E(\d+(?:\.\d+)?)(?:\s*\(.*?\))?$'
    match4a = re.match(pattern4a, name)
    if match4a:
        anime_name = match4a.group(1).strip()
        season = int(match4a.group(2))
        episode = match4a.group(3)
        return anime_name, season, episode
    
    # Padrão 4b: [Grupo] Nome Season X - XX
    pattern4b = r'^\[.*?\]\s*(.+?)\s+Season\s+(\d+)\s*-\s*(\d+(?:\.\d+)?)\s*(?:\(.*?\))?\s*(?:\[.*?\])?$'
    match4b = re.match(pattern4b, name)
    if match4b:
        anime_name = match4b.group(1).strip()
        season = int(match4b.group(2))
        episode = match4b.group(3)
        return anime_name, season, episode
    if match4:
        anime_name = match4.group(1).strip()
        episode = match4.group(2)
        return anime_name, 1, episode
    
    # Padrão 5: [Grupo] Nome - XX.X (episódio especial)
    pattern5 = r'^\[.*?\]\s*(.+?)\s*-\s*(\d+\.\d+)\s*(?:\(.*?\))?$'
    match5 = re.match(pattern5, name)
    if match5:
        anime_name = match5.group(1).strip()
        episode = match5.group(2)
        return anime_name, 1, episode
    
    log_message(f"❌ Não foi possível analisar: {original}")
    return None, None, None

def clean_anime_name(name):
    """Limpa o nome do anime"""
    # Remove informações técnicas
    name = re.sub(r'\b(BD|720p|1080p|AV1|MiNi|x264|x265|HEVC|WebRip|BluRay|WEB-DL)\b', '', name, flags=re.IGNORECASE)
    
    # Remove espaços extras
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Remove traços no final
    name = re.sub(r'\s*-\s*$', '', name)
    
    # Remove caracteres problemáticos para sistema de arquivos
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    
    return name

def create_symlink(source_file, target_file):
    """Cria link simbólico, removendo se já existir"""
    target_path = Path(target_file)
    
    # Criar diretório pai se não existir
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remover link existente se houver
    if target_path.exists() or target_path.is_symlink():
        target_path.unlink()
    
    # Criar novo link simbólico
    try:
        target_path.symlink_to(source_file)
        return True
    except Exception as e:
        log_message(f"❌ Erro ao criar link simbólico: {e}")
        return False

def organize_single_file(source_file, downloads_dir, shares_dir):
    """Organiza um único arquivo"""
    source_path = Path(source_file)
    
    # Verificar se é arquivo de vídeo
    if source_path.suffix.lower() not in ['.mkv', '.mp4', '.avi']:
        return False
    
    filename = source_path.name
    anime_name, season, episode = extract_anime_info(filename)
    
    if not anime_name:
        return False
    
    anime_name = clean_anime_name(anime_name)
    
    # Estrutura de diretórios no shares
    anime_dir = Path(shares_dir) / "Anime" / anime_name
    season_dir = anime_dir / f"Season {season:02d}"
    
    # Formato do episódio
    if isinstance(episode, str) and '.' in episode:
        episode_str = episode.replace('.', '_')
    else:
        episode_str = f"{int(float(episode)):02d}"
    
    # Nome do arquivo final
    new_filename = f"{anime_name} - S{season:02d}E{episode_str}{source_path.suffix}"
    target_file = season_dir / new_filename
    
    # Criar link simbólico
    if create_symlink(source_path, target_file):
        log_message(f"✅ {anime_name} - E{episode_str}")
        log_message(f"   {filename} → {new_filename}")
        return True
    else:
        log_message(f"❌ Falha ao organizar: {filename}")
        return False

def organize_existing_files(downloads_dir, shares_dir):
    """Organiza todos os arquivos existentes"""
    downloads_path = Path(downloads_dir)
    
    if not downloads_path.exists():
        log_message(f"❌ Diretório de downloads não encontrado: {downloads_dir}")
        return
    
    log_message("🔄 Organizando arquivos existentes...")
    
    # Procurar arquivos de vídeo
    video_files = []
    for ext in ['*.mkv', '*.mp4', '*.avi']:
        video_files.extend(downloads_path.glob(ext))
        video_files.extend(downloads_path.glob(f'**/{ext}'))
    
    organized_count = 0
    
    for video_file in video_files:
        if organize_single_file(video_file, downloads_dir, shares_dir):
            organized_count += 1
    
    log_message(f"✅ {organized_count} arquivos organizados!")

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 auto_organize_anime.py organize    # Organiza arquivos existentes")
        print("  python3 auto_organize_anime.py <arquivo>   # Organiza arquivo específico")
        sys.exit(1)
    
    downloads_dir = "/mnt/samsung/Downloads"
    shares_dir = "/mnt/samsung/Shares"
    
    if sys.argv[1] == "organize":
        organize_existing_files(downloads_dir, shares_dir)
    else:
        # Organizar arquivo específico
        file_path = sys.argv[1]
        if organize_single_file(file_path, downloads_dir, shares_dir):
            log_message("✅ Arquivo organizado com sucesso!")
        else:
            log_message("❌ Falha ao organizar arquivo")

if __name__ == "__main__":
    main()