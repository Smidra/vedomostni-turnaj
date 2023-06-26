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


# Administrace hry
Do hry je potřeba vložit soubor s definicí hry. Formát souboru byl navržen tak, aby ho mohl vytvářet kdokoliv z pedagogického sboru. Jedná se o běžnou google tabulku, která s následně stáhne příbo ve formátu .csv, který se importuje do hry. Je velmi jednoduché šablonu vyplnit a hra by ji měla po uploadu úspěšně překousat. Stačí CSV z Google tabulek stáhnout (soubor-stáhnout-csv) a pak stažený soubor nahrát do hry. To zároveň resetuje celou hru.

Ukázka definice hry je volně přístupná na https://docs.google.com/spreadsheets/d/1zbQkvFwCIeVGs0YkSzFnw-ZVXSWXRlndgtvr3Jee-9U/edit?usp=sharing

V případě problémů lze body upravovat i ve vytvořeném administračním rozhraní. Nástěnky s tajenkou stejně jako administrační rozhraní lez nalézt na níže uvedených endpointech.

## Automatická tvorba Gamefiles
Do administračního rozhraní hry je implementovaná funkce aktomatické losování otázek + tvorba Gamefile. Stačí jít do administračníáho rozhraní. Pod nápisem "Generate gamefiles" uvidíte možnost nahrát soubor. Program očekává CSVčko se třemi sloupci. Pro větší turnaje doporučuji mít takto uloženou databázi více jak 1000 otázek.

```
PŘEDMĚT1, OTÁZKA1, ODPOVĚĎ1
PŘEDMĚT1, OTÁZKA2, ODPOVĚĎ2
PŘEDMĚT1, OTÁZKA3, ODPOVĚĎ3
PŘEDMĚT2, OTÁZKA4, ODPOVĚĎ4
...
```

Vyplňte poté pole "počet her", které určí kolik Gamefiles se vygeneruje. Je důležité myslet na všechny hry, které se budou během turnaje hrát - program generuje Gamefiles v rámci jednoho generování tak, aby se žádné otázky neopakovaly. Pak už stačí jen vyplnit počet řádků a sloupců a stisknout "Generate gamefiles".

Po šesti sekundách program buď nabídle soubor "output.xlsx" ke stažení, nebo ho hodí error, nebo nic neudělá. V druhém a třetím případě to zkuste znovu (rozdělování není deterministické - program se mohl zacyklit) a zkuste trochu déle počkat. Pokud to nepomůže tak zkuste změnit zadané parametry nebo rozšířit soubor o další otázky.

Ve staženém XLSX souboru si upravte tajenky, názvy a promyslete obtížnost jednotlivých kol. Pokud jste s nimi spojeni tak jednotlivé listy uložte jako nový soubor .csv.  To by měl být plně validní gamefile, který lze importovat do hry. Enjoy. :)

# Demo hry
Herní obrazovka: https://smidra.pythonanywhere.com/
Tajenka pro červený tým: https://smidra.pythonanywhere.com/red_dashboard
Tajenka pro modrý tým: https://smidra.pythonanywhere.com/blue_dashboard
Administrace: https://smidra.pythonanywhere.com/admin_dashboard

# Deployment hry
Hra je naprogramována ve frameworku Flask. Lze nasadit zdarma na pythonanywhere - stačí naklonovat toto GIT repo a nastavit následujícím způsobem.

```
Source code: /home/smidra/vedomostni-turnaj
Working directory: /home/smidra/
WSGI configuration file: /var/www/smidra_pythonanywhere_com_wsgi.py
Python version: 3.9
```

A to WSGI (/var/www/smidra_pythonanywhere_com_wsgi.py) vypadá takto:

```
# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = '/home/smidra/vedomostni-turnaj'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application  # noqa
```

## Docker
V případě zájmu o vlastní nasazení využijte docker příkazem, který se postará o nasazení včetně spuštení mockup webserveru na adrese localhost:80
... ale nevím kdy jsem ho naposledy zkoušel jesti funguje.

```
docker run -d -p 5050:5000 smidra/vedomostni-turnaj
```

Hra bude spuštěna na http://0.0.0.0:5050


# Development hry

```
flask --app flask_app run 
```

Hra bude spuštěna na http://127.0.0.1:5000


# Známé bugy
Na Linuxu mi při načtení csvčka, které má v názku háčky čárky mezery stránka spadne.