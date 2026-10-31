"""
Ponto de entrada do Sistema Kanban Local - A5 Tecnologia (Toledo Prix).

Execute:  python app.py

Todo o código fica no pacote `kanban/` (veja kanban/__init__.py para o mapa dos arquivos).
"""
from kanban import create_app
from kanban import database as db
from kanban.config import PORT
from kanban.extensions import socketio
from kanban.utils import get_local_ip

app = create_app()


if __name__ == "__main__":
    db.init_db()
    local_ip = get_local_ip()
    print("=" * 68)
    print("  SISTEMA KANBAN LOCAL - A5 TECNOLOGIA (TOLEDO PRIX)")
    print("=" * 68)
    print(f"  [RECEPÇÃO / PRISCILA] -> http://localhost:{PORT}/admin")
    print(f"  [PAINEL TV OFICINA]   -> http://{local_ip}:{PORT}/painel-tv")
    print(f"  [BANCADA MOBILE QR]   -> http://{local_ip}:{PORT}/saida")
    print(f"  [CONSULTA BALCÃO]     -> http://{local_ip}:{PORT}/consulta")
    print(f"  [GERÊNCIA / RELATÓRIO]-> http://{local_ip}:{PORT}/gerencia")
    print(f"  [FOTOS RECEPÇÃO]      -> http://{local_ip}:{PORT}/recepcao-fotos")
    print("=" * 68)

    socketio.run(app, host="0.0.0.0", port=PORT, debug=False, allow_unsafe_werkzeug=True)
