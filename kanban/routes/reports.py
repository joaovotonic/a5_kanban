"""API de relatórios da gerência: métricas, exportação CSV e backup."""
from flask import Blueprint, Response, jsonify, request, send_file

from ..backup import perform_daily_backup
from ..services.board import get_analytics_summary
from ..services.reports import build_os_csv

bp = Blueprint("api_reports", __name__, url_prefix="/api")


@bp.route("/analytics", methods=["GET"])
def analytics():
    """Dados para o painel /gerencia."""
    return jsonify(get_analytics_summary())


@bp.route("/export/csv", methods=["GET"])
def export_csv():
    """Exporta relatório completo de O.S. para Excel (CSV UTF-8 com BOM)."""
    content, filename = build_os_csv(request.args.get("period", "all"))  # day, month, year, all
    return Response(
        content,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@bp.route("/backup/download", methods=["GET"])
def download_backup():
    """Gera um backup imediato e faz download do arquivo .db."""
    return send_file(perform_daily_backup(force=True), as_attachment=True)

