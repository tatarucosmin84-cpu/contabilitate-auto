"""
updater.py — Sistem de actualizare automata ContabilitateAuto
"""

import urllib.request
import urllib.error
import json
import os
import shutil

GITHUB_USER   = "tatarucosmin84-cpu"
GITHUB_REPO   = "contabilitate-auto"
GITHUB_BRANCH = "main"

GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"

FOLDER_APP = r"C:\ContabilitateAuto"

FISIERE_ACTUALIZABILE = {
    "version.json":              r"C:\ContabilitateAuto\version.json",
    "app/dashboard_multi.py":    r"C:\ContabilitateAuto\app\dashboard_multi.py",
    "app/vizualizeaza_fisa.py":  r"C:\ContabilitateAuto\app\vizualizeaza_fisa.py",
    "app/database.py":           r"C:\ContabilitateAuto\app\database.py",
    "app/modules/fisa_platitor.py": r"C:\ContabilitateAuto\app\modules\fisa_platitor.py",
    "app/modules/pdf_reader.py":    r"C:\ContabilitateAuto\app\modules\pdf_reader.py",
    "app/modules/updater.py":       r"C:\ContabilitateAuto\app\modules\updater.py",
}

def citeste_versiune_locala():
    cale = os.path.join(FOLDER_APP, "version.json")
    try:
        with open(cale, "r", encoding="utf-8") as f:
            return json.load(f).get("versiune", "0.0.0")
    except Exception:
        return "0.0.0"

def citeste_versiune_remote():
    url = f"{GITHUB_RAW}/version.json"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            date = json.loads(r.read().decode("utf-8"))
            return date.get("versiune", "0.0.0"), date.get("descriere", "")
    except urllib.error.URLError:
        return None, "Nu exista conexiune la internet."
    except Exception as e:
        return None, f"Eroare: {e}"

def compara_versiuni(v_locala, v_remote):
    try:
        return tuple(int(x) for x in v_remote.split(".")) > \
               tuple(int(x) for x in v_locala.split("."))
    except Exception:
        return False

def descarca_fisier(cale_github, cale_locala):
    url = f"{GITHUB_RAW}/{cale_github}"
    cale_backup = cale_locala + ".backup"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            continut = r.read()
        if os.path.exists(cale_locala):
            shutil.copy2(cale_locala, cale_backup)
        os.makedirs(os.path.dirname(cale_locala), exist_ok=True)
        with open(cale_locala, "wb") as f:
            f.write(continut)
        return True
    except Exception as e:
        if os.path.exists(cale_backup):
            shutil.copy2(cale_backup, cale_locala)
        print(f"  Eroare la {cale_github}: {e}")
        return False

def sterge_backup_uri():
    for _, cale in FISIERE_ACTUALIZABILE.items():
        bk = cale + ".backup"
        if os.path.exists(bk):
            try: os.remove(bk)
            except: pass

def restaureaza_backup_uri():
    for _, cale in FISIERE_ACTUALIZABILE.items():
        bk = cale + ".backup"
        if os.path.exists(bk):
            try:
                shutil.copy2(bk, cale)
                os.remove(bk)
            except: pass

def ruleaza_update(callback_progres=None):
    def log(mesaj):
        if callback_progres:
            callback_progres(mesaj)
        print(mesaj)

    log("Se verifica versiunea disponibila...")
    v_locala = citeste_versiune_locala()
    v_remote, descriere = citeste_versiune_remote()

    if v_remote is None:
        log(f"Eroare: {descriere}")
        return "eroare"

    log(f"Versiune instalata: {v_locala}")
    log(f"Versiune disponibila: {v_remote}")

    if not compara_versiuni(v_locala, v_remote):
        log("Softul este deja la versiunea cea mai noua!")
        return "la_zi"

    log(f"Versiune noua: {v_remote} — {descriere}")
    log("Se descarca actualizarile...")

    succes = True
    for cale_github, cale_locala in FISIERE_ACTUALIZABILE.items():
        log(f"  -> {cale_github}")
        if not descarca_fisier(cale_github, cale_locala):
            succes = False

    if succes:
        sterge_backup_uri()
        log(f"Actualizare la {v_remote} finalizata! Reporneste softul.")
        return "actualizat"
    else:
        restaureaza_backup_uri()
        log("Eroare. S-a restaurat versiunea anterioara.")
        return "eroare"

if __name__ == "__main__":
    print("=== Test Updater ===\n")
    print(ruleaza_update())
