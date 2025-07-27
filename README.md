# 🎬 Sistema de Organização Automática de Animes

Sistema automatizado para organização de downloads de animes, com integração ao qBittorrent e compatibilidade com Jellyfin/Plex.

## 📋 Funcionalidades

- ✅ **Organização automática** de arquivos por nome do anime e temporada
- ✅ **Detecção inteligente** de nomes de anime, temporadas e episódios
- ✅ **Suporte completo a temporadas** (S2, S3, S4, etc.)
- ✅ **Links simbólicos** para economizar espaço em disco
- ✅ **Integração com qBittorrent** para organização automática
- ✅ **Monitoramento em tempo real** da pasta de downloads
- ✅ **Compatibilidade com nyaa.si** e grupos de fansub
- ✅ **Logs detalhados** de todas as operações
- ✅ **Interface de linha de comando** para gerenciamento

## 🚀 Instalação Rápida

```bash
# Clonar repositório
git clone https://github.com/kikuchibarbosa/jellyfin-organizer.git
cd jellyfin-organizer

# Instalar com Makefile (recomendado)
make deploy

# OU usar instalador tradicional
chmod +x tools/install.sh
./tools/install.sh
```

## 📁 Estrutura Final

```
/mnt/samsung/Shares/Anime/
├── Dandadan/
│   └── Season 01/
│       ├── Dandadan - S01E13.mkv
│       ├── Dandadan - S01E14.mkv
│       └── ...
├── Tate no Yuusha no Nariagari/
│   └── Season 04/
│       ├── Tate no Yuusha no Nariagari - S04E01.mkv
│       ├── Tate no Yuusha no Nariagari - S04E02.mkv
│       └── ...
└── Dr. Stone/
    └── Season 04/
        └── Dr. Stone - S04E15.mkv
```

## 🎯 Formatos Suportados

O sistema reconhece automaticamente diversos formatos de arquivo:

### ✅ Com Temporadas Explícitas
```
[SubsPlease] Tate no Yuusha no Nariagari S4 - 01 (720p) [hash].mkv
[SubsPlease] Dr. Stone S4 - 15 (720p) [hash].mkv
[SubsPlease] Yofukashi no Uta S2 - 04 (720p) [hash].mkv
[Grupo] Nome do Anime S3 - 22 (1080p) [hash].mkv
```

### ✅ Sem Temporadas (assume S01)
```
[SubsPlease] Dandadan - 16 (720p) [hash].mkv
[SubsPlease] Kaijuu 8-gou - 14 (720p) [hash].mkv
[Grupo] Nome do Anime - 05 (720p) [hash].mkv
```

### ✅ Outros Formatos
```
Nome do Anime S2E05.mkv
Nome do Anime - 12.mkv
[Grupo] Nome Season 2 - 10 (720p) [hash].mkv
```

## 🔧 Comandos de Gerenciamento

### Com Makefile (Recomendado)
```bash
make help          # Ver todos os comandos disponíveis
make deploy        # Instalar e iniciar sistema
make start         # Iniciar serviço
make stop          # Parar serviço
make restart       # Reiniciar serviço
make status        # Ver status
make logs          # Ver logs em tempo real
make test          # Executar testes
make uninstall     # Desinstalar sistema
```

### Com CLI Tradicional
```bash
organize-anime organize  # Organizar arquivos existentes
organize-anime status    # Ver status do serviço
organize-anime logs      # Ver logs em tempo real
organize-anime restart   # Reiniciar serviço
```

## ⚙️ Configuração do qBittorrent

Após a instalação, configure no qBittorrent:

1. **Ferramentas** → **Opções**
2. Aba **Downloads**:
   - Pasta padrão: `/mnt/samsung/Downloads`
3. Aba **Conexão**:
   - ✅ Executar programa externo ao completar
   - Comando: `/opt/anime-organizer/qbittorrent-completion.sh`
   - Parâmetros: `%N %F`

## 📦 Arquivos do Sistema

### Scripts Principais
- **`auto_organize_anime.py`** - Motor principal de organização
- **`monitor_downloads.py`** - Monitor em tempo real
- **`config.py`** - Configurações centralizadas

### Scripts de Sistema
- **`organize-anime.sh`** - Interface de linha de comando
- **`qbittorrent-completion.sh`** - Integração com qBittorrent
- **`anime-organizer.service`** - Serviço SystemD

### Utilitários
- **`teste_temporadas.py`** - Script para testar reconhecimento
- **`install.sh`** - Instalador automatizado

## 🔍 Testando o Sistema

```bash
# Testar reconhecimento de padrões
python3 /opt/anime-organizer/teste_temporadas.py

# Testar arquivo específico
python3 /opt/anime-organizer/auto_organize_anime.py "arquivo.mkv"

# Organizar todos os arquivos
organize-anime organize
```

## 📊 Logs e Monitoramento

```bash
# Ver logs em tempo real
organize-anime logs

# Logs do sistema
tail -f /var/log/anime-organizer.log

# Status do serviço
systemctl status anime-organizer
```

## 🛠️ Configuração Avançada

Edite `/opt/anime-organizer/config.py` para personalizar:

```python
# Pastas do sistema
DOWNLOAD_FOLDER = "/mnt/samsung/Downloads"
ANIME_FOLDER = "/mnt/samsung/Shares/Anime"

# Usar links simbólicos (economiza espaço)
USE_SYMLINKS = True

# Formato do nome do arquivo
FILENAME_FORMAT = "{anime_name} - S{season:02d}E{episode}.{extension}"

# Formato da pasta de temporada
SEASON_FOLDER_FORMAT = "Season {season:02d}"
```

## 🔄 Desinstalação

```bash
# Parar e desabilitar serviço
sudo systemctl stop anime-organizer
sudo systemctl disable anime-organizer

# Remover arquivos
sudo rm -rf /opt/anime-organizer
sudo rm /usr/local/bin/organize-anime
sudo rm /etc/systemd/system/anime-organizer.service
sudo rm /etc/logrotate.d/anime-organizer

# Recarregar systemd
sudo systemctl daemon-reload
```

## 🐛 Solução de Problemas

### Serviço não funciona
```bash
# Verificar status
organize-anime status

# Verificar logs
organize-anime logs

# Reiniciar serviço
organize-anime restart
```

### Arquivos não são organizados
```bash
# Verificar se o arquivo é reconhecido
python3 /opt/anime-organizer/teste_temporadas.py

# Organizar manualmente
organize-anime organize

# Verificar permissões
ls -la /mnt/samsung/Downloads/
ls -la /mnt/samsung/Shares/Anime/
```

### Temporadas incorretas
```bash
# Testar reconhecimento
python3 /opt/anime-organizer/teste_temporadas.py

# Reorganizar todos os arquivos
organize-anime organize
```

## 🎯 Compatibilidade

- ✅ **nyaa.si** - Compatível com SubsPlease e outros grupos
- ✅ **qBittorrent** - Integração completa
- ✅ **Jellyfin** - Estrutura de pastas otimizada
- ✅ **Plex** - Compatível com padrões de nomenclatura
- ✅ **Linux** - Testado em Ubuntu/Debian

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commite suas mudanças
4. Faça um push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte, abra uma issue no repositório ou entre em contato através dos canais oficiais.

---

**Última atualização:** 27/07/2025  
**Versão:** 2.0.0  
**Status:** ✅ Estável e em produção
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commite suas mudanças
4. Faça um push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte, abra uma issue no repositório ou entre em contato através dos canais oficiais.

---

**Última atualização:** 27/07/2025  
**Versão:** 2.0.0  
**Status:** ✅ Estável e em produção