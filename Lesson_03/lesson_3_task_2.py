
from smartphone import Smartphone


catalog = []


catalog.append(Smartphone("Apple", "iPhone 22", "+7912"))
catalog.append(Smartphone("Samsung", "Galaxy S28", "+7900"))
catalog.append(Smartphone("Xiaomi", "Mi 300", "+7934"))
catalog.append(Smartphone("Google", "Pixel 7", "+7911"))
catalog.append(Smartphone("OnePlus", "20 Pro", "+7900"))

for smartphone in catalog:
    print(f"{smartphone.brand} - {smartphone.model}. {smartphone.phone_number}")