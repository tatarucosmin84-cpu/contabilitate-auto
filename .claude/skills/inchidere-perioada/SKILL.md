---
name: inchidere-perioada
description: Închiderea lunii sau a trimestrului pentru o societate (SRL/PFA) - reconciliere SPV, gestiune, balanță, TVA la încasare, terți, vector fiscal, fișă rol, praguri, declarații, Financiara. Se folosește când contabilul scrie „închidere lună … pentru firma …” sau „închidere trimestrul … pentru societatea …”.
---

Citește integral fișierul `prompts/inchidere-perioada.md` din acest repo și aplică-l pas cu pas
pentru firma și perioada din comanda primită (argumentele: `$ARGUMENTS`).

Reguli scurte de reținut:
- rulezi mai întâi regulile existente de verificare a societăților, apoi pașii din prompt;
- nu inventezi cifre, nu modifici înregistrări și nu depui declarații fără confirmare;
- legislația se verifică la data rulării, cu citarea actului și a articolului;
- raportul final respectă formatul din §14 al promptului și se salvează în `rapoarte/<CUI>-<perioada>.md`;
- actualizezi `istoric/<CUI>.md` la final.
