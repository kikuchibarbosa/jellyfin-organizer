#!/usr/bin/env python3
"""
Exemplos de uso do Sistema de Organização Automática de Animes
"""

import sys
import os

# Adicionar o caminho do sistema ao PATH
sys.path.append('/opt/anime-organizer')

def example_1_test_recognition():
    """Exemplo 1: Testar reconhecimento de diferentes formatos"""
    from auto_organize_anime import extract_anime_info
    
    print("🧪 Exemplo 1: Testando Reconhecimento de Padrões")
    print("=" * 60)
    
    test_files = [
        "[SubsPlease] Tate no Yuusha no Nariagari S4 - 01 (720p) [1E52143D].mkv",
        "[SubsPlease] Dandadan - 16 (720p) [34C56981].mkv", 
        "[SubsPlease] Dr. Stone S4 - 15 (720p) [68C7DC33].mkv",
        "Attack on Titan S3E22.mkv",
        "One Piece - 1000.mkv"
    ]
    
    for filename in test_files:
        result = extract_anime_info(filename)
        if result:
            anime, season, episode = result
            print(f"✅ {filename}")
            print(f"   → {anime} - Season {season:02d}, Episode {episode}")
        else:
            print(f"❌ {filename} - Não reconhecido")
        print()

def example_2_organize_single_file():
    """Exemplo 2: Organizar um arquivo específico"""
    import subprocess
    
    print("📁 Exemplo 2: Organizando Arquivo Específico")
    print("=" * 60)
    
    # Exemplo de arquivo para organizar
    test_file = "/mnt/samsung/Downloads/[SubsPlease] Exemplo - S2 - 05 (720p) [ABC123].mkv"
    
    if os.path.exists(test_file):
        try:
            result = subprocess.run([
                'python3', 
                '/opt/anime-organizer/auto_organize_anime.py', 
                test_file
            ], capture_output=True, text=True)
            
            print("Saída do comando:")
            print(result.stdout)
            
            if result.stderr:
                print("Erros:")
                print(result.stderr)
                
        except Exception as e:
            print(f"Erro ao executar: {e}")
    else:
        print(f"Arquivo de teste não encontrado: {test_file}")
        print("Crie um arquivo de teste para experimentar!")

def example_3_monitor_status():
    """Exemplo 3: Verificar status do sistema"""
    import subprocess
    
    print("📊 Exemplo 3: Status do Sistema")
    print("=" * 60)
    
    commands = [
        ("Status do Serviço", ["organize-anime", "status"]),
        ("Últimas 10 linhas do log", ["tail", "-n", "10", "/var/log/anime-organizer.log"]),
    ]
    
    for description, cmd in commands:
        print(f"\n{description}:")
        print("-" * 30)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            
            if result.stderr:
                print("Erros:", result.stderr)
                
        except Exception as e:
            print(f"Erro ao executar comando: {e}")

def example_4_directory_structure():
    """Exemplo 4: Mostrar estrutura de diretórios"""
    import subprocess
    
    print("📂 Exemplo 4: Estrutura de Diretórios")
    print("=" * 60)
    
    anime_folder = "/mnt/samsung/Shares/Anime"
    
    if os.path.exists(anime_folder):
        try:
            # Mostrar estrutura com tree (se disponível) ou ls
            if subprocess.run(["which", "tree"], capture_output=True).returncode == 0:
                result = subprocess.run([
                    "tree", "-L", "3", anime_folder
                ], capture_output=True, text=True)
            else:
                # Fallback para ls se tree não estiver disponível
                result = subprocess.run([
                    "find", anime_folder, "-maxdepth", "3", "-type", "d"
                ], capture_output=True, text=True)
            
            print("Estrutura atual:")
            print(result.stdout)
            
        except Exception as e:
            print(f"Erro ao listar diretórios: {e}")
    else:
        print(f"Pasta de animes não encontrada: {anime_folder}")

def example_5_configuration():
    """Exemplo 5: Exibir configuração atual"""
    
    print("⚙️ Exemplo 5: Configuração Atual")
    print("=" * 60)
    
    try:
        from config import print_config, validate_config
        
        print_config()
        
        print("\nValidação da configuração:")
        errors = validate_config()
        
        if not errors:
            print("✅ Configuração válida!")
        else:
            print("❌ Problemas encontrados:")
            for error in errors:
                print(f"   • {error}")
                
    except ImportError:
        print("❌ Arquivo config.py não encontrado")
        print("Execute o instalador primeiro!")

def main():
    """Função principal - executa todos os exemplos"""
    
    print("🎬 Exemplos de Uso - Sistema de Organização de Animes")
    print("=" * 70)
    print()
    
    examples = [
        example_1_test_recognition,
        example_2_organize_single_file, 
        example_3_monitor_status,
        example_4_directory_structure,
        example_5_configuration
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"❌ Erro no exemplo {i}: {e}")
        
        if i < len(examples):
            input("\nPressione Enter para continuar...")
            print("\n" + "="*70 + "\n")
    
    print()
    print("🎉 Exemplos concluídos!")
    print()
    print("💡 Dicas:")
    print("   • Use 'organize-anime --help' para ver todas as opções")
    print("   • Monitore os logs com 'organize-anime logs'")
    print("   • Configure o qBittorrent conforme a documentação")

if __name__ == "__main__":
    main()