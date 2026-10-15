# PROMPT: Închidere lună / trimestru pentru o societate

> Versiune: 1.0 — redactat 15.10.2026. Valorile de praguri și cotele din Anexa A sunt
> **de referință la data redactării** și trebuie reconfirmate la fiecare rulare (vezi pasul 9).

---

## 0. Declanșator și parametri

Această regulă se aplică atunci când contabilul dă o comandă de forma:

- „închidere lună **<luna> <an>** pentru firma/societatea **<nume sau CUI>**”
- „închidere trimestrul **<T1..T4> <an>** pentru firma/societatea **<nume sau CUI>**”
- orice formulare echivalentă (ex. „închide octombrie la Karma to Code”, „fă închiderea T3 la La Blonda”).

Extrage obligatoriu:

| Parametru | Cum îl determini |
|---|---|
| `FIRMA` | nume + CUI (caută în baza de date / dosarul firmei; dacă există mai multe potriviri, întreabă) |
| `PERIOADA` | lună sau trimestru + an; la trimestru procesezi fiecare lună din trimestru și apoi consolidarea |
| `TIP_ENTITATE` | SRL / SA / PFA / II / IF / ONG — schimbă setul de verificări (vezi §12) |
| `REGIM_FISCAL` | din vectorul fiscal: micro / profit, plătitor TVA (lunar/trimestrial), TVA la încasare, angajator (D112), accize etc. |

Dacă lipsește un parametru și nu îl poți deduce fără dubiu, **întreabă înainte de a începe**. Nu presupune firma sau perioada.

---

## 1. Principii de lucru (obligatorii)

1. **Rulezi mai întâi regulile existente de verificare a societăților** (cele din CLAUDE.md / proiect / memorie). Prezentul prompt se adaugă la ele, nu le înlocuiește.
2. **Nu inventezi cifre, documente sau numere de facturi.** Orice valoare din raport are o sursă (balanță, jurnal, fișă terț, fișier SPV, PDF ANAF). Dacă nu ai sursa, scrii „LIPSĂ DATE” și pui întrebarea.
3. **Nu modifici înregistrări contabile și nu depui declarații fără aprobarea explicită a contabilului.** Generezi propuneri de note contabile și declarații în stare de **CIORNĂ**.
4. **Legislația se verifică la data rulării**, nu din memorie: pentru orice prag, cotă sau termen citezi actul normativ, articolul și data de la care se aplică (vezi §9 și Anexa A). Dacă nu poți verifica online, marchezi explicit „NEVERIFICAT LA ZI — valoare din Anexa A”.
5. **Orice neconcordanță devine o întrebare numerotată** în secțiunea „Întrebări pentru contabil” din raport, cu suma, documentul și efectul fiscal.
6. **Lucrezi pe istoric.** Lucrurile se repetă: compari luna curentă cu lunile anterioare și cu aceeași lună din anul precedent. Abaterile se explică sau se întreabă.
7. **Semafor pe fiecare secțiune**: 🟢 OK / 🟡 de clarificat / 🔴 blocant pentru închidere.
8. Limba raportului: română, cu diacritice. Termeni contabili conform OMFP 1802/2014.

---

## 2. Pregătire și istoricul societății

1. Încarcă dosarul firmei: balanțe (luna curentă + 12 luni anterioare), registru jurnal, jurnale TVA, fișe terți, fișa pe plătitor (ANAF), vectorul fiscal, declarațiile depuse, facturile SPV (e-Factura) primite și emise, extrase de bancă, registrul de casă, state de salarii.
2. Deschide (sau creează, dacă nu există) fișierul de istoric al societății: `istoric/<CUI>.md`. Conținut minim:
   - profil: obiect de activitate, CAEN, regim fiscal, perioadă TVA, gestiune (da/nu, tip), salariați, asociați (procente, alte firme deținute), administrator;
   - furnizori recurenți (interni și externi) cu frecvență și sume tipice;
   - clienți principali și comportament de plată (zile medii de încasare);
   - indicatori lunari (CA, cheltuieli, profit, TVA de plată/recuperat, sold casă, sold 542, sold 455/4551, capitaluri proprii);
   - probleme găsite la închiderile anterioare și cum s-au rezolvat;
   - alerte de praguri și evoluția lor;
   - decizii ale contabilului (ex. „sold 461 acceptat, este împrumut cu contract nr. …”).
3. **La final de închidere actualizezi istoricul** cu rezultatele perioadei curente. Istoricul este sursa pentru predicțiile de praguri (§9) și pentru detectarea lipsurilor (§8).

---

## 3. Facturi primite prin SPV (e-Factura) vs. contabilitate

Pentru fiecare factură primită în SPV în perioadă (și cele din lunile anterioare neînregistrate încă):

| Verificare | Criteriu | Dacă nu se potrivește |
|---|---|---|
| Există în contabilitate | același furnizor (CUI), număr și dată | 🔴 listă „facturi SPV neînregistrate” |
| Aceeași bază, TVA și total | diferență = 0,00 lei (toleranță 0,01 lei la rotunjiri) | 🔴 listă cu ambele sume și diferența |
| Cota de TVA corectă | 21% / 11% / scutit / taxare inversă conform tipului de operațiune și datei | 🟡 verifică deductibilitatea |
| Furnizor valid | activ în Registrul contribuabililor, cod TVA valid, nu în lista inactivilor la data facturii | 🔴 risc nedeductibilitate (Cod fiscal art. 11) |
| Furnizor cu TVA la încasare | dacă furnizorul aplică TVA la încasare, TVA se deduce la plată (4428 → 4426) | 🟡 verifică nota |
| Facturi în contabilitate dar inexistente în SPV | furnizor intern B2B obligat la e-Factura | 🟡 cere furnizorului transmiterea / întreabă contabilul |

Rezultat: tabel de reconciliere SPV ↔ contabilitate cu totaluri pe ambele părți și diferența netă.

---

## 4. Facturi emise: toate trimise în SPV?

1. Lista facturilor emise din contabilitate (jurnal de vânzări) ↔ lista facturilor transmise în SPV (e-Factura).
2. Pentru fiecare factură emisă: transmisă? în termenul legal (5 zile calendaristice de la emitere, Legea 296/2023 / OUG 120/2021 — confirmă termenul la zi)? validată fără erori? aceleași sume?
3. B2C: verifică dacă societatea are obligația e-Factura B2C (din 01.01.2025) și dacă a transmis.
4. Facturi stornate / anulate: există stornarea și în SPV?
5. Facturi emise către persoane fizice încasate cu bon fiscal: nu se dublează venitul (bon + factură).
6. Rezultat: 🔴 facturi netransmise (cu riscul sancțiunii), 🟡 transmise cu întârziere, 🟢 toate transmise.

---

## 5. Gestiune

### 5.1 Are gestiune?
Deduci din balanță (371, 301, 302, 303, 345, 381, 378, 4428 analitice) și din profilul din istoric. Dacă vinde marfă, trebuie să existe 371 și 607.

### 5.2 Conturi de gestiune „pe nedefinit”
Caută în program/balanță analitice de stoc fără gestiune atribuită (ex. „nedefinit”, „fără gestiune”, analitic 371.00, 607 fără corespondent 371). Orice astfel de cont cu rulaj sau sold = 🔴 și întrebare: „În ce gestiune se reclasifică?”.

### 5.3 Gestiune global-valorică (comerț cu amănuntul) — verificări obligatorii
- Fiecare intrare în 371 are înregistrate: `371 = 401` (cost), `371 = 378` (adaos comercial), `371 = 4428` (TVA neexigibilă). Lipsa oricăreia = 🔴.
- **Adaosul comercial (378) pe fiecare intrare nu are voie să fie negativ.** Listezi intrările cu adaos ≤ 0 sau anormal de mic/mare față de media gestiunii din istoric.
- Coeficientul K de repartizare a adaosului (378) la descărcarea de gestiune: recalculezi K = (Si 378 + Rc 378) / (Si 371 + Rd 371 − TVA neexigibilă) și compari cu cel folosit în notele de descărcare.
- Soldul 378 ≈ adaosul aferent stocului rămas; soldul 4428 (analitic gestiune) ≈ TVA aferentă stocului la preț de vânzare. Verifici relația: Sold 371 = Stoc la cost + Sold 378 + Sold 4428 (analitic). Abaterea = 🔴.
- Descărcarea de gestiune (607, 378, 4428) corespunde cu vânzările din 707 + 4427 din rapoartele Z / jurnal de vânzări.
- Sold 371 negativ sau sold 378 debitor = 🔴.
- Inventar: dacă perioada este decembrie sau există plus/minus de inventar, verifici înregistrarea (Legea 82/1991 art. 7, OMFP 2861/2009).

### 5.4 Gestiune cantitativ-valorică
Stocuri negative pe articole, articole cu preț unitar zero, intrări fără NIR, consumuri fără bon de consum = 🟡/🔴 după caz.

---

## 6. Balanța de verificare — conturi și solduri

### 6.1 Solduri contrare naturii contului (toate conturile, clasele 1–7)
Listezi orice cont cu sold contrar naturii. Cele mai frecvente:

| Cont | Natura | Sold anormal | Cauză tipică |
|---|---|---|---|
| 401, 404, 408 | creditor | debitor | plăți fără factură / factură neînregistrată / plată dublă |
| 4111, 418 | debitor | creditor | încasări în avans neînregistrate la 419, încasare dublă |
| 409, 419 | debitor / creditor | invers | avansuri neînchise |
| 5311, 5121, 5124 | debitor | creditor | plăți fără numerar / extras neînregistrat; **casă negativă = imposibil fizic = 🔴** |
| 371, 301, 303 | debitor | creditor | descărcare mai mare decât intrarea |
| 4423, 4424 | de plată / de recuperat | ambele cu sold | regularizare TVA neefectuată |
| 4426, 4427 | — | sold la final de lună | TVA neînchis prin 4423/4424 |
| 4428 | — | fără corespondent | vezi §7 |
| 421, 431, 437, 444 | creditor | debitor | plăți peste stat / stat neînregistrat |
| 441, 4411, 4418 | creditor | debitor | plată peste datorie sau impozit necalculat |
| 455, 4551 | creditor | debitor | **asociat creditat de firmă** — risc reîncadrare (vezi §10) |
| 461, 462 | debitor / creditor | invers | sume ridicate fără documente |
| 542 | debitor | creditor | decont înregistrat fără avans |
| 1012, 1171, 121 | — | verifică semnul și corelația cu D101/situații financiare | |

### 6.2 Conturi noi
Compari lista de conturi (sintetice și analitice) cu balanța lunii anterioare și cu lunile din istoric. Pentru fiecare cont apărut prima dată:
- din ce notă contabilă provine (articol contabil, document, sumă);
- este justificat (operațiune nouă reală) sau este o eroare de cont (ex. 6588 în loc de 6581, 628 în loc de 611)?
- se scrie în istoric cu explicația.

### 6.3 Comparativ lunar
Tabel cu rulajele conturilor din clasele 6 și 7 pe ultimele 12 luni; marchezi 🟡 variațiile > 30% față de media istorică și cheltuielile care lipsesc în luna curentă deși apar lunar (chirie, utilități, abonamente, salarii, contabilitate, leasing).

### 6.4 Cont 542 — avansuri de trezorerie
- Fiecare avans acordat ≤ plafonul zilnic din Legea 70/2015 (vezi Anexa A). Depășirile = 🔴 cu sumă, dată, persoană.
- Avansuri nedecontate mai vechi de termenul de decontare = 🟡; sold 542 la final de perioadă pe persoane, cu vechime.
- Sold 542 mare și persistent pe administrator/asociat = risc de reîncadrare ca dividend/avantaj în natură → întrebare obligatorie.

### 6.5 Casa (5311) și Legea 70/2015
- Sold casă zilnic ≤ plafon (Anexa A); excedentul trebuie depus la bancă în 2 zile lucrătoare.
- Plăți în numerar către un furnizor ≤ plafon zilnic/furnizor și ≤ plafon zilnic total; încasări numerar de la persoane juridice ≤ plafon; încasări/plăți cu persoane fizice ≤ plafon; **fragmentarea plăților este interzisă** (aceeași factură plătită în mai multe zile sub plafon = 🔴).
- Registrul de casă vs. 5311 din balanță: sold identic.

### 6.6 Capitaluri proprii
Calculezi: capitaluri proprii = total active − total datorii (= clasa 1 fără 16x și 15x). Dacă sunt **negative** sau **activul net < ½ din capitalul social** → aplici §10 integral.

---

## 7. TVA la încasare și notele de TVA

Dacă firma aplică TVA la încasare (verifică în Registrul persoanelor care aplică TVA la încasare + vectorul fiscal):

1. **Pe vânzări:** la facturare `4111 = 707 + 4428`; la încasare (integral/parțial) `4428 = 4427` proporțional cu suma încasată. Verifici fiecare încasare din perioadă (bancă + casă) că are nota de exigibilitate aferentă.
2. **Pe cumpărări de la furnizori** (indiferent dacă furnizorul aplică sau nu TVA la încasare, cât timp beneficiarul aplică): `4428 = 401` la primire, `4426 = 4428` la plată.
3. **Soldul 4428 (analitic TVA la încasare)** trebuie să fie egal cu: TVA din facturile emise neîncasate + TVA din facturile primite neplătite, din jurnalele de TVA la încasare. Orice diferență = 🔴 cu lista facturilor cauză.
4. Facturi neîncasate / neplătite peste termenul la care TVA devine exigibilă oricum (verifică regula în vigoare — istoric 90 de zile, eliminat; confirmă la zi).
5. 4428 pentru TVA la încasare ≠ 4428 pentru adaos global-valoric: trebuie analitice separate. Dacă sunt amestecate = 🔴.
6. D300: rândurile de TVA exigibilă corespund cu 4427/4426 din perioadă, nu cu 4428.
7. Pentru firmele fără TVA la încasare: 4426 și 4427 trebuie închise integral în 4423/4424; 4424 nu se compensează cu 4423 decât prin regularizare; TVA de recuperat solicitat la rambursare (D300 cu bifă) vs. report.
8. Compari plafonul de 4.500.000 lei (Anexa A) cu CA cumulată: depășirea obligă la ieșirea din sistem (D700).

---

## 8. Terți: furnizori, clienți, sold și vechime

1. **Totalul fișelor de furnizori** (401 + 404 + 408 + 409 pe parteneri) = sold 401/404/408/409 din balanță. Idem **clienți** (4111 + 418 + 419 + 4118). Diferențele = 🔴 cu lista partidelor nedefinite / plăților fără factură.
2. Parteneri cu sold debitor la 401 sau creditor la 4111 → cauză (plată dublă, avans, factură lipsă).
3. **Vechimea soldurilor** (aging): 0–30, 31–60, 61–90, 91–180, 181–365, > 365 zile.
4. **Pragul de alertă îl stabilești tu din istoric**: calculezi pentru fiecare firmă durata medie de încasare (DSO) și de plată (DPO) pe ultimele 12 luni; alertezi partenerii al căror sold depășește **2 × media istorică** sau 90 de zile (ce este mai mic), precum și orice sold > 365 zile. Explici în raport cum ai ales pragul.
5. Pentru soldurile vechi pregătești o **situație** (tabel: partener, facturi, sume, vechime, ultima plată/încasare, istoric relației) și **întrebi contabilul**: se mai încasează/achită? se compensează? se trece pe ajustări (491 — deductibilitate conform Cod fiscal art. 26)? se prescrie (3 ani, Cod civil art. 2517)? există litigiu?
6. Clienți cu sold vechi și furnizori cu sold vechi către **aceeași societate** → propune compensare (OUG 77/1999 pentru sume > 10.000 lei, confirmă la zi).
7. Verifici dacă vreun partener important a devenit inactiv / în insolvență (buletinul insolvenței) și efectul asupra creanței.

---

## 9. Fiscalitate: vector, fișă rol, declarații, praguri (legislația la data verificării)

### 9.1 Vector fiscal
- Citești vectorul fiscal actual (din aplicație / PDF SPV) și istoricul lui (`vector_istoric`). Orice modificare în perioadă (D700, din oficiu) se notează și se verifică efectul: perioadă TVA, micro ↔ profit, angajator, TVA la încasare.
- Obligațiile din vector trebuie să corespundă realității: are salariați → trebuie să aibă D112 în vector; depășește praguri → vezi 9.4.

### 9.2 Fișa pe plătitor (fișa rol)
- Pentru fiecare obligație: declarat vs. plătit vs. sold la zi; dobânzi (0,02%/zi) și penalități de întârziere (0,01%/zi) și de nedeclarare (0,08%/zi) acumulate — confirmă cotele la zi.
- Sume neidentificate în cont unic, compensări neefectuate, plăți duplicate, TVA de rambursat în curs.
- Soldul din fișă vs. soldurile 441, 4411, 4423/4424, 431, 437, 444, 446, 447 din balanță la aceeași dată. Diferența se explică (decalaj de declarare, plăți în tranzit) sau devine întrebare.

### 9.3 Declarații conform vectorului
Construiești calendarul perioadei: pentru fiecare obligație din vector, declarația datorată, termenul, status (depusă / nedepusă / rectificativă necesară) și dovada (recipisă). Minim de verificat: D300, D390 (dacă există operațiuni intracomunitare), D394, D100, D101 (anual), D112, D205 (anual), D406 SAF-T (lunar/trimestrial conform perioadei TVA — termenul este ultima zi a lunii următoare), D700, e-Factura, e-Transport (dacă transportă bunuri cu risc fiscal), e-TVA (decontul precompletat — diferențe față de D300 și notificările de conformare, termen de răspuns 20 de zile), D212 pentru PFA/II, D301 pentru neplătitori cu achiziții intracomunitare, D010/D020 pentru înregistrări.
Orice declarație nedepusă cu termen expirat = 🔴 cu calculul amenzii/penalității estimate.

### 9.4 Praguri și regimuri — verificare și predicție
Pentru fiecare prag din Anexa A:
1. valoarea curentă cumulată (an fiscal / 12 luni, după cum cere legea);
2. procent din plafon;
3. **proiecție până la final de an** pe baza istoricului (run-rate pe ultimele 3 și 12 luni, plus sezonalitate din anul anterior);
4. alertă: 🟡 la ≥ 80% din plafon sau dacă proiecția depășește plafonul; 🔴 la depășire efectivă, cu **data exactă a depășirii** și **termenul legal de acțiune** (ex. 10 zile de la sfârșitul lunii pentru înregistrarea în scopuri de TVA; trecerea la impozit pe profit de la trimestrul depășirii).

Praguri obligatorii de urmărit: scutire TVA, perioadă TVA lunar/trimestrial, TVA la încasare, microîntreprindere (plafon venituri, salariat, deținere asociat ≥ 25% în alte micro, CAEN cu cotă 3%), impozit pe profit (plăți anticipate, impozit minim), dividende (impozit + CASS la beneficiari), plafon e-Transport, plafon case de marcat/încasări numerar, plafoane Legea 70.

Dacă **vreo condiție de regim nu mai este îndeplinită** (ex. micro fără salariat peste termenul legal, asociat care deține > 25% în mai multe micro, venituri din consultanță dacă regula e în vigoare) → 🔴 + propunere D700 + efect fiscal recalculat.

### 9.5 Verificarea la zi a legislației
Înainte de a emite concluzii fiscale, cauți online (ANAF, Monitorul Oficial, legislatie.just.ro, static.anaf.ro) modificările aduse în ultimele 12 luni la: Codul fiscal (L 227/2015), Codul de procedură fiscală (L 207/2015), Legea 70/2015, Legea 31/1990, Legea 82/1991, OMFP 1802/2014, OUG 120/2021 (e-Factura), OPANAF SAF-T, legile bugetare și pachetele fiscale (ex. L 296/2023, OUG 115/2023, OUG 156/2024, L 141/2025, OUG 22/2025). Scrii în raport **data verificării** și lista actelor consultate. Dacă găsești o valoare diferită de Anexa A, folosești valoarea verificată și semnalezi că Anexa A trebuie actualizată.

---

## 10. Capitaluri proprii negative și activ net sub ½ din capitalul social — ce NU ai voie

Când constați capitaluri proprii negative (sau activ net < ½ capital social), **îmi amintești obligatoriu** (chiar dacă am mai fost avertizat), cu trimitere la lege, cel puțin următoarele:

1. **Nu se distribuie dividende** și nu se ridică sume „în contul dividendelor”: dividendele se plătesc doar din profituri reale, determinate potrivit legii (Legea 31/1990 art. 67 alin. 3); distribuirea din profituri fictive sau care nu puteau fi distribuite este **infracțiune** (art. 272^1).
2. **Profitul anului se folosește mai întâi la acoperirea pierderii reportate** (OMFP 1802/2014, secțiunea privind repartizarea profitului; Legea 82/1991 art. 19), nu la dividende.
3. **Obligația administratorului de a convoca AGA extraordinară** când activul net a scăzut sub jumătatea capitalului social, pentru a decide dizolvarea sau reîntregirea; dacă nu se reîntregește până la finalul exercițiului următor, capitalul se reduce sau orice persoană interesată (inclusiv ONRC/ANAF) poate cere dizolvarea (Legea 31/1990 art. 153^24 și art. 237 — verifică aplicabilitatea la SRL și forma la zi a textului).
4. **Nu se reduce capitalul social sub minimul legal** și nu se reduce fără hotărâre AGA publicată și fără respectarea termenului de opoziție al creditorilor (Legea 31/1990 art. 207–208).
5. **Societatea nu creditează asociații/administratorii**: sold debitor pe 455/4551/461 fără contract de împrumut = sumă ridicată fără titlu → reîncadrare ca dividend (impozit pe dividende + CASS) sau avantaj în natură; cu capitaluri negative riscul penal crește (vezi pct. 1).
6. **Soluții legale de reîntregire**: aport la capital (majorare), prime de capital, împrumut de la asociat cu contract (4551, dobândă conform regulilor de deductibilitate și prețuri de transfer dacă e cazul), conversia creanței asociatului în capital, renunțarea asociatului la creanță (venit impozabil pentru societate — atenție la efect fiscal).
7. **Stare de insolvență**: dacă datorii exigibile > 90 de zile nu pot fi plătite din fonduri disponibile, administratorul are obligația de a cere deschiderea procedurii în 30 de zile (Legea 85/2014 art. 66); nerespectarea atrage răspundere personală (art. 169) și posibil penală.
8. **Facilitățile pentru capitaluri pozitive** (OUG 153/2020) — verifică dacă mai sunt în vigoare; dacă da, societatea le pierde.
9. **Efecte colaterale**: riscuri la licitații publice, bănci, leasing; reconsiderarea de către ANAF a tranzacțiilor cu afiliații; obligația de prezentare în notele explicative la situațiile financiare.

Cauți pe legislatie.just.ro textul la zi al articolelor citate și le menționezi cu numărul și data ultimei modificări.

---

## 11. Facturi externe (furnizori din UE / non-UE)

1. Din istoric: lista furnizorilor externi recurenți (ex. Google, Meta, Microsoft, Amazon, Apple, Shopify, OpenAI, Adobe, Canva, platforme de freelancing, hosting) cu frecvență lunară.
2. Pentru fiecare furnizor recurent **absent în luna curentă** → 🟡 „Lipsește factura <furnizor> pentru <luna>; luna trecută a fost <sumă>. Te rog trimite-o sau confirmă că nu există.”
3. Pentru fiecare factură externă înregistrată: tratament corect — **servicii intracomunitare B2B**: taxare inversă `4426 = 4427`, raportare în D390 (cod S) și D300 la rândurile corespunzătoare, cod valid VIES al furnizorului și al societății (dacă societatea e neplătitoare de TVA: obligația de a se înregistra special cu D091/D010 și de a plăti TVA prin D301 — verifică). **Non-UE**: TVA prin taxare inversă conform art. 307; **bunuri**: DVI / achiziție intracomunitară (cod A în D390), e-Transport dacă e cazul.
4. Facturi externe în valută: cursul BNR din data facturii, diferențele de curs la plată (665/765), reevaluarea soldurilor la final de lună/an.
5. Furnizorul extern aplică TVA românesc (ex. OSS) → nu se face taxare inversă, se verifică deductibilitatea.
6. Chitanțe/„receipts” fără factură fiscală (card online) → nu sunt documente justificative pentru TVA; cere factura.

---

## 12. Particularități după tipul entității

- **PFA / II / IF (sistem real)**: nu există balanță în partidă dublă; verifici Registrul-jurnal de încasări și plăți, Registrul inventar, venit net, cheltuieli deductibile limitat (OMFP 170/2015), CAS/CASS la plafoane de 12/24 și 6/12/24 salarii minime, D212 (termen 25 mai), eventual TVA dacă e plătitor. La normă de venit: verifici plafonul de 25.000 euro pentru trecerea la sistem real.
- **Micro**: cotă 1%/3% pe venituri (baza impozabilă conform art. 53 Cod fiscal: se scad veniturile din 711, 722, 758x etc.), D100 trimestrial, condiția de salariat, plafonul de venituri.
- **Profit**: cheltuieli nedeductibile (art. 25), amortizare fiscală (art. 28), sponsorizare (limite), rezerva legală (5% din profit până la 20% din capital — Legea 31/1990 art. 183), impozit minim pe cifra de afaceri dacă CA > plafon, D100 trimestrial + D101 anual.
- **Angajator**: stat de salarii vs. 421/431/436/437/444, D112, salariu minim în vigoare (inclusiv sectoare cu minim special), tichete de masă, avantaje în natură, concedii, REVISAL.
- **ONG**: Legea 227 art. 15, 2% / 3,5%, D100 doar pentru activitate economică.

---

## 13. Generarea declarațiilor și introducerea în „Financiara” (localhost)

Numai după ce analiza din §2–§12 este completă și nu există 🔴 nerezolvat (sau contabilul a decis să continue):

1. Generezi **ciornele** declarațiilor datorate pentru perioadă, conform calendarului din §9.3, cu valorile pe rânduri și sursa fiecărui rând (ex. D300 rd. 1 = rulaj 4427 din jurnal vânzări 21%). Format: tabel rând-cu-rând + fișierul în formatul cerut de ANAF (PDF inteligent / XML) dacă ai instrumentele; altfel, fișier de import.
2. Verifici corelațiile obligatorii între declarații (D300 ↔ D390 ↔ D394 ↔ D406; D100 ↔ balanță; D112 ↔ stat de salarii; e-TVA ↔ D300).
3. Deschizi aplicația **Financiara** de pe localhost și introduci **toate documentele pe care aplicația le cere** pentru perioadă (balanță, declarații, fișa rol, SPV, extrase etc.), în ordinea cerută de aplicație; notezi în raport ce ai introdus și ce a refuzat.
4. Rulezi secțiunea **Analiză financiară**. Dacă aplicația **nu are** o astfel de secțiune, **o construiești** (în codul aplicației, pe ramura de lucru, cu commit) cu minim: indicatori de lichiditate (curentă, imediată), solvabilitate, îndatorare, rotația creanțelor/datoriilor/stocurilor (DSO, DPO, DIO), marje (brută, operațională, netă), cash-flow lunar, evoluția capitalurilor proprii, evoluția pragurilor fiscale, aging clienți/furnizori, comparativ cu lunile anterioare și cu aceeași perioadă a anului precedent. Explici în raport ce ai construit și cum se folosește.
5. **Nu depui nimic la ANAF** fără confirmarea explicită a contabilului pentru fiecare declarație.

---

## 14. Raportul final (format fix)

```
# Raport închidere <FIRMA> (CUI <…>) — <PERIOADA>
Data rulării: <…>   Legislație verificată la: <…>   Regim: <micro/profit, TVA …>

## 1. Rezumat (semafor)
| Secțiune | Stare | Puncte cheie |
...

## 2. Întrebări pentru contabil (numerotate, cu sumă, document, efect fiscal, termen)
## 3. Neconcordanțe găsite (SPV, terți, balanță, gestiune, TVA la încasare)
## 4. Alerte praguri și regim fiscal (valoare, % din plafon, proiecție, data estimată, acțiune)
## 5. Fiscalitate: vector, fișă rol, calendar declarații, declarații generate (ciorne)
## 6. Capitaluri proprii / Legea 70 / 542 — memento obligații (dacă e cazul)
## 7. Facturi externe lipsă / de cerut
## 8. Situația soldurilor vechi clienți/furnizori (cu pragul ales și motivarea lui)
## 9. Ce am introdus în Financiara și rezultatul analizei financiare
## 10. Legislație consultată (act, articol, data verificării, sursă)
## 11. Istoric actualizat (ce am adăugat în istoric/<CUI>.md)
## 12. Checklist de închidere (bifat/nebifat)
```

Checklist minim: SPV primite reconciliate · SPV emise complete · gestiune fără nedefinit · adaos ≥ 0 · fără solduri contrare naturii · conturi noi explicate · fișe terți = balanță · TVA la încasare închis · 4426/4427 închise · Legea 70 respectată · 542 în plafon · capitaluri proprii verificate · vector = realitate · fișa rol reconciliată · declarații complete · praguri verificate · facturi externe complete · istoric actualizat.

---

## Anexa A — Praguri, cote, termene și legi de referință (la 15.10.2026; **reconfirmă la fiecare rulare**)

| Subiect | Valoare de referință | Temei (de verificat la zi) |
|---|---|---|
| Cota standard TVA / redusă | 21% / 11% (de la 01.08.2025) | L 141/2025, Cod fiscal art. 291 |
| Plafon scutire TVA (întreprinderi mici) | 395.000 lei (de la 01.09.2025) | Cod fiscal art. 310, OUG 22/2025 |
| Înregistrare TVA la depășire | cerere în 10 zile de la sfârșitul lunii depășirii | art. 310 |
| Perioadă fiscală TVA | trimestrial dacă CA an precedent < 100.000 euro și fără AIC bunuri; altfel lunar | art. 322 |
| TVA la încasare — plafon | 4.500.000 lei CA | art. 282 |
| Termen e-Factura | 5 zile calendaristice de la emitere | OUG 120/2021, L 296/2023 |
| Micro — plafon venituri | 100.000 euro (de la 01.01.2026; 250.000 euro în 2025) | OUG 156/2024, art. 47 |
| Micro — cote | 1% (venituri ≤ 60.000 euro și CAEN neexceptat) / 3% | art. 51 |
| Micro — condiții | ≥ 1 salariat; asociat ≥ 25% într-o singură micro; capital privat | art. 47 |
| Impozit pe profit | 16% | art. 17 |
| Impozit pe dividende | 16% (de la 01.01.2026; 10% până în 2025) | L 141/2025, art. 97 |
| CASS la dividende (beneficiari PF) | plafoane 6 / 12 / 24 salarii minime | art. 170 |
| Rezerva legală | 5% din profit brut până la 20% din capital social | L 31/1990 art. 183 |
| Legea 70/2015 — plăți numerar PJ→PJ | 5.000 lei/zi/furnizor, max 10.000 lei/zi total | L 70/2015 art. 3, OUG 98/2023 |
| Legea 70/2015 — PJ ↔ PF | 10.000 lei/zi/persoană | art. 4 |
| Legea 70/2015 — avans trezorerie | 5.000 lei/zi/persoană | art. 3 |
| Legea 70/2015 — plafon casă | 50.000 lei/zi; excedent depus în 2 zile lucrătoare | art. 4^1 |
| Legea 70/2015 — sancțiune | amendă procentuală din suma peste plafon (10% / 25% — confirmă) | art. 12 |
| Dobânzi / penalități ANAF | 0,02%/zi · 0,01%/zi · nedeclarare 0,08%/zi | L 207/2015 art. 174, 176, 181 |
| Termen D300, D390, D100, D112 | 25 ale lunii următoare perioadei | Cod fiscal / OPANAF |
| Termen D394 | 30 ale lunii următoare | OPANAF 3769/2015 |
| Termen D406 SAF-T | ultima zi a lunii următoare perioadei (lunar/trimestrial ca TVA) | OPANAF 1783/2021 |
| Termen D101 | 25 martie / 25 iunie anul următor — confirmă | art. 42 |
| Termen D212 (PFA) | 25 mai anul următor | art. 122 |
| Prescripție creanțe comerciale | 3 ani | Cod civil art. 2517 |
| Ajustări creanțe (491) deductibile | condiții art. 26 Cod fiscal (procente / insolvență) | art. 26 |
| Inventariere | anual obligatoriu | L 82/1991 art. 7, OMFP 2861/2009 |
| Păstrare documente | 5 ani (registre, documente justificative) — confirmă | L 82/1991 art. 25 |
| Activ net < ½ capital social | convocare AGA, reîntregire / reducere / dizolvare | L 31/1990 art. 153^24, 237 |
| Dividende din profit fictiv | infracțiune | L 31/1990 art. 67, 272^1 |
| Insolvență — obligația cererii | 30 de zile de la apariția stării | L 85/2014 art. 66 |

**Legi de bază pentru o conduită profesionistă** (de citat când e cazul): Legea contabilității 82/1991; OMFP 1802/2014 (reglementări contabile); OMFP 2634/2015 (documente financiar-contabile); OMFP 2861/2009 (inventariere); Codul fiscal L 227/2015 + Normele HG 1/2016; Codul de procedură fiscală L 207/2015; Legea 70/2015 (numerar); Legea 31/1990 (societăți); Legea 85/2014 (insolvență); OUG 28/1999 (case de marcat); OUG 120/2021 (e-Factura); OUG 41/2022 (e-Transport); OUG 77/1999 (compensări); Legea 53/2003 (Codul muncii) și HG salariu minim; OG 65/1994 (CECCAR) și Codul etic al profesionistului contabil; Legea 129/2019 (prevenirea spălării banilor — obligații pentru contabili).

---

## 15. Autoînvățare: lecții învățate, corecții și ștergerea erorilor

Scopul: regula se îmbunătățește singură din greșeli și din situații noi, dar **nu păstrează lecții greșite**.

### 15.1 Unde se țin lecțiile
- `lectii/lectii-invatate.md` — lecții **generale** (valabile pentru toate firmele): proceduri, legislație, erori de interpretare, formatul raportului.
- `istoric/<CUI>.md`, secțiunea „Lecții și excepții acceptate” — lecții **specifice firmei** (ex. „la La Blonda adaosul la articolele X este 0 din cauza promoțiilor, nu e eroare”).
- Fiecare lecție are formatul:

```
### L-<număr> · <titlu scurt>
- Data: <zz.ll.aaaa>   Firma: <general / CUI>   Status: în test | activă | anulată
- Situația: <ce s-a întâmplat, cu suma/documentul dacă e cazul>
- Lecția (regula de aplicat): <o propoziție imperativă, verificabilă>
- Sursa: contabil (confirmare explicită) | lege (act + articol + link) | eroare observată de mine
- Confirmări: <n> (număr de închideri în care regula s-a dovedit corectă)
- Istoric: <zz.ll.aaaa> creată · <zz.ll.aaaa> confirmată · <zz.ll.aaaa> anulată (motiv)
```

### 15.2 Când înveți (creezi o lecție)
Creezi o lecție **numai** în aceste cazuri:
1. **Contabilul mă corectează** („nu, aici e corect pentru că…”, „data viitoare să faci…”, „asta nu se verifică așa”). Lecția se scrie imediat, cu status **activă** dacă corecția a fost explicită, altfel **în test**.
2. **Am găsit o eroare proprie** (am semnalat 🔴 ceva ce s-a dovedit corect, sau am ratat ceva ce contabilul a găsit). Status: **în test** până la confirmare.
3. **A apărut ceva nou** (o lege verificată la sursă, un tip de operațiune nouă, un furnizor nou recurent, un prag modificat). Lecțiile din lege au status **activă** doar dacă au link către textul oficial; altfel **în test**.
4. **Contabilul îmi spune direct**: „învață: …” → lecție activă; „uită: …” → anulare (vezi 15.4); „lecții” → listez lecțiile active și în test.

Nu creezi lecții din presupuneri, din o singură observație neconfirmată sau din lucruri deja acoperite de prompt. Înainte de a crea, cauți dacă există deja o lecție similară: dacă da, o actualizezi (nu dublezi).

### 15.3 Cum folosești lecțiile la fiecare închidere
1. **La început** citești `lectii/lectii-invatate.md` și secțiunea de lecții din `istoric/<CUI>.md`. Lecțiile **active** se aplică obligatoriu. Lecțiile **în test** se aplică, dar rezultatul lor se marchează în raport cu „(lecție în test L-nn)”. Lecțiile **anulate** nu se aplică și nu se re-creează.
2. **La final** scrii în raport (secțiunea 11) ce lecții ai aplicat, ce lecții noi propui și ce lecții au fost contrazise.
3. O lecție **în test** devine **activă** după 2 închideri în care s-a dovedit corectă (Confirmări ≥ 2) sau la confirmarea explicită a contabilului.
4. Dacă regula din prompt și o lecție se contrazic: **lecția activă câștigă** (este mai nouă și confirmată), dar semnalezi contradicția în raport ca să decidă contabilul dacă actualizăm promptul.

### 15.4 Când și cum ștergi (anulezi) o lecție
O lecție se **anulează** dacă:
- contabilul spune că e greșită sau zice „uită: …”;
- aplicarea ei a produs o eroare într-o închidere (contabilul a corectat rezultatul);
- legea pe care se baza s-a schimbat (verificat la sursă);
- o lecție mai nouă, confirmată, o contrazice;
- nu a mai fost relevantă de 12 luni (în acest caz **întrebi** înainte de a anula).

Anularea înseamnă: status → **anulată**, motivul și data în „Istoric”, iar lecția se **mută** în secțiunea „Lecții anulate — NU se reînvață” de la finalul fișierului, redusă la 2 rânduri (titlu + motiv). Păstrezi urma tocmai ca să nu reînveți aceeași greșeală din aceeași situație. Lecțiile anulate mai vechi de 24 de luni se șterg complet (întrebi înainte).

### 15.5 Reguli de igienă
- O lecție = o regulă. Fără lecții vagi („fii mai atent”). Trebuie să se poată verifica dacă a fost aplicată.
- Max. 3 lecții noi propuse per închidere; restul le pui ca întrebări.
- Nu scrii în lecții date personale (CNP, IBAN, salarii nominale); folosești CUI și denumiri.
- Orice modificare a fișierelor de lecții se face cu commit separat, cu mesaj de forma `lectii: L-12 activă (TVA la încasare, 4428 analitic)`, ca să se vadă în istoricul git ce s-a învățat și ce s-a șters.
