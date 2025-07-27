# Sistema de Organização Automática de Animes

## 📋 Visão Geral

Sistema automatizado para organização de downloads de animes no servidor, com integração ao qBittorrent e estrutura padronizada de pastas.

## 🎯 Funcionalidades

- ✅ **Organização automática** de arquivos por nome do anime e temporada
- ✅ **Detecção inteligente** de nomes de anime e episódios
- ✅ **Links simbólicos** para economizar espaço
- ✅ **Integração com qBittorrent** para organização automática
- ✅ **Monitoramento em tempo real** da pasta de downloads
- ✅ **Logs detalhados** de todas as operações
- ✅ **Interface de linha de comando** para gerenciamento

## 📁 Estrutura de Pastas

```
/mnt/samsung/Shares/Anime/
├── Dandadan/
│   └── Season 01/
│       ├── Dandadan - S01E13.mkv
│       ├── Dandadan - S01E14.mkv
│       └── ...
├── Kaijuu 8-gou/
│   └── Season 01/
│       └── ...
└── ...
```

## 🔧 Comandos de Gerenciamento

Use o comando `organize-anime` para gerenciar o sistema:

```bash
# Organizar arquivos existentes manualmente
organize-anime organize

# Controle do serviço
organize-anime start     # Iniciar monitor
organize-anime stop      # Parar monitor
organize-anime restart   # Reiniciar monitor
organize-anime status    # Ver status
organize-anime logs      # Ver logs em tempo real
organize-anime enable    # Habilitar início automático
```

## 📦 Componentes do Sistema

### 1. Scripts Python
- **`auto_organize_anime.py`** - Motor principal de organização
- **`monitor_downloads.py`** - Monitor em tempo real da pasta de downloads

### 2. Serviço SystemD
- **`anime-organizer.service`** - Executa o monitor automaticamente

### 3. Scripts de Shell
- **`organize-anime`** - Interface de linha de comando
- **`qbittorrent-completion.sh`** - Script de integração com qBittorrent

## ⚙️ Configuração do qBittorrent

Configure no qBittorrent:

1. **Ferramentas** → **Opções**
2. Aba **Downloads**:
   - Pasta padrão: `/mnt/samsung/Downloads`
3. Aba **Conexão**:
   - ✅ Executar programa externo ao completar
   - Comando: `/opt/anime-organizer/qbittorrent-completion.sh`
   - Parâmetros: `%N %F`

## 🔍 Padrões de Arquivo Suportados

O sistema reconhece os seguintes formatos de nome:

- `[SubsPlease] Dandadan - 16 (720p) [34C56981].mkv`
- `[Grupo] Nome do Anime S2 - 05 (qualidade) [hash].mkv`
- `Nome do Anime - 12.mkv`
- `Nome do Anime S3E04.mkv`

## 📊 Logs e Monitoramento

```bash
# Ver logs do serviço
organize-anime logs

# Logs do sistema
tail -f /var/log/anime-organizer.log

# Status do serviço
systemctl status anime-organizer
```

## 🛠️ Solução de Problemas

### Serviço não está funcionando
```bash
organize-anime restart
organize-anime status
```

### Arquivos não sendo organizados
```bash
# Verificar logs
organize-anime logs

# Organizar manualmente
organize-anime organize

# Testar arquivo específico
python3 /opt/anime-organizer/auto_organize_anime.py "caminho/do/arquivo.mkv"
```

### Verificar permissões
```bash
# Verificar se usuário tem permissões nas pastas
ls -la /mnt/samsung/Downloads/
ls -la /mnt/samsung/Shares/Anime/
```

## 📋 Status da Instalação

✅ Scripts Python instalados em `/opt/anime-organizer/`  
✅ Serviço SystemD configurado e habilitado  
✅ Comando `organize-anime` disponível globalmente  
✅ Rotação de logs configurada  
✅ 58 arquivos organizados na instalação inicial  
✅ Monitor ativo e funcionando  

## 🎬 Teste do Sistema

1. Faça download de um novo anime via qBittorrent
2. Aguarde o download completar
3. Verifique se aparece organizado em `/mnt/samsung/Shares/Anime/`
4. Monitor os logs: `organize-anime logs`

---

**Data da instalação:** 27/07/2025  
**Servidor:** kikuchi@192.168.151.201  
**Status:** ✅ Operacional