from Converter_HS import convert, coordsCloseEnough


#test = '27.15.45,2S 18.32.53,4E'
#test = '-25deg 10min 6.95sec S 26deg 58min 55.80sec E'

#test = '24 05.346S 028 03.289E'
#test = '22 34 20.55 S 17 05 41.05 E'
test = '26 45 34 S 23 23 23 E'
correct =[-27.75944, 23.38972]
# test = '   27.45637° S  23.123445° E'
# test = '-25.5589167 31.0113888'


#converted = convert(test)

try:
    converted = convert(test)
    print(converted)
    correctlyConverted = coordsCloseEnough(converted[0],converted[1],correct[0],correct[1])
    if correctlyConverted:
        print("Conversion was correct")
    else:
        print("Conversion was incorrect")
except Exception as e:
    print(e)