from converter import convert, coordsCloseEnough
import json

with open("testFormats.json", encoding='utf-8') as file:
  test = json.load(file)

allPassed = True

for dict in test:
  try:
    converted = convert(dict.get("verbatimCoordinates"))
    #print(converted)
    correctlyConverted = coordsCloseEnough(converted["decimalLatitude"],converted["decimalLongitude"],dict.get("decimalLatitude"),dict.get("decimalLongitude"))
    if not correctlyConverted:
      print(str(dict) + str(converted["decimalLatitude"]) + ' ' + str(converted["decimalLongitude"]) +" " + "Conversion was incorrect") 
      allPassed = False        
  except Exception as e:
    print('converter threw exception for', dict.get("verbatimCoordinates"))
    allPassed = False

if  allPassed:
  print('All coordinates converted successfully that should have')


failingFormats = [
  '50°4\'17.698"south, 24.34532', #different formats on each side
  '90°4\'17.698"south, 23°4\'17.698"east', #latitude out of bounds
  '89°4\'17.698"south, 183°4\'17.698"east', #longitude out of bounds
  '50°4\'17.698"east, 23°4\'17.698"south', #directions wrong way round
  'E23.34355,S25.324234', # directions wrong way round
  '23°45\'12.2\'\'S 18.33\'56.7\'\'E', #symbols don't match
  'S 27.45.34 23.23.23', #missing direction on right side
  'S 27.45.34 S 23.23.23', #invalid direction on right side
  'S 90°4\'17.698" S 23°4\'17.698"',
  '27.45.34 S S 23.23.23', #invalid direction on right side
  '27.45.34  23.23.23 E'] #no dir on one side

allPassed = True
for dict  in failingFormats:
  try:
    converted = convert(dict)
    print(dict.get("verbatimCoordinates"), "should not have converted") 
    allPassed = False         
  except Exception as e:
    continue

if allPassed == True:
  print('All failingformats failed as expected')





