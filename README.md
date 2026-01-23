# IDOS Public Transport custom integration
IDOS Public Transport integration scrapes Czech public transport information system [IDOS](idos.idnes.cz) and gets latest data about a bus/tram/train connection.

For english explanation, scroll all the way down.

# IDOS integrace do Home assistenta
Integrace IDOS Public Transport využívá český informační systém veřejné dopravy [IDOS] (idos.idnes.cz) k získávání nejnovějších dat o autobusovém/tramvajovém/vlakovém spojení.

*Nejsem zodpovědný za žádné zmeškané spojení!!! Na vlaky, autobusy a tramvaje (šaliny pro ty vybrané) choďte či běhejte za včasu!!!*

## Instalace
Pro integraci je potřeba použít [HACS](https://www.hacs.xyz/) a je potřeba tuto integraci přidat přes 'custom repository' - [návod zde](https://www.hacs.xyz/docs/faq/custom_repositories/). Jako typ repozitáře zvolte 'Integrace'.

Po přidání integrace můžete přidat zařízení 'IDOS' v nastavení a získáte tak přístup k 6 entitám:
- 3x entity senzorů - pro první 3 nalezená spojení
  - Zpřístupňuje zbývající čas do odjezdu spojení jako stav
  - Obsahuje také další informace o spojení jako atributy
- 2x entita textového vstupu
  - Umožňuje změnit cíl a příjezdovou stanici
- entita tlačítka
  - Zatím nefunguje

## Použití
Používejte entity jako u ostatních zařízení.

Pokud chcete změnit odjezdovou/cílovou stanici, tak použijte textové entity pro vstup.

Doporučuji nainstalovat [speciální IDOS UI kartu](https://github.com/Tomdein/homeassistant-public-transport-idos-card) pro hezčí zobrazení spojení. Nejen že je pěkná, ale tato karta umí i napovídat stanice když začnete psát do pole odjezdové/cílové stanice. Tuto kartu nainstalujete obdobně jako tuto integraci, jen jako typ repozitáře dejte 'Ovládací panel'.

## Kdyby se někdo chtěl dozvědět jak vytvořit vlastní integraci
*Aktualizace* Borci z HA už konečně vydali aspoň nějakou dokumentaci o vývoji integracích [zde](https://developers.home-assistant.io/docs/creating_component_index). I tak zde nechám tuto sekci.

Koukněte jak jsem postupně přidával kód po krocích - koukněte na gitu/githubu na tagy se jménem `example<X>`.


# English:
*I am not responsible for any missed connections!!! Walk or run to trains, buses and trams on time!!!*

## Installation
For integration, you need to use [HACS](https://www.hacs.xyz/) and you need to add this integration via 'custom repository' - [instructions here](https://www.hacs.xyz/docs/faq/custom_repositories/). Select 'Integration' as the repository type.

The integration exposes a few entites:
- 3x Sensor entites - for 3 earliest connections found
  - Exposes remaining time to departure for connection as state
  - Also has additional information about connection as attributes
- 2x Text input entity
  - Enables you to change destination and arrival station
- Button entity
  - Does not work yet

## Usage
Use entities as with other devices.

If you want to change the departure/destination station, use text entities for input.

I recommend installing the [special IDOS UI card](https://github.com/Tomdein/homeassistant-public-transport-idos-card) for a nicer connection display. Not only is it nice, but this card can also suggest stations when you start typing in the departure/destination station field. You install this card similarly to this integration, just set the repository type to 'Dashboard'.

This integration uses python idos-scraper package.

## Wanna create your custom integration?
*Update* The HA guys have finally released some documentation on developing integrations [here](https://developers.home-assistant.io/docs/creating_component_index). I'll leave this section here anyway.

See how I added the code step by step - follow git/github tags named `example<X>`.
