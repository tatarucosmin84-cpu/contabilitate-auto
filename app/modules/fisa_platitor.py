import sys
sys.path.insert(0, r'C:\ContabilitateAuto\app\modules')

import pdfplumber
import sqlite3
import os
import re
from datetime import datetime

DB_PATH = r"C:\ContabilitateAuto\data\contabilitate.db"

TIPURI_DATORII = {
    "taxa pe valoarea adaugata": "TVA",
    "obligatii fiscale accesorii aferente tva": "TVA_ACCESORII",
    "impozit pe profit": "PROFIT",
    "impozit pe veniturile microintreprinderilor": "MICRO",
    "impozit pe venitul microintreprinderilor": "MICRO",
    "contributia de asigurari sociale": "CAS",
    "contributia asiguratorie pentru munca": "CAM",
    "contributie asiguratorie pentru munca": "CAM",
    "impozit pe veniturile din salarii": "IMPOZIT_VENIT",
    "impozit pe venit": "IMPOZIT_VENIT",
    "contributia pentru asigurari de sanatate": "CASS",
    "contributia individuala de asigurari sociale": "CAS_IND",
    "impozit pe dividende": "DIVIDENDE",
    "penalitati de nedeclarare": "PENALITATI",
    "venituri din amenzi": "AMENZI",
    "venituri ale bugetului": "VENITURI_BUGET",
    "sume incasate pentru bugetul": "SUME_BUGET",
}

def identifica_tip(text):
    if not text:
        return None
    t = text.lower().strip()
    for cheie, tip in TIPURI_DATORII.items():
        if cheie in t:
            return tip
    return None

def parse_numar(text):
    if not text:
        return 0.0
    text = str(text).strip().replace(' ', '').replace(',', '.')
    text = re.sub(r'[^\d.\-]', '', text)
    if not text or text == '-':
        return 0.0
    try:
        return float(text)
    except:
        return 0.0

def extrage_info_firma(linii):
    info = {"cif": None, "denumire": None, "data_calcul": None}
    for i, linie in enumerate(linii[:20]):
        m = re.search(r'Cod de identificare fiscala[:\s]+(\d{6,10})', linie, re.IGNORECASE)
        if m:
            info["cif"] = m.group(1)
            if i + 1 < len(linii):
                info["denumire"] = linii[i + 1].strip()
        m = re.search(r'Calcul accesorii pana la data de\s*:(\d{2}/\d{2}/\d{4})', linie, re.IGNORECASE)
        if m:
            info["data_calcul"] = m.group(1)
    return info

PATTERN_CATEGORIE = re.compile(r'^(\d{1,5})\s+([A-ZĂÎȘȚÂ][^\d\n]{8,})$')

PATTERN_TOTAL = re.compile(
    r'^Total impozit:\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)'
)

PATTERN_TOTAL_GENERAL = re.compile(
    r'^Total cod fiscal:\s+\d+\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)'
)

def proceseaza_fisa(cale_fisier):
    print(f"\n🔍 Procesez: {os.path.basename(cale_fisier)}")
    print("-" * 60)

    if not os.path.exists(cale_fisier):
        print("❌ Fișierul nu există")
        return None

    text_total = ""
    try:
        with pdfplumber.open(cale_fisier) as pdf:
            for pagina in pdf.pages:
                text_total += (pagina.extract_text() or "") + "\n"
    except Exception as e:
        print(f"❌ Eroare citire PDF: {e}")
        return None

    linii = text_total.split('\n')
    print(f"📄 Total linii: {len(linii)}")

    info_firma = extrage_info_firma(linii)
    print(f"🏢 Firmă:       {info_firma['denumire']}")
    print(f"📋 CIF:         {info_firma['cif']}")
    print(f"📅 Data calcul: {info_firma['data_calcul']}")

    categorii = {}
    ordine = []
    categorie_curenta = None
    total_general_pdf = None

    for linie in linii:
        linie = linie.strip()
        if not linie:
            continue

        # --- Total general al fișei (ultima linie importantă) ---
        m_gen = PATTERN_TOTAL_GENERAL.match(linie)
        if m_gen:
            nums = [parse_numar(m_gen.group(i)) for i in range(1, 8)]
            total_general_pdf = {
                "obligatie": nums[0],
                "neachitata": nums[1],
                "dobanda": nums[2],
                "penalitati": nums[3],
                "incasari": nums[4],
                "rambursari": nums[5],
                "credit": nums[6]
            }
            continue

        # --- Total per categorie ---
        m_total = PATTERN_TOTAL.match(linie)
        if m_total and categorie_curenta:
            nums = [parse_numar(m_total.group(i)) for i in range(1, 8)]
            # pozitii: obligatie, neachitata, dobanda, penalitati, incasari, rambursari, credit
            c = categorii[categorie_curenta]
            # Acumulăm (categoria poate apărea pe mai multe pagini)
            c["obligatie"]  += nums[0]
            c["neachitata"] += nums[1]
            c["dobanda"]    += nums[2]
            c["penalitati"] += nums[3]
            c["incasari"]   += nums[4]
            c["rambursari"] += nums[5]
            c["credit"]     += nums[6]
            c["are_total"]   = True
            continue

        # --- Antet categorie: ex. "1 Taxa pe valoarea adaugata" ---
        m_cat = PATTERN_CATEGORIE.match(linie)
        if m_cat:
            denumire = m_cat.group(2).strip()
            # Ignoră capete de tabel
            if any(x in denumire for x in ['Document', 'Scadenta', 'Obligatie', 'Atribut', 'Termen']):
                continue
            # Ignoră dacă prea multe cifre față de litere
            if len(re.findall(r'\d', denumire)) > len(re.findall(r'[a-zA-Z]', denumire)):
                continue

            if denumire not in categorii:
                categorii[denumire] = {
                    "cod": m_cat.group(1),
                    "denumire": denumire,
                    "tip": identifica_tip(denumire),
                    "obligatie": 0.0,
                    "neachitata": 0.0,
                    "dobanda": 0.0,
                    "penalitati": 0.0,
                    "incasari": 0.0,
                    "rambursari": 0.0,
                    "credit": 0.0,
                    "are_total": False,
                }
                ordine.append(denumire)
            categorie_curenta = denumire
            continue

    # ============================================
    # AFIȘARE REZULTATE
    # ============================================
    print(f"\n💰 Categorii fiscale găsite: {len(categorii)}")
    print(f"{'─'*75}")
    print(f"  {'Categorie':<46} {'Neachitat':>10} {'Credit':>10}")
    print(f"{'─'*75}")

    total_neachitat = 0.0
    total_credit    = 0.0
    datorii = []

    for denumire in ordine:
        c = categorii[denumire]
        neachitat = c["neachitata"]
        credit    = c["credit"]

        total_neachitat += neachitat
        total_credit    += credit

        if neachitat > 0:
            col_neachitat = f"🔴 {neachitat:>8,.0f}"
        else:
            col_neachitat = f"⚪  {neachitat:>7,.0f}"

        if credit > 0:
            col_credit = f"🟢 {credit:>8,.0f}"
        else:
            col_credit = f"   {credit:>8,.0f}"

        print(f"  {denumire[:46]:<46} {col_neachitat} {col_credit}")

        datorii.append({
            "denumire": denumire,
            "cod": c["cod"],
            "tip": c["tip"] or "NECUNOSCUT",
            "recunoscut": c["tip"] is not None,
            "obligatie": c["obligatie"],
            "neachitata": neachitat,
            "dobanda": c["dobanda"],
            "penalitati": c["penalitati"],
            "incasari": c["incasari"],
            "credit": credit,
            "sold": neachitat
        })

    print(f"{'─'*75}")
    print(f"  🔴 TOTAL NEACHITAT:    {total_neachitat:>10,.2f} RON")
    print(f"  🟢 TOTAL CREDIT:       {total_credit:>10,.2f} RON")

    sold_net = total_neachitat - total_credit
    if sold_net > 0:
        print(f"  ⚠️  SOLD NET DE PLATĂ: {sold_net:>10,.2f} RON")
    elif sold_net < 0:
        print(f"  ✅ SOLD NET CREDIT:   {sold_net:>10,.2f} RON")
    else:
        print(f"  ✅ BALANȚĂ ZERO:      {sold_net:>10,.2f} RON")
    print(f"{'─'*75}")

    if total_general_pdf:
        print(f"\n📊 CONFIRMARE DIN PDF (Total cod fiscal):")
        print(f"   Neachitat: {total_general_pdf['neachitata']:,.0f} RON")
        print(f"   Credit:    {total_general_pdf['credit']:,.0f} RON")

    return {
        "firma": info_firma,
        "datorii": datorii,
        "total": sold_net,
        "total_neachitat": total_neachitat,
        "total_credit": total_credit,
        "cale_fisier": cale_fisier,
        "data_import": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def salveaza_in_db(rezultat):
    if not rezultat:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cif = rezultat['firma']['cif']
    denumire = rezultat['firma']['denumire']
    if not cif:
        print("❌ CIF negăsit")
        conn.close()
        return
    cursor.execute("INSERT OR IGNORE INTO societati (cui, denumire) VALUES (?, ?)",
                   (cif, denumire or "Necunoscut"))
    cursor.execute("SELECT id FROM societati WHERE cui = ?", (cif,))
    societate_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM fisa_platitor WHERE societate_id = ? AND cale_fisier = ?",
                   (societate_id, rezultat['cale_fisier']))
    for d in rezultat['datorii']:
        cursor.execute("""
            INSERT INTO fisa_platitor
            (societate_id, denumire_datorie, suma_datorata, sold, data_fisa, cale_fisier)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (societate_id, d['denumire'], d['obligatie'], d['sold'],
              rezultat['firma']['data_calcul'], rezultat['cale_fisier']))
    conn.commit()
    conn.close()
    print(f"\n✅ Salvat în DB: {denumire} (CIF: {cif})")

if __name__ == "__main__":
    FOLDER = r'C:\Users\conta\OneDrive\TDEC\SPV TDEC\RALEX PROIECT CONSTRUCT SRL\2026.03\RASPUNS SOLICITARE'
    pdf_uri = sorted([f for f in os.listdir(FOLDER) if f.endswith('.pdf')], reverse=True)
    if pdf_uri:
        cale = os.path.join(FOLDER, pdf_uri[0])
        rezultat = proceseaza_fisa(cale)
        if rezultat:
            salveaza_in_db(rezultat)
    else:
        print("❌ Nu am găsit PDF-uri")
