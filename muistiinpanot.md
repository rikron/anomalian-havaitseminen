Pidä omaa lopputyöpäiväkirjaa esimerkiksi tiedostossa lopputyo/muistiinpanot.md. Kirjaa jokaisesta moduulista:

    mitä päätit
    mitä ajoit
    mikä tulos tai havainto syntyi
    mikä jäi epävarmaksi
    mitä muutat seuraavaksi

Jos oma aineisto ei vielä ole valmiina, tee moduulin oma harjoitus kurssin pienellä esimerkkidatalla ja kirjaa, miten sama vaihe tehtäisiin omalle aineistolle myöhemmin

# Lopputyö

## Alustava tapauskansio
Alustavana sovellusalueena verkkotunkeutumisen havaitseminen ja datasettinä UNSW-NB15, train/test CSV. Verkkotunkeutumisen havaitsemisessa normaalin ja poikkeavan liikenteen havaitseminen on tärkeää. Huomaamalla verkkoliikenteessä esiintyviä poikkeamia, voidaan välttää ja estää mahdollisia tunkeutumisyrityksiä, sekä ylläpitää tietoturvaa. Havaitsemalla poikkeavaa liikennettä, voidaan tunnistaa mahdollisia yrityksiä tunkeutua järjestelmään. 

Normaalia dataa voisi olla tavalliset verkkoliikenteen toiminnot, kuten käyttäjien suorittamat toiminnot, keep-alive -viestit ja taustalla pyörivien sovellusten verkkoliikenne. Poikkeavaa dataa voisivat olla yllättävästä IP-osoitteesta tuleva liikenne, pingaukset ja lyhyessä aikavälissä saapuvat runsaat pyyntömäärät.

### 01 Mitä anomalia tarkoittaa

Verkkoliikenteessä pisteanomalia saattaisi olla erikoinen ftp kirjautumisyritys tai suuri pakettimäärä. Kontekstuaalinen anomalia saattaisi taas olla useampi yllättävä ftp kirjautumisyritys etenkin, jos FTP ei ole käytössä kohdejärjestelmissä. Kollektiivisia anomalioita voi esiintyä verkkoliikenteen seassa, sillä aineistossa yksittäinen lokimerkintä ei saata itsessään nostaa hälytystä, kun taas kokoelma poikkeuksia voisi olla huomionarvoista. Tässä työssä käytämme termiä havainto yksittäisestä lokimerkinnästä.

### 02 Datatyypit ja datamatriisi

Tässä lopputyössä alustavana aineistona on siis UNSW-NB15 datasetti, jossa on synteettistä verkkoliikennettä kategorisoituna tunnistettuihin hyökkäyksiin tai normaaliin liikenteeseen. Vaihtoehtoisena aineistona voisi olla KDD Cup 1999 10 percent.  UNSW-NB15 aineiston viitteet löytyvät tämän kansion README.md tiedostosta. Test CSV on noin 15MB ja training CSV noin 32MB. Aineisto on akateemisessa käytössä vapaasti hyödynnettävissä, kun alkuperäisiin artikkeleihin viitataan oikeaoppisesti. Aineiston tärkeimpiä sarakkeita ovat kesto (dur), protokolla (proto), palvelu (service), lähettäjän ja kohteen tavut (sbytes, dbytes) sekä pakettinopeus (rate). Sarakkeita on kymmeniä kappaleita, joista osa on tärkeämpiä kuin toiset. Edellä mainitut ovat mielekkäimpiä tutkia yksittäisten havaintojen kohdalta, mutta muut sarakkeet tarjoavat niin ikään hyödyllistä tietoa. Aineistossa on olemassa valmiit label-arvot. Label kertoo, onko havainto poikkeava/anomalia binäärisesti ja attack_cat kertoo valmiiksi havaitun hyökkäysluokan. 

