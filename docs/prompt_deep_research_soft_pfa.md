# Prompt pentru Gemini Deep Research — Cum funcționează un soft de contabilitate pentru PFA

> Copiază tot ce este sub linia de mai jos și lipește în Gemini Deep Research.

---

Acționează ca un arhitect de software specializat în aplicații de contabilitate și fiscalitate din România, cu experiență în integrări ANAF. Pregătesc un raport de cercetare aprofundat, în limba română, despre **cum funcționează un soft de contabilitate pentru PFA (Persoană Fizică Autorizată), II și IF din România**, cu toate conexiunile externe, bune practici, „tips and tricks” și un dashboard pentru clienți.

## Context despre mine

Sunt contabil, învăț programare și dezvolt o aplicație desktop în Python (Tkinter, SQLite) numită „ContabilitateAuto”. Aplicația citește deja PDF-uri cu fișa sintetică a plătitorului descărcate din SPV (Spațiul Privat Virtual), extrage vectorul fiscal, verifică declarațiile depuse (D212, D100, D300, D390, D205 etc.) și afișează un dashboard multi-client. Vreau să înțeleg cum arată un soft complet pentru PFA ca să știu ce să construiesc mai departe și în ce ordine. Explică conceptele tehnice simplu, pentru cineva care nu este programator de meserie, dar fără să omiți detaliile importante.

## Ce vreau să afli (structurează raportul pe aceste secțiuni)

### 1. Contabilitatea PFA în România — regulile pe care softul trebuie să le implementeze
- Contabilitate în partidă simplă (OMFP 170/2015): Registrul-jurnal de încasări și plăți, Registrul-inventar, Registrul de evidență fiscală.
- Sistem real vs. normă de venit: ce se calculează diferit, ce registre sunt obligatorii în fiecare caz.
- Cheltuieli deductibile integral, limitat (ex. protocol, sponsorizare, mașină 50%) și nedeductibile, cu referințe la Codul fiscal actualizat la zi.
- Calculul impozitului pe venit (10%), CAS și CASS pentru PFA, inclusiv plafoanele raportate la salariul minim brut pe anul curent și anul următor. Verifică care sunt cele mai recente modificări legislative (2025-2026) și semnalează ce s-a schimbat.
- Declarația Unică (D212): secțiunile, termenele, estimare vs. definitivare, cum se calculează automat sumele din registrul de încasări și plăți.
- PFA plătitor de TVA: când devine obligatoriu, D300, D390, D394, jurnalele de vânzări și cumpărări, TVA la încasare.
- Amortizarea mijloacelor fixe la PFA și Registrul-inventar.

### 2. Toate conexiunile (integrările) pe care le poate avea un soft pentru PFA
Pentru fiecare integrare descrie: ce face, cum se autentifică, ce API sau format de fișier folosește, ce este oficial documentat de autorități, ce limitări are, și dacă există biblioteci open source (de preferat Python) care o implementează.
- **SPV / ANAF**: descărcare fișă sintetică, notificări, recipise. Există acces programatic sau doar descărcare manuală?
- **e-Factura (RO e-Factura)**: API-ul ANAF (OAuth2, certificat digital calificat, token de acces, mediu de test vs. producție), formatul XML UBL 2.1 / CIUS-RO, validare, trimitere, descărcare facturi primite, obligativitatea pentru PFA. Caută biblioteci Python existente.
- **e-TVA, e-Transport, SAF-T (D406)**: se aplică PFA-urilor? Când?
- **Validatoare ANAF (DUKIntegrator)** și semnarea PDF-urilor inteligente ale declarațiilor pentru depunere.
- **Extrase bancare**: import CSV / MT940 / camt.053 de la băncile din România; există Open Banking (PSD2) accesibil pentru un soft mic? Ce agregatori există (ex. Salt Edge, GoCardless/Nordigen, Smart Fintech, Finqware) și ce costă.
- **Case de marcat electronice** și raportarea la ANAF, dacă este relevantă.
- **Verificarea partenerilor**: serviciul web ANAF de interogare CUI/TVA (webservice public), REGES, ONRC, lista contribuabililor inactivi, registrul TVA la încasare.
- **Cursul valutar BNR** (XML public) pentru facturi în valută.
- **Email** (trimitere facturi, notificări de termene) și **stocare în cloud** (Google Drive, OneDrive) — menționează problemele de sincronizare a bazei de date SQLite pe OneDrive.
- **Export către contabilitate în partidă dublă** (SAGA, Smartbill, Ciel) pentru cazul în care clientul trece la SRL.

### 3. Cum arată softurile existente din România pentru PFA (analiză comparativă)
- Compară cel puțin: SmartBill, Keez, FGO, Oblio, Facturis, Contzilla, SAGA PS, Ciel, Pluxee/alte soluții, plus programe gratuite sau open source.
- Pentru fiecare: ce funcții au pentru PFA, prețuri, ce integrări oferă, ce le lipsește, ce spun utilizatorii în recenzii (puncte slabe repetate).
- Identifică nișe neacoperite unde un soft nou, construit de un contabil, ar putea aduce valoare.

### 4. Dashboard pentru clienți — ce trebuie să vadă un PFA și ce trebuie să vadă contabilul
- **Vedere contabil (multi-client)**: termene scadente pe toate firmele, declarații lipsă, obligații neachitate din fișa sintetică, alerte de risc (depășire plafon TVA, plafon CASS, inactivitate), status e-Factura.
- **Vedere client (PFA)**: venituri și cheltuieli pe lună, profit estimat, impozit/CAS/CASS estimate pentru anul curent, „cât mai pot încasa până la următorul plafon”, facturi neîncasate, documente de trimis contabilului.
- Ce indicatori (KPI) și ce grafice folosesc produsele de top; exemple de design bun; ce greșeli de UX sunt frecvente.
- Opțiuni tehnice pentru a oferi clienților acces: aplicație desktop vs. portal web (ex. Flask/FastAPI + o bază de date comună) vs. rapoarte PDF trimise automat pe email. Avantaje, dezavantaje, costuri și complexitate pentru fiecare, ținând cont că pornesc de la o aplicație desktop Python.

### 5. Arhitectură și bune practici tehnice („tips and tricks”)
- Cum se organizează corect baza de date pentru un soft contabil (tabele pentru firme, documente, încasări/plăți, declarații, termene; audit log; de ce nu se șterg niciodată înregistrările, ci se stornează).
- Precizie numerică: de ce nu se folosește float pentru bani (Decimal în Python), rotunjiri conform regulilor fiscale.
- Versionarea regulilor fiscale pe ani (plafoane, cote) ca să nu fie hardcodate în cod.
- Extragere de date din PDF-uri ANAF: cele mai robuste biblioteci (pdfplumber, PyMuPDF, Camelot), OCR pentru documente scanate, cum se gestionează schimbările de format ale fișelor ANAF.
- Securitate și GDPR: criptarea datelor, stocarea certificatelor digitale și a token-urilor, backup automat, jurnalizare acces.
- Testare: cum se testează calculele fiscale (exemple cu cazuri limită), date de test.
- Actualizare automată a aplicației și distribuție (PyInstaller, semnare, canal de update prin GitHub).
- Drumul de la desktop la web: când merită migrarea și cu ce stack (ex. FastAPI + PostgreSQL + un front-end simplu), păstrând logica de calcul reutilizabilă.

### 6. Foaie de parcurs recomandată
- Pe baza tuturor celor de mai sus, propune o ordine de implementare în 4-6 etape pentru un dezvoltator solo, începător, pornind de la aplicația descrisă: ce aduce cel mai mult valoare cu cel mai mic efort, ce depinde de ce, ce riscuri legislative trebuie urmărite.
- Pentru fiecare etapă: funcții, integrări necesare, estimare de complexitate (mică/medie/mare) și resurse de învățat (documentație oficială, tutoriale, repo-uri GitHub).

## Cerințe de format și calitate
- Scrie în limba română, cu termeni tehnici explicați la prima apariție.
- Citează sursele (documentație ANAF, Codul fiscal, pagini oficiale ale produselor, repo-uri GitHub) cu link-uri, și precizează data informației; marchează clar ce este incert sau în schimbare legislativă.
- Folosește tabele pentru comparații (integrări, softuri concurente, opțiuni de arhitectură).
- Include la final: un glosar de termeni, o listă de verificare („checklist”) cu funcțiile minime ale unui soft pentru PFA, și o listă de 10 „tips and tricks” practice din experiența produselor mature.
- Nu inventa API-uri sau funcții; dacă o integrare nu are acces programatic oficial, spune explicit acest lucru și descrie soluția de ocolire folosită în practică.
