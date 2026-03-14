import pdfplumber
import fitz  # PyMuPDF
import os

def citeste_pdf_text(cale_fisier):
    """
    Încearcă să citească textul din PDF.
    Mai întâi cu pdfplumber (PDF-uri normale).
    Dacă nu găsește text, folosește PyMuPDF.
    """
    if not os.path.exists(cale_fisier):
        print(f"❌ Fișierul nu există: {cale_fisier}")
        return None

    # Metoda 1: pdfplumber (pentru PDF-uri cu text)
    try:
        with pdfplumber.open(cale_fisier) as pdf:
            text_total = ""
            for pagina in pdf.pages:
                text = pagina.extract_text()
                if text:
                    text_total += text + "\n"

            if text_total.strip():
                print(f"✅ Citit cu pdfplumber: {os.path.basename(cale_fisier)}")
                return text_total
    except Exception as e:
        print(f"⚠️ pdfplumber a eșuat: {e}")

    # Metoda 2: PyMuPDF (fallback)
    try:
        doc = fitz.open(cale_fisier)
        text_total = ""
        for pagina in doc:
            text_total += pagina.get_text() + "\n"
        doc.close()

        if text_total.strip():
            print(f"✅ Citit cu PyMuPDF: {os.path.basename(cale_fisier)}")
            return text_total
    except Exception as e:
        print(f"⚠️ PyMuPDF a eșuat: {e}")

    print(f"❌ Nu s-a putut citi textul din: {os.path.basename(cale_fisier)}")
    return None


def citeste_tabel_pdf(cale_fisier):
    """
    Extrage tabele din PDF (util pentru vectorul fiscal).
    Returnează o listă de tabele, fiecare tabel = listă de rânduri.
    """
    if not os.path.exists(cale_fisier):
        print(f"❌ Fișierul nu există: {cale_fisier}")
        return None

    try:
        tabele = []
        with pdfplumber.open(cale_fisier) as pdf:
            for nr_pagina, pagina in enumerate(pdf.pages, 1):
                tabel = pagina.extract_table()
                if tabel:
                    tabele.append({
                        "pagina": nr_pagina,
                        "date": tabel
                    })

        if tabele:
            print(f"✅ Am găsit {len(tabele)} tabel(e) în fișier")
            return tabele
        else:
            print("⚠️ Nu s-au găsit tabele în PDF")
            return None

    except Exception as e:
        print(f"❌ Eroare la extragere tabel: {e}")
        return None


def afiseaza_preview(cale_fisier, nr_caractere=500):
    """
    Afișează primele N caractere din PDF.
    Util pentru a vedea rapid ce conține un fișier.
    """
    text = citeste_pdf_text(cale_fisier)
    if text:
        print("\n" + "="*50)
        print(f"📄 Preview: {os.path.basename(cale_fisier)}")
        print("="*50)
        print(text[:nr_caractere])
        print("="*50 + "\n")
    return text


# ============================================
# TEST — rulează direct acest fișier pentru a testa
# ============================================
if __name__ == "__main__":
    print("🔍 Test modul pdf_reader")
    print("-" * 40)

    # Schimbă această cale cu un PDF real de pe calculatorul tău
    PDF_TEST = r"C:\calea\catre\un\fisier.pdf"

    if os.path.exists(PDF_TEST):
        afiseaza_preview(PDF_TEST)
    else:
        print("⚠️  Modifică variabila PDF_TEST cu calea unui PDF real de la tine")
        print("    Exemplu: PDF_TEST = r'C:\\Users\\conta\\Desktop\\test.pdf'")
