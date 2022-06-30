from Converter_HS import convert, coordsCloseEnough
import json

with open("testFormats.json", encoding='utf-8') as file:
    test = json.load(file)

allPassed = True

for dict in test:
    try:
        converted = convert(dict.get("verbatimCoordinates"))
        #print(converted)
        correctlyConverted = coordsCloseEnough(converted[0],converted[1],dict.get("decimalLatitude"),dict.get("decimalLongitude"))
        if not correctlyConverted:
            print(str(dict) + str(converted[0]) + ' ' + str(converted[1]) +" " + "Conversion was incorrect") 
            allPassed = False        
    except Exception as e:
        print('converter threw exception for', dict.get("verbatimCoordinates"))
        allPassed = False

if(allPassed):
    print('All coordinates converted successfully')


