# Aplikace vědomostní turnaj
## Radek Šmíd 2021
Repozitář: https://github.com/Smidra/vedomostni-turnaj

# summary
Jeopardy-like custom made czech game to host knowledge tournaments at local elementary school (ZŠ Vzbíralova).

- Running on https://smidra.pythonanywhere.com/
- Can be deployed anywhere where flask runs
- Simple, quick, and dirty code and Dockerfile (very dirty)


# Shrnutí
Aplikace vědomostní turnaj vznikla jako nápad poskytnout žákům ZŠ Vybíralova alternativu k fotbalovému turnaji. Hra má nesludující funkce:
- Motivační
	- Žáci si zažijí, že lze soutěžit týmově i mimo sporty.
	- Využijí své mezioborové znalosti.
- Repetetivně fixační
	- Žáci sledující probhající turnaj si mimoděk opakují znalosti
	- Žáci hrající turnaj si v družstvu mezi sebou připomínají věci z hodiny
- Kontrolně diagnostická (méně)
	- Učitelé napříč školou mohou vidět znalosti nabyté v ostatních předmětech.

# Hra
Hra opisuje oblíbenou televizní soutě "Jeopardy" či v češtině "Riskuj". S tím rozdílem, že hrají pouze dva týmy a jsou složené z cca 4 hráčů. Týmy mají jasně dané barvy: červený a modrý. Každý z týmů před sebou má jednu živou nástěnku s jejich tajenkou (monitor). Cílem hry je uhádnout tajenku.

Když přijde na tým řada má možnost si vybrat zda bude ve svém kole odpovídat buď na otázku a nebo se pokusí rozluštit tajenku. Tajenku se může pokusit rozluštit libovolně-mnohokrát. Pokud luští tajenku pak má jeden pokus. Pokud odpovídá na otázku, vybere si jí z herního pole a pak má 30-60s na odpověď. Tu pak moderátor odhalí podržením na otázku a případně přidělí body. Za každý bod se příslušnému týmu na jeho monitoru odhalí jedno písmeno tajenky.


# Administrativa hry
Do hry je potřeba vložit soubor s definicí hry. Formát souboru byl navržen tak, aby ho mohl vytvářet kdokoliv z pedagogického sboru. Jedná se o běžnou google tabulku, která s následně stáhne příbo ve formátu .csv, který se importuje do hry. Je velmi jednoduché šablonu vyplnit a hra by ji měla po uploadu úspěšně překousat. Stačí CSV z Google tabulek stáhnout (soubor-stáhnout-csv) a pak stažený soubor nahrát do hry. To zároveň resetuje celou hru.

Ukázka definice hry je volně přístupná na https://docs.google.com/spreadsheets/d/1zbQkvFwCIeVGs0YkSzFnw-ZVXSWXRlndgtvr3Jee-9U/edit?usp=sharing

V případě problémů lze body upravovat i ve vytvořeném administračním rozhraní. Nástěnky s tajenkou stejně jako administrační rozhraní lez nalézt na níže uvedených endpointech.

# Demo hry
Herní obrazovka: https://smidra.pythonanywhere.com/
Tajenka pro červený tým: https://smidra.pythonanywhere.com/red_dashboard
Tajenka pro modrý tým: https://smidra.pythonanywhere.com/blue_dashboard
Administrace: https://smidra.pythonanywhere.com/admin_dashboard

# Deployment hry
Hra je naprogramována ve frameworku Flask.
V případě zájmu o vlastní nasazení využijte docker příkazem, který se postará o nasazení včetně spuštení mockup webserveru na adrese localhost:80

```
docker run -d -p 5050:5000 smidra/vedomostni-turnaj
```

Hra bude spuštěna na http://0.0.0.0:5050
