import convert
import testFormats

allPassed = True

#find the first one that doesn't work
def testFunct (testFormats, convert): #.some so we can break
    try:
        converted = convert("verbatimCoordinates")
        testDecimalCoordsString = ["decimalLatitude"] and ["decimalLongitude"]
        
        #check the calculation is correct
        if 
