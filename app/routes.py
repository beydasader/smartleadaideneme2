from flask import Blueprint, jsonify, render_template, request
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service

pages = Blueprint("pages", __name__)
api = Blueprint("api", __name__)

@pages.route("/")
def home():
    return render_template("index.html")

@pages.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@api.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json()
    if not data or not data.get("mesaj"):
        return jsonify({"basari": False, "hata": "Mesaj gerekli."}), 400
    try:
        cevap = ai_service.yanit_uret(data["mesaj"], data.get("gecmis", []))
        return jsonify({"basari": True, "cevap": cevap}), 200
    except Exception as hata:
        # Hatanın gerçek sebebini Wix'e gönderecek kısım
        return jsonify({"basari": False, "hata": str(hata)}), 500

@api.route("/leads", methods=["POST"])
def lead_kaydet():
    data = request.get_json()
    if not data:
        return jsonify({"basari": False, "hata": "Veri gönderilmedi."}), 400
    
    isim = data.get("isim")
    email = data.get("email")
    mesaj = data.get("mesaj", "")

    if not isim or not email:
        return jsonify({"basari": False, "hata": "İsim ve email zorunludur."}), 400
    
    try:
        lead_ekle(isim, email, mesaj)
        return jsonify({"basari": True, "mesaj": "Kayıt başarıyla oluşturuldu."}), 201
    except Exception as hata:
        return jsonify({"basari": False, "hata": "Kayıt sırasında hata oluştu."}), 500

@api.route("/leads", methods=["GET"])
def leadleri_getir():
    try:
        leads = tum_leadler()
        liste = []
        for lead in leads:
            liste.append({
                "id": lead["id"],
                "isim": lead["isim"],
                "email": lead["email"],
                "mesaj": lead["mesaj"],
                "tarih": lead["tarih"]
            })
        return jsonify({"basari": True, "leadler": liste}), 200
    except Exception as hata:
        return jsonify({"basari": False, "hata": "Lead kayıtları alınamadı."}), 500

