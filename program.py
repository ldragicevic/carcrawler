from polovni_automobili_crawler import PaCrawler
from mobile_de_crawler import MdCrawler

PA_START_URL = r'https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=bmw&model%5B%5D=serija-1&price_from=&price_to=15000&year_from=2015&year_to=2019&fuel%5B%5D=2309&door_num=3013&submit_1=&date_limit=&showOldNew=all&modeltxt=&engine_volume_from=&engine_volume_to=&power_from=&power_to=&mileage_from=&mileage_to=&emission_class=&gearbox%5B%5D=251&seat_num=&wheel_side=2630&registration=&country=&country_origin=&city=&damaged%5B%5D=3799&registration_price=&page=&sort=price_asc'
MD_START_URL = r'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&doorCount=FOUR_OR_FIVE&fuels=DIESEL&isSearchRequest=true&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=g20&maxFirstRegistrationDate=2019&maxMileage=200000&maxPowerAsArray=PS&maxPrice=12000&minFirstRegistrationDate=2015&minMileage=50000&minPowerAsArray=PS&minPrice=7000&scopeId=C&sfmr=false&transmissions=AUTOMATIC_GEAR&vatable=true'

#PaCrawler(PA_START_URL, "PolovniAutomobili").start()
MdCrawler(MD_START_URL, "MobileDe").start()
