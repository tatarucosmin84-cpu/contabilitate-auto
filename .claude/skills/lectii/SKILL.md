---
name: lectii
description: Gestionează lecțiile învățate ale regulii de închidere (listare, adăugare, anulare). Se folosește la comenzi ca „/lectii”, „învață: …”, „uită: …”, „ce ai învățat”, „șterge lecția …”.
---

Aplică §15 din `prompts/inchidere-perioada.md`. Fișiere: `lectii/lectii-invatate.md` (generale) și
`istoric/<CUI>.md` secțiunea „Lecții și excepții acceptate” (pe firmă). Argumente primite: `$ARGUMENTS`.

- fără argumente sau „listă”: afișează lecțiile active și în test, grupate general / pe firmă, cu id, titlu, status, confirmări;
- „învață: <regula> [firma <nume/CUI>]”: creează lecția cu status activă (sursa: contabil), după ce verifici că nu există deja una similară; dacă există, o actualizezi;
- „uită: <L-nn sau descriere>”: marchezi lecția anulată, ceri motivul dacă nu e dat, o muți în „Lecții anulate — NU se reînvață”;
- „confirmă L-nn”: incrementezi confirmările; la ≥ 2 trece în activă;
- orice modificare: commit separat cu mesaj `lectii: ...`, apoi afișezi lecția rezultată.
