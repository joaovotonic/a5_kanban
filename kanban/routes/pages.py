"""Rotas de páginas web (telas do sistema)."""
from flask import Blueprint, redirect, render_template, request, url_for

from ..config import PORT
from ..services.board import enrich_card
from ..services.cards import get_card_row_by_os
from ..utils import get_local_ip

bp = Blueprint("pages", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    """Redireciona a raiz para o painel da recepção."""
    return redirect(url_for("pages.admin_page"))


@bp.route("/admin")
def admin_page():
    """1. Rota Admin / Recepção (Operado pela Priscila)."""
    return render_template("admin.html", local_ip=get_local_ip(), port=PORT)


@bp.route("/painel-tv")
def tv_page():
    """2. Rota TV Oficina (Dashboard Visual e Sonoro Dark Mode Glassmorphism)."""
    return render_template("tv.html", local_ip=get_local_ip(), port=PORT)


@bp.route("/saida")
def saida_page():
    """3. Rota Bancada Mobile (Acessada via QR Code pelos celulares dos técnicos)."""
    os_num = request.args.get("os", "").strip()
    return render_template("saida.html", os_number=os_num, local_ip=get_local_ip())


@bp.route("/recepcao-fotos")
def recepcao_fotos_page():
    """Rota Mobile da Recepção (Priscila) para tirar fotos antes de gerar a O.S. no Teorema."""
    return render_template("recepcao_fotos.html", local_ip=get_local_ip(), port=PORT)


@bp.route("/consulta")
def consulta_page():
    """4. Rota Consulta Rápida (Para balcão e vendedores, sem permissão de edição)."""
    return render_template("consulta.html")


@bp.route("/gerencia")
def gerencia_page():
    """5. Rota Gerência & Histórico (Métricas, gráficos, ranking e backups)."""
    return render_template("gerencia.html")


@bp.route("/diretoria")
@bp.route("/chamado")
def diretoria_page():
    """6. Rota Intercom do Sr. Jacson (Para o Sr. Jacson chamar a equipe na TV com áudio e voz)."""
    return render_template("diretoria.html", local_ip=get_local_ip(), port=PORT)


@bp.route("/apresentacao")
def apresentacao_page():
    """7. Apresentação Executiva Comercial do Sistema A5 Kanban para o Sr. Jacson."""
    return render_template("apresentacao.html", local_ip=get_local_ip(), port=PORT)


@bp.route("/etiqueta/<path:os_number>")
def etiqueta_page(os_number):
    """Gera a visualização de impressão térmica 60x40mm com QR Code da O.S."""
    row = get_card_row_by_os(os_number)
    if not row:
        return "Ordem de Serviço não encontrada.", 404

    card = enrich_card(row)
    qr_url = f"http://{get_local_ip()}:{PORT}/saida?os={card['os_number']}"
    return render_template("etiqueta.html", card=card, qr_url=qr_url)


@bp.route("/folha/<path:os_number>")
def folha_page(os_number):
    """Visualização/impressão da Folha Digital de Orçamento e Serviço (espelho da folha física)."""
    row = get_card_row_by_os(os_number)
    if not row:
        return "Ordem de Serviço não encontrada.", 404

    card = enrich_card(row)
    return render_template("folha.html", card=card)

