import sys
sys.path.insert(0, r'C:\ContabilitateAuto\app\modules')

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from fisa_platitor import proceseaza_fisa, salveaza_in_db

# ============================================================
# CALEA PDF — din argument (dashboard) sau ales manual
# ============================================================
PDF_DIN_ARGUMENT = sys.argv[1] if len(sys.argv) > 1 else None

FOLDER_DEFAULT = r'C:\Users\conta\OneDrive\TDEC\SPV TDEC\RALEX PROIECT CONSTRUCT SRL\2026.03\RASPUNS SOLICITARE'

# ============================================================
# LOGICĂ PRINCIPALĂ
# ============================================================

def deschide_fisier():
    """Butonul 'Deschide alt PDF' — selector manual"""
    cale = filedialog.askopenfilename(
        title="Selectează Fișa Sintetică PDF",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if cale:
        incarca_fisa(cale)


def incarca_fisa(cale_pdf):
    """Procesează PDF-ul și reconstruiește interfața"""
    global frame_continut

    if not os.path.exists(cale_pdf):
        messagebox.showerror("Eroare", f"Fișierul nu există:\n{cale_pdf}")
        return

    rezultat = proceseaza_fisa(cale_pdf)

    if not rezultat:
        messagebox.showerror("Eroare", f"Nu am putut procesa fișierul:\n{cale_pdf}")
        return

    try:
        salveaza_in_db(rezultat)
    except Exception:
        pass  # Continuăm chiar dacă salvarea în DB eșuează

    # Actualizăm titlul ferestrei
    denumire = rezultat['firma'].get('denumire', 'Necunoscut')
    cif = rezultat['firma'].get('cif', '')
    root.title(f"Fișă Sintetică — {denumire} (CIF: {cif})")

    # Ștergem conținutul vechi și reconstruim
    for widget in frame_continut.winfo_children():
        widget.destroy()

    construieste_tabel(frame_continut, rezultat, cale_pdf)


def construieste_tabel(container, rezultat, cale_pdf):
    """Construiește tabelul cu datele firmei"""

    datorii = rezultat.get('datorii', [])
    total_neachitat = rezultat.get('total_neachitat', 0)
    total_credit = rezultat.get('total_credit', 0)
    sold_net = total_neachitat - total_credit

    # ---- INFO FIRMĂ ----
    frame_info = tk.Frame(container, bg="#e8eaf6", pady=8)
    frame_info.pack(fill="x", padx=12, pady=(8, 4))

    denumire = rezultat['firma'].get('denumire', 'Necunoscut')
    cif = rezultat['firma'].get('cif', '—')
    data = rezultat['firma'].get('data_calcul', '—')

    tk.Label(frame_info, text=f"🏢  {denumire}",
             font=("Segoe UI", 11, "bold"), bg="#e8eaf6", fg="#1a237e").pack(side="left", padx=10)
    tk.Label(frame_info, text=f"CIF: {cif}  |  Data: {data}",
             font=("Segoe UI", 9), bg="#e8eaf6", fg="#555555").pack(side="left", padx=10)

    # Buton deschide PDF
    tk.Button(frame_info, text="📄 Deschide PDF",
              font=("Segoe UI", 9), bg="#1565c0", fg="white",
              relief="flat", padx=10, pady=3, cursor="hand2",
              command=lambda: os.startfile(cale_pdf)).pack(side="right", padx=10)

    # ---- TABEL ----
    frame_tabel = tk.Frame(container, bg="#f5f5f5")
    frame_tabel.pack(fill="both", expand=True, padx=12, pady=4)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
        font=("Segoe UI", 10), rowheight=28,
        background="#ffffff", fieldbackground="#ffffff", foreground="#222222")
    style.configure("Treeview.Heading",
        font=("Segoe UI", 10, "bold"), background="#e8eaf6", foreground="#1a237e")
    style.map("Treeview",
        background=[("selected", "#bbdefb")],
        foreground=[("selected", "#0d47a1")])

    columns = ("Categorie", "Tip", "Neachitat (RON)", "Credit (RON)")
    tree = ttk.Treeview(frame_tabel, columns=columns, show="headings", selectmode="browse")

    tree.heading("Categorie", text="Categorie Fiscală")
    tree.heading("Tip", text="Tip")
    tree.heading("Neachitat (RON)", text="Neachitat (RON)")
    tree.heading("Credit (RON)", text="Credit (RON)")

    tree.column("Categorie", width=340, anchor="w")
    tree.column("Tip", width=110, anchor="center")
    tree.column("Neachitat (RON)", width=140, anchor="e")
    tree.column("Credit (RON)", width=140, anchor="e")

    tree.tag_configure("cu_datorie",  background="#ffebee", foreground="#b71c1c")
    tree.tag_configure("cu_credit",   background="#e8f5e9", foreground="#1b5e20")
    tree.tag_configure("fara_datorie", background="#ffffff",  foreground="#222222")
    tree.tag_configure("necunoscut",   background="#fff3e0",  foreground="#e65100")
    tree.tag_configure("total",        background="#1a73e8",  foreground="#ffffff")

    for d in datorii:
        neachitat = d.get('neachitata', 0) or 0
        credit    = d.get('credit', 0) or 0

        ne_fmt = f"{neachitat:,.2f}" if neachitat != 0 else "0,00"
        cr_fmt = f"{credit:,.2f}"    if credit != 0    else "0,00"

        if not d.get('recunoscut', True):
            tag = "necunoscut"
        elif neachitat > 0:
            tag = "cu_datorie"
        elif credit > 0:
            tag = "cu_credit"
        else:
            tag = "fara_datorie"

        tree.insert("", "end", values=(
            d.get('denumire', '')[:55],
            d.get('tip', ''),
            ne_fmt,
            cr_fmt,
        ), tags=(tag,))

    # Rând TOTAL
    tree.tag_configure("total", background="#1a73e8", foreground="#ffffff")
    tree.insert("", "end", values=(
        "TOTAL",
        "",
        f"{total_neachitat:,.2f}" if total_neachitat else "0,00",
        f"{total_credit:,.2f}"    if total_credit    else "0,00",
    ), tags=("total",))

    scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # ---- FOOTER ----
    frame_footer = tk.Frame(container, bg="#1a73e8", pady=8)
    frame_footer.pack(fill="x", side="bottom")

    if sold_net > 0:
        text_sold = f"⚠️  SOLD NET DE PLATĂ: {sold_net:,.2f} RON"
        culoare_sold = "#ffcdd2"
    elif sold_net < 0:
        text_sold = f"✅ SOLD NET CREDIT: {abs(sold_net):,.2f} RON"
        culoare_sold = "#c8e6c9"
    else:
        text_sold = "✅ BALANȚĂ ZERO"
        culoare_sold = "white"

    tk.Label(frame_footer,
        text=(
            f"🔴  NEACHITAT: {total_neachitat:,.2f} RON"
            f"        🟢  CREDIT: {total_credit:,.2f} RON"
            f"        {text_sold}"
        ),
        font=("Segoe UI", 11, "bold"),
        bg="#1a73e8", fg=culoare_sold
    ).pack()


# ============================================================
# FEREASTRA PRINCIPALĂ
# ============================================================

root = tk.Tk()
root.title("Fișă Sintetică Simplificată ANAF")
root.geometry("800x620")
root.configure(bg="#f5f5f5")

# Bara de sus
frame_top = tk.Frame(root, bg="#e0e0e0", pady=6)
frame_top.pack(fill="x")

tk.Label(frame_top, text="📋 Fișă Sintetică Simplificată ANAF",
         font=("Segoe UI", 12, "bold"), bg="#e0e0e0").pack(side="left", padx=12)

tk.Button(frame_top, text="📂 Deschide alt PDF",
          font=("Segoe UI", 10), bg="#1a73e8", fg="white",
          relief="flat", padx=10, pady=3, cursor="hand2",
          command=deschide_fisier).pack(side="right", padx=12)

# Frame conținut (global — modificat la fiecare încărcare)
frame_continut = tk.Frame(root, bg="#f5f5f5")
frame_continut.pack(fill="both", expand=True)

# Mesaj inițial
tk.Label(frame_continut,
    text="Apasă '📂 Deschide alt PDF' pentru a încărca o fișă sintetică.",
    font=("Segoe UI", 11), bg="#f5f5f5", fg="#888888"
).pack(expand=True)

# ============================================================
# AUTO-ÎNCĂRCARE LA PORNIRE
# ============================================================

def auto_incarca():
    if PDF_DIN_ARGUMENT and os.path.exists(PDF_DIN_ARGUMENT):
        # Venit din dashboard cu argument explicit
        incarca_fisa(PDF_DIN_ARGUMENT)
    elif os.path.exists(FOLDER_DEFAULT):
        # Fallback pe folderul default (RALEX)
        pdf_uri = sorted(
            [f for f in os.listdir(FOLDER_DEFAULT) if f.lower().endswith('.pdf')],
            reverse=True
        )
        if pdf_uri:
            incarca_fisa(os.path.join(FOLDER_DEFAULT, pdf_uri[0]))

root.after(200, auto_incarca)
root.mainloop()
