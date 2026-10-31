"""
Avisos em tempo real (WebSocket) para todas as telas: quadro atualizado e
anúncios sonoros/visuais da TV da oficina (os textos falados ficam todos aqui).
"""
from .extensions import socketio
from .services.board import get_full_board


def broadcast_board():
    """Envia o quadro completo para todas as telas e o retorna."""
    board = get_full_board()
    socketio.emit("board_updated", board)
    return board


def _announce(payload):
    socketio.emit("tv_announcement", payload)


def announce_arrival(card, stage, intro="Atenção oficina."):
    _announce({
        "type": "new_arrival",
        "os_number": card["os_number"],
        "client_name": card["client_name"],
        "equipment_type": card["equipment_type"],
        "stage": stage,
        "is_urgent": card["is_urgent"] or card["is_warranty"],
        "tts_text": f"{intro} A O.S. {card['os_number']}, do cliente {card['client_name']}, chegou para {stage}."
    })


def announce_finished_on_board(card, actor, finished_today):
    """O.S. arrastada para FINALIZADAS pela recepção."""
    _announce({
        "type": "os_finished",
        "os_number": card["os_number"],
        "client_name": card["client_name"],
        "tech_name": card["tech_name"] or actor,
        "finished_today": finished_today,
        "tts_text": f"Excelente trabalho! O.S. {card['os_number']} do cliente {card['client_name']} foi finalizada por {card['tech_name'] or 'oficina'}!"
    })


def announce_finished_mobile(os_number, client_name, tech_name, inmetro_seal, finished_today):
    """O.S. finalizada pelo técnico no celular (QR Code)."""
    _announce({
        "type": "os_finished",
        "os_number": os_number,
        "client_name": client_name,
        "tech_name": tech_name,
        "inmetro_seal": inmetro_seal,
        "finished_today": finished_today,
        "tts_text": f"Serviço concluído! O técnico {tech_name} finalizou a O.S. {os_number} do cliente {client_name}."
    })


def announce_call_tech(tech_name, reason):
    _announce({
        "type": "call_alert",
        "title": "CHAMADO NA RECEPÇÃO",
        "tech_name": tech_name,
        "reason": reason,
        "is_urgent": True,
        "tts_text": f"Atenção {tech_name}. Por favor, comparecer na recepção. {reason}."
    })


def announce_director_call(tech_name, message="", is_urgent=False, audio_base64=None, sender="Sala da Diretoria"):
    """Chamado ou áudio enviado pelo chefe / sala da diretoria para a TV da oficina."""
    title = "🚨 CHAMADO URGENTE DA DIRETORIA" if is_urgent else "📢 CHAMADO DA DIRETORIA"
    clean_msg = (message or "").strip()
    if clean_msg:
        tts_text = f"Atenção {tech_name}. Mensagem da diretoria: {clean_msg}."
    else:
        tts_text = f"Atenção {tech_name}. Favor comparecer à sala da diretoria."

    _announce({
        "type": "director_call",
        "title": title,
        "tech_name": tech_name or "Oficina",
        "reason": clean_msg or "Comparecer à Sala da Diretoria",
        "is_urgent": bool(is_urgent),
        "tts_text": tts_text,
        "audio_base64": audio_base64,
        "sender": sender
    })


def announce_bench_support(tech_name, os_number):
    _announce({
        "type": "support_alert",
        "title": "APOIO SOLICITADO NA BANCADA",
        "tech_name": tech_name,
        "os_number": os_number,
        "is_urgent": True,
        "tts_text": f"Atenção oficina. {tech_name} solicita apoio técnico na bancada para a O.S. {os_number}."
    })


def announce_timer_done(os_number, client_name, label):
    _announce({
        "type": "timer_done",
        "os_number": os_number,
        "client_name": client_name,
        "label": label,
        "is_urgent": True,
        "tts_text": f"Atenção oficina! Tempo de {label} concluído para a O.S. {os_number}, cliente {client_name}. Retirar equipamento da estufa."
    })


def notify_timer_started(os_number, client_name, minutes, end_time, label):
    socketio.emit("timer_started", {
        "os_number": os_number,
        "client_name": client_name,
        "minutes": minutes,
        "end_time": end_time,
        "label": label
    })


def notify_tv_mute(muted):
    socketio.emit("tv_mute_changed", {"muted": muted})


def notify_admin(payload):
    """Envia uma notificação em tempo real para o painel Admin da Recepção (Priscila)."""
    socketio.emit("admin_notification", payload)


