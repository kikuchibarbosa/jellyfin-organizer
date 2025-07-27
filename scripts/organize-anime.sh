#!/bin/bash
SCRIPTS_DIR="/opt/anime-organizer"

case "$1" in
    "organize")
        echo "🔄 Organizando arquivos existentes..."
        python3 "$SCRIPTS_DIR/auto_organize_anime.py" organize
        ;;
    "start")
        echo "▶️ Iniciando serviço..."
        sudo systemctl start anime-organizer
        sudo systemctl status anime-organizer
        ;;
    "stop")
        echo "⏹️ Parando serviço..."
        sudo systemctl stop anime-organizer
        ;;
    "restart")
        echo "🔄 Reiniciando serviço..."
        sudo systemctl restart anime-organizer
        sudo systemctl status anime-organizer
        ;;
    "status")
        sudo systemctl status anime-organizer
        ;;
    "logs")
        sudo journalctl -u anime-organizer -f
        ;;
    "enable")
        echo "🔧 Habilitando serviço para iniciar automaticamente..."
        sudo systemctl enable anime-organizer
        sudo systemctl start anime-organizer
        ;;
    *)
        echo "Uso: organize-anime {organize|start|stop|restart|status|logs|enable}"
        echo ""
        echo "Comandos:"
        echo "  organize  - Organiza arquivos existentes"
        echo "  start     - Inicia o monitor"
        echo "  stop      - Para o monitor"
        echo "  restart   - Reinicia o monitor"
        echo "  status    - Mostra status do serviço"
        echo "  logs      - Mostra logs em tempo real"
        echo "  enable    - Habilita início automático"
        exit 1
        ;;
esac
