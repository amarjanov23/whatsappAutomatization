# WhatsApp Automatization

Ovaj projekt omogućava automatizirano dodavanje kontakata u WhatsApp zajednicu koristeći Selenium WebDriver.

## Preduvjeti

Prije pokretanja osiguraj da imaš instalirane sljedeće pakete:

- Python 3.x
- Google Chrome
- ChromeDriver (odgovarajuća verzija za tvoj Chrome)

Pakete možeš instalirati pomoću:

sh
pip install -r req.txt

## Kako koristiti

### Postavi Chrome profil
- Otvori Google Chrome, prijavi se na [WhatsApp Web](https://web.whatsapp.com) i sačuvaj svoj korisnički profil.
- U skripti (main.py), postavi putanju do svog Chrome profila. Preporučuje se korištenje relativne putanje (npr. chrome_profile).

### Pokreni skriptu
- Otvori terminal u direktoriju projekta i pokreni:
  
sh
  python src/main.py

Nakon pokretanja, pojavit će se QR kod za prijavu na WhatsApp Web. Skeniraj QR kod sa svojim mobitelom.

## Dodavanje kontakata

Skripta će automatski pretražiti zadanu WhatsApp zajednicu i pokušati dodati sve vidljive kontakte.

Kontaktima se pristupa preko XPath selektora, pa se preporučuje ručno testiranje i eventualno prilagođavanje XPath izraza ako se WhatsApp UI promijeni.

## Napomena

- WhatsApp može ograničiti masovno dodavanje kontakata, stoga se preporučuje ručno testiranje prije korištenja skripte za veći broj kontakata.
- Provjeri kompatibilnost verzije ChromeDriver-a s verzijom Google Chrome-a koju koristiš. Preporuča se koristiti webdriver-manager za automatsko preuzimanje ispravne verzije.
- Datoteka `chrome_profile/` i slični direktoriji s korisničkim podacima trebaju biti isključeni iz repozitorija (dodati u `.gitignore`) zbog privatnosti i veličine.

## Autor

**Adam Marjanović**  
[https://github.com/amarjanov23](https://github.com/amarjanov23