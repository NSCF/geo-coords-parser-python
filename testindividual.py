from Converter_HS import convert
#test = '-27.45.34 S 23.23.23 E'
#test = '-25deg 10min 6.95sec S 26deg 58min 55.80sec E'

#test = '24 05.346S 028 03.289E'
#test = '22 34 20.55 S 17 05 41.05 E'

# test = '   27.45637° S  23.123445° E'
# test = '-25.5589167 31.0113888'
test = '-27 45 34 S 23 23 23 E'

#converted = convert(test)

try:
    converted = convert(test)
    print(converted)
except Exception as e:
    print(e)