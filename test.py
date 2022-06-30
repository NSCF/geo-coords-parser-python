from Converter_HS import convert, coordsCloseEnough
import json

with open("testFormats.json", encoding='utf-8') as file:
    test = json.load(file)
    print(test)

allPassed = True

for dict in test:
    try:
        converted = convert(dict.get("verbatimCoordinates"))
        #print(converted)
        correctlyConverted = coordsCloseEnough(converted[0],converted[1],dict.get("decimalLatitude"),dict.get("decimalLongitude"))
        if correctlyConverted:
            print("Conversion was correct")
        else:
            print(str(dict) + str(converted[0]) + ' ' + str(converted[1]) +" " + "Conversion was incorrect")
    except Exception as e:
        print(e)


