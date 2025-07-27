#!/usr/bin/env python3
"""
Script para testar o reconhecimento de temporadas no sistema de organização de animes
"""

import sys
import os
sys.path.append('/opt/anime-organizer')

from auto_organize_anime import extract_anime_info

def test_season_recognition():
    """Testa o reconhecimento de temporadas em diferentes formatos"""
    
    test_cases = [
        # Casos com temporadas explícitas
        "[SubsPlease] Tate no Yuusha no Nariagari S4 - 01 (720p) [1E52143D].mkv",
        "[SubsPlease] Dr. Stone S4 - 15 (720p) [68C7DC33].mkv", 
        "[SubsPlease] Yofukashi no Uta S2 - 04 (720p) [A00F1180].mkv",
        "[SubsPlease] Attack on Titan S3 - 22 (720p) [ABC123].mkv",
        
        # Casos sem temporadas (assumir S01)
        "[SubsPlease] Dandadan - 16 (720p) [34C56981].mkv",
        "[SubsPlease] Kaijuu 8-gou - 14 (720p) [B8E57762].mkv",
        "[SubsPlease] Bad Girl - 04 (720p) [0983C8F1].mkv",
        
        # Casos com episódios especiais
        "[SubsPlease] Koujo Denka no Kateikyoushi - 04.5 (720p) [8BC844D2].mkv",
        
        # Casos sem tags de grupo
        "Dr. Stone S4 - 15.mkv",
        "Dandadan - 16.mkv",
        "Attack on Titan S3 - 22.mkv",
    ]
    
    print("🧪 Teste de Reconhecimento de Temporadas")
    print("=" * 80)
    
    for filename in test_cases:
        print(f"\n📂 Arquivo: {filename}")
        
        try:
            result = extract_anime_info(filename)
            if result:
                anime_name, season, episode = result
                print(f"✅ Reconhecido: {anime_name} - Temporada {season:02d}, Episódio {episode}")
                print(f"   Será organizado como: {anime_name} - S{season:02d}E{episode.zfill(2)}.mkv")
                print(f"   Pasta: {anime_name}/Season {season:02d}/")
            else:
                print("❌ Não foi possível analisar")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    print("\n" + "=" * 80)
    print("🎯 Teste concluído!")

if __name__ == "__main__":
    test_season_recognition()