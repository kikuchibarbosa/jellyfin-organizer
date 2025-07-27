# Makefile para Jellyfin Organizer
# Sistema de Organização Automática de Animes

# Variáveis de configuração
PROJECT_NAME = jellyfin-organizer
VERSION = 2.0.0
INSTALL_DIR = /opt/anime-organizer
SERVICE_NAME = anime-organizer
CONFIG_FILE = config/default.conf
SYSTEMD_DIR = /etc/systemd/system
LOGROTATE_DIR = /etc/logrotate.d
BIN_DIR = /usr/local/bin

# Cores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
PURPLE = \033[0;35m
CYAN = \033[0;36m
NC = \033[0m

# Verificar se está sendo executado como root
define check_root
	@if [ "$$(id -u)" -eq 0 ]; then \
		echo "$(RED)❌ Este comando não deve ser executado como root!$(NC)"; \
		echo "$(YELLOW)Execute como usuário normal: make $1$(NC)"; \
		exit 1; \
	fi
endef

# Verificar se está sendo executado como usuário normal
define check_user
	@if [ "$$(id -u)" -eq 0 ]; then \
		echo "$(RED)❌ Este comando deve ser executado como root!$(NC)"; \
		echo "$(YELLOW)Execute com sudo: sudo make $1$(NC)"; \
		exit 1; \
	fi
endef

# Verificar dependências
define check_deps
	@echo "$(BLUE)🔍 Verificando dependências...$(NC)"
	@command -v python3 >/dev/null 2>&1 || { echo "$(RED)❌ Python 3 não encontrado!$(NC)"; exit 1; }
	@command -v pip3 >/dev/null 2>&1 || { echo "$(RED)❌ pip3 não encontrado!$(NC)"; exit 1; }
	@echo "$(GREEN)✅ Dependências verificadas$(NC)"
endef

# Carregar configurações
define load_config
	@if [ -f "$(CONFIG_FILE)" ]; then \
		. ./$(CONFIG_FILE); \
	else \
		echo "$(YELLOW)⚠️  Arquivo de configuração não encontrado: $(CONFIG_FILE)$(NC)"; \
	fi
endef

.PHONY: help install uninstall start stop restart status logs test clean build deploy dev-setup check-config docker-build docker-run docker-stop docker-logs docker-deploy

# Comando padrão
help:
	@echo "$(BLUE)🎬 Jellyfin Organizer - Sistema de Organização Automática de Animes$(NC)"
	@echo "$(BLUE)================================================================$(NC)"
	@echo ""
	@echo "$(CYAN)Comandos disponíveis:$(NC)"
	@echo "  $(GREEN)install$(NC)        - Instalar o sistema completo"
	@echo "  $(GREEN)uninstall$(NC)      - Desinstalar completamente"
	@echo "  $(GREEN)start$(NC)          - Iniciar o serviço"
	@echo "  $(GREEN)stop$(NC)           - Parar o serviço"
	@echo "  $(GREEN)restart$(NC)        - Reiniciar o serviço"
	@echo "  $(GREEN)status$(NC)         - Ver status do serviço"
	@echo "  $(GREEN)logs$(NC)           - Ver logs em tempo real"
	@echo "  $(GREEN)test$(NC)           - Executar testes"
	@echo "  $(GREEN)clean$(NC)          - Limpar arquivos temporários"
	@echo "  $(GREEN)build$(NC)          - Compilar/preparar arquivos"
	@echo "  $(GREEN)deploy$(NC)         - Deploy completo (install + start)"
	@echo "  $(GREEN)dev-setup$(NC)      - Configurar ambiente de desenvolvimento"
	@echo "  $(GREEN)check-config$(NC)   - Verificar configuração"
	@echo ""
	@echo "$(CYAN)Comandos Docker:$(NC)"
	@echo "  $(GREEN)docker-build$(NC)   - Construir imagem Docker"
	@echo "  $(GREEN)docker-run$(NC)     - Executar com Docker"
	@echo "  $(GREEN)docker-stop$(NC)    - Parar container Docker"
	@echo "  $(GREEN)docker-logs$(NC)    - Ver logs do container"
	@echo "  $(GREEN)docker-deploy$(NC)  - Deploy completo com Docker"
	@echo ""
	@echo "$(CYAN)Exemplos:$(NC)"
	@echo "  make install         # Instalar sistema"
	@echo "  make deploy          # Deploy completo"
	@echo "  make docker-deploy   # Deploy com Docker"
	@echo "  make test            # Executar testes"
	@echo "  make logs            # Ver logs"
	@echo ""
	@echo "$(YELLOW)Versão: $(VERSION)$(NC)"

# Verificar configuração
check-config:
	@echo "$(BLUE)⚙️  Verificando configuração...$(NC)"
	$(call load_config)
	@python3 src/config.py
	@echo "$(GREEN)✅ Configuração verificada$(NC)"

# Instalar dependências Python
install-deps:
	@echo "$(BLUE)📦 Instalando dependências Python...$(NC)"
	@pip3 install --user watchdog
	@echo "$(GREEN)✅ Dependências instaladas$(NC)"

# Preparar diretórios
prepare-dirs:
	@echo "$(BLUE)📁 Preparando diretórios...$(NC)"
	@sudo mkdir -p $(INSTALL_DIR)
	@sudo mkdir -p $(INSTALL_DIR)/logs
	@sudo mkdir -p /var/log
	@echo "$(GREEN)✅ Diretórios preparados$(NC)"

# Copiar arquivos
copy-files:
	@echo "$(BLUE)📋 Copiando arquivos...$(NC)"
	@sudo cp src/*.py $(INSTALL_DIR)/
	@sudo cp scripts/* $(INSTALL_DIR)/
	@sudo cp config/default.conf $(INSTALL_DIR)/
	@sudo chmod +x $(INSTALL_DIR)/*.sh
	@sudo cp scripts/organize-anime.sh $(BIN_DIR)/organize-anime
	@sudo chmod +x $(BIN_DIR)/organize-anime
	@echo "$(GREEN)✅ Arquivos copiados$(NC)"

# Configurar serviço systemd
setup-service:
	@echo "$(BLUE)⚙️  Configurando serviço systemd...$(NC)"
	@sudo cp config/$(SERVICE_NAME).service $(SYSTEMD_DIR)/
	@sudo systemctl daemon-reload
	@echo "$(GREEN)✅ Serviço configurado$(NC)"

# Configurar logrotate
setup-logrotate:
	@echo "$(BLUE)📝 Configurando rotação de logs...$(NC)"
	@sudo tee $(LOGROTATE_DIR)/$(SERVICE_NAME) > /dev/null <<EOF
/var/log/$(SERVICE_NAME).log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        /bin/systemctl reload-or-restart $(SERVICE_NAME) > /dev/null 2>&1 || true
    endscript
}
EOF
	@echo "$(GREEN)✅ Rotação de logs configurada$(NC)"

# Organização inicial
initial-organize:
	@echo "$(BLUE)🔄 Executando organização inicial...$(NC)"
	@sudo -u $$USER python3 $(INSTALL_DIR)/auto_organize_anime.py --organize-all || true
	@echo "$(GREEN)✅ Organização inicial concluída$(NC)"

# Instalar sistema completo
install: check-config
	$(call check_root,install)
	$(call check_deps)
	@echo "$(BLUE)🚀 Iniciando instalação do $(PROJECT_NAME) v$(VERSION)...$(NC)"
	@$(MAKE) install-deps
	@$(MAKE) prepare-dirs
	@$(MAKE) copy-files
	@$(MAKE) setup-service
	@$(MAKE) setup-logrotate
	@$(MAKE) initial-organize
	@echo "$(GREEN)🎉 Instalação concluída com sucesso!$(NC)"
	@echo ""
	@echo "$(CYAN)📋 Próximos passos:$(NC)"
	@echo "  1. Configure o qBittorrent:"
	@echo "     - Comando: $(INSTALL_DIR)/qbittorrent-completion.sh"
	@echo "     - Parâmetros: %N %F"
	@echo "  2. Inicie o serviço: make start"
	@echo "  3. Monitore os logs: make logs"

# Desinstalar sistema
uninstall:
	@echo "$(BLUE)🗑️  Desinstalando $(PROJECT_NAME)...$(NC)"
	@$(MAKE) stop || true
	@sudo systemctl disable $(SERVICE_NAME) || true
	@sudo rm -f $(SYSTEMD_DIR)/$(SERVICE_NAME).service
	@sudo rm -f $(LOGROTATE_DIR)/$(SERVICE_NAME)
	@sudo rm -f $(BIN_DIR)/organize-anime
	@sudo rm -rf $(INSTALL_DIR)
	@sudo systemctl daemon-reload
	@echo "$(GREEN)✅ Sistema desinstalado$(NC)"

# Iniciar serviço
start:
	@echo "$(BLUE)🚀 Iniciando serviço...$(NC)"
	@sudo systemctl enable $(SERVICE_NAME)
	@sudo systemctl start $(SERVICE_NAME)
	@echo "$(GREEN)✅ Serviço iniciado$(NC)"

# Parar serviço
stop:
	@echo "$(BLUE)🛑 Parando serviço...$(NC)"
	@sudo systemctl stop $(SERVICE_NAME)
	@echo "$(GREEN)✅ Serviço parado$(NC)"

# Reiniciar serviço
restart:
	@echo "$(BLUE)🔄 Reiniciando serviço...$(NC)"
	@sudo systemctl restart $(SERVICE_NAME)
	@echo "$(GREEN)✅ Serviço reiniciado$(NC)"

# Ver status
status:
	@echo "$(BLUE)📊 Status do serviço:$(NC)"
	@sudo systemctl status $(SERVICE_NAME) --no-pager

# Ver logs
logs:
	@echo "$(BLUE)📋 Logs do serviço (Ctrl+C para sair):$(NC)"
	@sudo journalctl -u $(SERVICE_NAME) -f --no-pager

# Executar testes
test:
	@echo "$(BLUE)🧪 Executando testes...$(NC)"
	@python3 tests/teste_temporadas.py
	@echo "$(GREEN)✅ Testes concluídos$(NC)"

# Limpar arquivos temporários
clean:
	@echo "$(BLUE)🧹 Limpando arquivos temporários...$(NC)"
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.log" -delete 2>/dev/null || true
	@find . -name "*.tmp" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída$(NC)"

# Preparar build
build:
	@echo "$(BLUE)🔨 Preparando build...$(NC)"
	@$(MAKE) clean
	@$(MAKE) check-config
	@echo "$(GREEN)✅ Build preparado$(NC)"

# Deploy completo
deploy: build install start
	@echo "$(BLUE)🚀 Deploy completo realizado!$(NC)"
	@$(MAKE) status
	@echo ""
	@echo "$(GREEN)🎉 Sistema está funcionando!$(NC)"
	@echo "$(CYAN)Use 'make logs' para monitorar$(NC)"

# Configurar ambiente de desenvolvimento
dev-setup:
	@echo "$(BLUE)🛠️  Configurando ambiente de desenvolvimento...$(NC)"
	@$(MAKE) install-deps
	@$(MAKE) check-config
	@echo "$(GREEN)✅ Ambiente de desenvolvimento configurado$(NC)"

# Backup da configuração
backup:
	@echo "$(BLUE)💾 Fazendo backup da configuração...$(NC)"
	@sudo tar -czf /tmp/$(SERVICE_NAME)-backup-$$(date +%Y%m%d-%H%M%S).tar.gz $(INSTALL_DIR)
	@echo "$(GREEN)✅ Backup criado em /tmp/$(NC)"

# Atualizar sistema
update: stop
	@echo "$(BLUE)🔄 Atualizando sistema...$(NC)"
	@$(MAKE) copy-files
	@$(MAKE) start
	@echo "$(GREEN)✅ Sistema atualizado$(NC)"

# Verificar saúde do sistema
health:
	@echo "$(BLUE)🏥 Verificando saúde do sistema...$(NC)"
	@$(MAKE) status
	@echo ""
	@echo "$(BLUE)Últimas 5 linhas do log:$(NC)"
	@sudo tail -n 5 /var/log/$(SERVICE_NAME).log 2>/dev/null || echo "$(YELLOW)Log não encontrado$(NC)"
	@echo ""
	@echo "$(BLUE)Uso de disco:$(NC)"
	@df -h $(INSTALL_DIR) 2>/dev/null || echo "$(YELLOW)Diretório não encontrado$(NC)"

# Informações do sistema
info:
	@echo "$(BLUE)ℹ️  Informações do sistema:$(NC)"
	@echo "  Projeto: $(PROJECT_NAME)"
	@echo "  Versão: $(VERSION)"
	@echo "  Diretório: $(INSTALL_DIR)"
	@echo "  Serviço: $(SERVICE_NAME)"
	@echo "  Usuário: $$(whoami)"
	@echo "  Sistema: $$(uname -a)"
	@echo "  Python: $$(python3 --version)"

# Validar instalação
validate:
	@echo "$(BLUE)✅ Validando instalação...$(NC)"
	@test -d $(INSTALL_DIR) || { echo "$(RED)❌ Diretório não encontrado$(NC)"; exit 1; }
	@test -f $(INSTALL_DIR)/auto_organize_anime.py || { echo "$(RED)❌ Script principal não encontrado$(NC)"; exit 1; }
	@test -f $(BIN_DIR)/organize-anime || { echo "$(RED)❌ CLI não encontrado$(NC)"; exit 1; }
	@systemctl is-enabled $(SERVICE_NAME) >/dev/null 2>&1 || { echo "$(RED)❌ Serviço não habilitado$(NC)"; exit 1; }
	@echo "$(GREEN)✅ Instalação válida$(NC)"

# Comandos Docker
docker-build:
	@echo "$(BLUE)🐳 Construindo imagem Docker...$(NC)"
	@docker build -t $(PROJECT_NAME):$(VERSION) -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✅ Imagem Docker construída$(NC)"

docker-run:
	@echo "$(BLUE)🐳 Executando container Docker...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✅ Container iniciado$(NC)"

docker-stop:
	@echo "$(BLUE)🐳 Parando container Docker...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✅ Container parado$(NC)"

docker-logs:
	@echo "$(BLUE)🐳 Logs do container Docker:$(NC)"
	@docker-compose logs -f $(PROJECT_NAME)

docker-deploy: docker-build docker-run
	@echo "$(BLUE)🐳 Deploy Docker completo realizado!$(NC)"
	@$(MAKE) docker-logs

# Limpeza Docker
docker-clean:
	@echo "$(BLUE)🐳 Limpando recursos Docker...$(NC)"
	@docker-compose down --volumes --remove-orphans
	@docker image prune -f
	@docker volume prune -f
	@echo "$(GREEN)✅ Limpeza Docker concluída$(NC)"

# Build multi-arquitetura
docker-buildx:
	@echo "$(BLUE)🐳 Construindo imagem multi-arquitetura...$(NC)"
	@docker buildx build --platform linux/amd64,linux/arm64 -t $(PROJECT_NAME):$(VERSION) -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✅ Imagem multi-arquitetura construída$(NC)"
