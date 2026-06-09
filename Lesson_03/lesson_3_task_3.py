from Address import Address
from Mailing import Mailing


from_addr = Address("123456", "Москва", "Тверская", "15", "10")
to_addr = Address("654321", "Санкт-Петербург", "Невский проспект", "20", "5")


mailing = Mailing(
    to_address=to_addr,
    from_address=from_addr,
    cost=9999999,
    track="TRACK123456789"
)


print(f"Отправление {mailing.track} из {mailing.from_address.index}, "
      f"{mailing.from_address.city}, {mailing.from_address.street}, "
      f"{mailing.from_address.house} - {mailing.from_address.apartment} "
      f"в {mailing.to_address.index}, {mailing.to_address.city}, "
      f"{mailing.to_address.street}, {mailing.to_address.house} - "
      f"{mailing.to_address.apartment}. Стоимость {mailing.cost} рублей.")