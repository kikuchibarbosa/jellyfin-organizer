#!/usr/bin/env python3
"""
Monitor de downloads para organização automática
Usa inotify para detectar novos arquivos e organizá-los automaticamente
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AnimeDownloadHandler(FileSystemEventHandler):
    """Handler para eventos de download de anime"""
    
    def __init__(self, organize_script):
        self.organize_script = organize_script
        self.processed_files = set()
        
    def log_message(self, message):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def is_video_file(self, filename):
        """Verifica se é arquivo de vídeo"""
        return filename.lower().endswith(('.mkv', '.mp4', '.avi'))
    
    def is_download_complete(self, filepath):
        """Verifica se o download foi concluído"""
        path = Path(filepath)
        
        # Verificar se arquivo existe
        if not path.exists():
            return False
        
        # Verificar se não é arquivo temporário
        if path.name.startswith('.') or path.name.endswith('.part'):
            return False
        
        # Verificar se arquivo não está sendo escrito
        try:
            # Tentar abrir o arquivo em modo exclusivo
            with open(filepath, 'r+b') as f:
                pass
            return True
        except (IOError, OSError):
            return False
    
    def organize_file(self, filepath):
        """Organiza o arquivo usando o script"""
        try:
            result = subprocess.run([
                'python3', self.organize_script, filepath
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_message(f"✅ Arquivo organizado: {Path(filepath).name}")
                return True
            else:
                self.log_message(f"❌ Erro ao organizar: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            self.log_message(f"⏱️ Timeout ao organizar: {filepath}")
            return False
        except Exception as e:
            self.log_message(f"❌ Erro: {e}")
            return False
    
    def on_created(self, event):
        """Callback para arquivo criado"""
        if event.is_directory:
            return
        
        filepath = event.src_path
        
        # Verificar se é arquivo de vídeo
        if not self.is_video_file(filepath):
            return
        
        # Evitar processar o mesmo arquivo múltiplas vezes
        if filepath in self.processed_files:
            return
        
        self.log_message(f"📁 Novo arquivo detectado: {Path(filepath).name}")
        
        # Aguardar alguns segundos para garantir que o download terminou
        time.sleep(5)
        
        # Verificar se download foi concluído
        if self.is_download_complete(filepath):
            self.processed_files.add(filepath)
            self.organize_file(filepath)
        else:
            self.log_message(f"⏳ Download ainda em andamento: {Path(filepath).name}")
    
    def on_moved(self, event):
        """Callback para arquivo movido (renomeado)"""
        if event.is_directory:
            return
        
        # Quando qBittorrent termina o download, ele move o arquivo .part para o nome final
        if self.is_video_file(event.dest_path):
            self.on_created(type('Event', (), {'src_path': event.dest_path, 'is_directory': False})())

def main():
    """Função principal do monitor"""
    downloads_dir = "/mnt/samsung/Downloads"
    organize_script = "/tmp/auto_organize_anime.py"
    
    # Verificar se diretório existe
    if not os.path.exists(downloads_dir):
        print(f"❌ Diretório de downloads não encontrado: {downloads_dir}")
        sys.exit(1)
    
    # Verificar se script de organização existe
    if not os.path.exists(organize_script):
        print(f"❌ Script de organização não encontrado: {organize_script}")
        sys.exit(1)
    
    print(f"🔍 Monitorando diretório: {downloads_dir}")
    print(f"📁 Organizando em: /mnt/samsung/Shares/Anime")
    print("🎬 Aguardando novos downloads...")
    
    # Configurar monitor
    event_handler = AnimeDownloadHandler(organize_script)
    observer = Observer()
    observer.schedule(event_handler, downloads_dir, recursive=True)
    
    # Iniciar monitoramento
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Parando monitor...")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()