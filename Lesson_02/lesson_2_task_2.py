def is_year_leap(year):
    return year % 4 == 0

test_year = 2026
result = is_year_leap(test_year)
print(f"год {test_year}: {result}")