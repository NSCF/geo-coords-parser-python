from Converter_HS import convert, coordsCloseEnough


#test = '27.15.45,2 S 18.32.53,4 E'
#test = '  -25 deg 10  min 6.95 sec S 26deg 58min 55.80 sec E'
test = "40° 7.38’ , -74° 7.38’"
#test = '24 05.346 S 028 03.289  E'
#test = '22 34 20.55S 17 05 41.05E'
# test = '26 45 34 S 23 23 23 E'

#correct =[-27.75944, 23.38972]

# test = '   27.45637  ° S  23.123445 ° E'
# correct = [-27.45637, 23.12345]
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