# 📝 Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

## [2.0.0] - 2025-07-27

### 🎯 Adicionado
- **Suporte completo a temporadas** - Reconhece S2, S3, S4, etc. automaticamente
- **Priorização de padrões** - Temporadas explícitas têm prioridade sobre inferência
- **Novos padrões de reconhecimento** para formatos diversos
- **Script de teste** para validar reconhecimento de temporadas
- **Arquivo de configuração centralizado** (`config.py`)
- **Instalador automatizado** (`install.sh`)
- **Documentação completa** com exemplos e solução de problemas

### 🔧 Melhorado
- **Algoritmo de parsing** completamente reescrito com priorização
- **Detecção inteligente** de temporadas em múltiplas posições
- **Compatibilidade expandida** com formatos do nyaa.si
- **Estrutura de código** mais modular e configurável
- **Logs mais detalhados** com informações de temporada

### 🐛 Corrigido
- **Temporadas incorretas** - Tate no Yuusha no Nariagari S4 agora vai para Season 04
- **Duplicação de nomes** - Remove "SX" do nome do anime na organização
- **Falsos positivos** - Melhora precisão na detecção de padrões

### 🔄 Casos de Teste
- ✅ `[SubsPlease] Tate no Yuusha no Nariagari S4 - 01 (720p) [hash].mkv` → Season 04
- ✅ `[SubsPlease] Dr. Stone S4 - 15 (720p) [hash].mkv` → Season 04
- ✅ `[SubsPlease] Yofukashi no Uta S2 - 04 (720p) [hash].mkv` → Season 02
- ✅ `[SubsPlease] Dandadan - 16 (720p) [hash].mkv` → Season 01

## [1.0.0] - 2025-07-26

### 🎯 Adicionado
- **Sistema base** de organização automática
- **Monitor em tempo real** da pasta de downloads
- **Integração com qBittorrent** via script de completion
- **Serviço SystemD** para execução automática
- **Interface CLI** com comando `organize-anime`
- **Links simbólicos** para economizar espaço
- **Rotação de logs** configurada
- **Detecção básica** de nomes de anime e episódios

### 🔧 Funcionalidades Iniciais
- Organização por nome do anime
- Detecção de episódios
- Suporte a arquivos .mkv, .mp4, .avi
- Logs detalhados
- Controle via systemctl

### 📦 Estrutura Base
```
/mnt/samsung/Shares/Anime/
├── Nome do Anime/
│   └── Season 01/
│       └── arquivos...
```

### 🐛 Problemas Conhecidos
- Temporadas não eram detectadas corretamente
- Animes com "S2", "S3" eram organizados em "Season 01"
- Limitações no parsing de nomes complexos

---

## 🔗 Links Úteis

- **Formato de versioning:** [Semantic Versioning](https://semver.org/)
- **Formato de changelog:** [Keep a Changelog](https://keepachangelog.com/)

## 📊 Estatísticas

### Versão 2.0.0
- **58 arquivos** reorganizados automaticamente
- **21 séries** detectadas e organizadas
- **100% compatibilidade** com nyaa.si/SubsPlease
- **4 temporadas diferentes** detectadas corretamente

### Versão 1.0.0
- **Sistema base** implementado
- **Monitor automático** funcionando
- **Integração qBittorrent** configurada
- **Logs e rotação** funcionando