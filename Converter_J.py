import re
import math
from unicodedata import decimal
# from toCoordinateFormat import *

# Coordinates pattern matching regex
dd_re = "(NORTH|SOUTH|[NS])?[\s]*([+-]?[0-8]?[0-9](?:[\.,]\d{3,}))([•º°]?)[\s]*(NORTH|SOUTH|[NS])?[\s]*[,/;]?[\s]*(EAST|WEST|[EW])?[\s]*([+-]?[0-1]?[0-9]?[0-9](?:[\.,]\d{3,}))([•º°]?)[\s]*(EAST|WEST|[EW])?"

# degrees minutes seconds with '.' as separator - gives array with 15 values
dms_periods = "/(NORTH|SOUTH|[NS])?[\ \t]*([+-]?[0-8]?[0-9])[\ \t]*(\.)[\ \t]*([0-5]?[0-9])[\ \t]*(\.)?[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(NORTH|SOUTH|[NS])?(?:[\ \t]*[,/;][\ \t]*|[\ \t]*)(EAST|WEST|[EW])?[\ \t]*([+-]?[0-1]?[0-9]?[0-9])[\ \t]*(\.)[\ \t]*([0-5]?[0-9])[\ \t]*(\.)?[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(EAST|WEST|[EW])?/i"

# degrees minutes seconds with words 'degrees, minutes, seconds' as separators (needed because the s of seconds messes with the S of SOUTH) - gives array of 17 values
dms_abbr = "/(NORTH|SOUTH|[NS])?[\ \t]*([+-]?[0-8]?[0-9])[\ \t]*(D(?:EG)?(?:REES)?)[\ \t]*([0-5]?[0-9])[\ \t]*(M(?:IN)?(?:UTES)?)[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(S(?:EC)?(?:ONDS)?)?[\ \t]*(NORTH|SOUTH|[NS])?(?:[\ \t]*[,/;][\ \t]*|[\ \t]*)(EAST|WEST|[EW])?[\ \t]*([+-]?[0-1]?[0-9]?[0-9])[\ \t]*(D(?:EG)?(?:REES)?)[\ \t]*([0-5]?[0-9])[\ \t]*(M(?:IN)?(?:UTES)?)[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(S(?:EC)?(?:ONDS)?)[\ \t]*(EAST|WEST|[EW])?/i"

#everything else - gives array of 17 values; ADDED BACK SLASHES FOR INVERTED COMMAS!
coords_other = "/(NORTH|SOUTH|[NS])?[\ \t]*([+-]?[0-8]?[0-9])[\ \t]*([•º°\.:]|D(?:EG)?(?:REES)?)?[\ \t]*,?([0-5]?[0-9](?:\.\d{1,})?)?[\ \t]*(['′´’\.:]|M(?:IN)?(?:UTES)?)?[\ \t]*,?((?:[0-5]?[0-9])(?:\.\d{1,3})?)?[\ \t]*(''|′′|’’|´´|[\"″”\.])?[\ \t]*(NORTH|SOUTH|[NS])?(?:\s*[,/;]\s*|\s*)(EAST|WEST|[EW])?[\ \t]*([+-]?[0-1]?[0-9]?[0-9])[\ \t]*([•º°\.:]|D(?:EG)?(?:REES)?)?[\ \t]*,?([0-5]?[0-9](?:\.\d{1,})?)?[\ \t]*(['′´’\.:]|M(?:IN)?(?:UTES)?)?[\ \t]*,?((?:[0-5]?[0-9])(?:\.\d{1,3})?)?[\ \t]*(''|′′|´´|’’|[\"″”\.])?[\ \t]*(EAST|WEST|[EW])?/i"

# Function for converting coordinates in a variety of formats to decimal coordinates
# @param {string} coordsString The coordinates string to convert
# @param {number} decimalPlaces The number of decimal places for converted coordinates; default is 5
# @returns {object} { verbatimCoordinates, decimalCoordinates, decimalLatitude, decimalLongitude }#

def convert(coordsString, decimalPlaces=5): #why use convert instead of converter like in JS?
    # TODO add exact match to entered string, so that it can be used to filter out superflous text around it
    # if not decimalPlaces:
    #     decimalPlaces = 5
    # why comment out this if statement?
    
    coordsString = re.sub("/\s+/", " ", coordsString).strip(); #just to tidy up whitespaces
    
    ddLat = None
    ddLng = None
    latdir = ""
    lngdir = ""
    match = []
    matchSuccess = False
    
    if re.search(dd_re, coordsString, re.I): # .search() returns only first match
        match = re.match(dd_re, coordsString, re.I) 
        #matchSuccess = checkMatch(match)
        
        if match:
            matchSuccess = True
            ddLat = match[2]
            ddLng = match[6]
            
            # need to fix if there are ','s instead of '.'
            if ',' in ddLat:
                ddLat = ddLat.replace(',','.')
                ddLat = float(ddLat)
            
            if ',' in ddLng:
                ddLng = ddLng.replace(',', '.')
                ddLng = float(ddLng)
            
            # get directions
            if match[1]:
                latdir = match[1]
                lngdir = match[5]
            elif match[4]:
                latdir = match[4]
                lngdir = match[8]
        else:
            raise TypeError("invalid decimal coordinate format") # correct error type? Should it be ValueError?
    
    elif re.search(dms_periods, coordsString, re.I):
        match = dms_periods.match(dms_periods, coordsString, re.I)
        matchSuccess = checkMatch(match)
        
        if matchSuccess:
            ddLat = abs(int(match.group(2)))
            if match[4]:
                ddLat += match[4]/60
            if match[6]:
                ddLat += match[6]/3600
            if int(match.group(2)) < 0:
                ddLat = -1 * ddLat
                ddLng = abs(int(match[9]).group())
            if match[11]:
                ddLng += match[11]/60
            if match[13]:
                ddLng += match[13]/3600
            if int(match[9]).group() < 0:
                ddLng = -1 * ddLng
            
            if match[1]:
                latdir = match[1]
                lngdir = match[8]
            elif match[7]:
                latdir = match[7]
                lngdir = match[14]
        else:
            raise TypeError("invalid DMS coordinates format") # correct error type? Should it be ValueError?
    
    elif re.search(dms_abbr, coordsString, re.I):
        match = dms_abbr.match(dms_abbr, coordsString, re.I)
        matchSuccess = checkMatch(match)
        
        if matchSuccess:
            ddLat = abs(int(match[2]).group())
            if match[4]:
                ddLat += match[4]/60
                if not match[3]:
                    match[3] = ' '
            if match[6]:
                ddLat += match[6]/3600
                if not match[5]:
                    match[5] = ' '
            if int(re.search(r'\d+', match[2]).group()) < 0:
                ddLat = -1 * ddLat
                ddLng = abs(int(re.search(r'\d+', match[10]).group()))
            if match[12]:
                ddLng += match[12]/60
                if not match[11]:
                    match[11] = ' '
            if match[14]:
                ddLng += match[14]/3600
                if not match[13]:
                    match[13] = ' '
            if int(re.search(r'\d+', match[10]).group()) < 0:
                ddLng = -1 * ddLng
                
            if match[1]:
                latdir = match[1]
                lngdir = match[9]
            elif match[8]:
                latdir = match[8]
                lngdir = match[16]
        else:
            raise TypeError("invalid DMS coordinates format") # correct error type? Should it be ValueError?
    
    elif re.search(coords_other, coordsString, re.I):
        match = coords_other.match(coords_other, coordsString, re.I)
        matchSuccess = checkMatch(match)
        
        if matchSuccess:
            ddLat = abs(int(re.search(r'\d+', match[2]).group()))
            if match[4]:
                ddLat += match[4]/60
                if not match[3]:
                    match[3] = ' '
            if match[6]:
                ddLat += match[6]/3600
                if not match[5]:
                    match[5] = ' '
            if int(re.search(r'\d+', match[2]).group()) < 0:
                ddLat = -1 * ddLat
                ddLng = abs(int(re.search(r'\d+', match[10]).group()))
            if match[12]:
                ddLng += match[12]/60
                if not match[11]:
                    match[11] = ' '
            if match[14]:
                ddLng += match[14]/3600
                if not match[13]:
                    match[13] = ' '
            if int(re.search(r'\d+', match[10]).group()) < 0:
                ddLng = -1 * ddLng
            
            if match[1]:
                latdir = match[1]
                lngdir = match[9]
            elif match[8]:
                latdir = match[8]
                lngdir = match[16]
        else:
            raise TypeError("invalid coordinates format") # correct error type? Should it be ValueError?
    
    # check longitude value - it can be wrong!
    if abs(ddLng) >= 180:
        raise ValueError("invalid longitude value")
    
    if matchSuccess:
        # make sure the signs and cardinal directions match
        #patt = "/S|SOUTH/i"
        patt = re.compile("S|SOUTH|s")

        if patt.search(latdir):
            if ddLat > 0:
                ddLat = -1 * ddLat
            
        #patt = "/W|WEST/i;"
        patt = re.compile("W|WEST|s;")
        if patt.search(lngdir):
            if ddLng > 0:
                ddLng = -1 * ddLng
        
        # we need to get the verbatim coords from the string
        # we can't split down the middle because if there are decimals they may have different numbers on each side
        # so we need to find the separating character, or if none, use the match values to split down the middle

        verbatimCoordinates = match[0].strip()
        verbatimLat = None
        verbatimLng = None
        sepChars = re.compile("/[,/;\u0020]/g") #comma, forward slash and spacebar
        seps = sepChars.match(verbatimCoordinates)

        if seps == None:
            # split down the middle
            middle = round(len(coordsString)/2)
            verbatimLat = verbatimCoordinates[0:middle].strip()
            verbatimLng = verbatimCoordinates[middle+1:].strip()
        else:          # if length is odd then find the index of the middle value
            #get the middle index
            middle = None
            #easy for odd numbers
            if (len(seps) % 2) == 1:
                middle = len(seps)/2
            else:
                middle = (len(seps)/2) -1
            
            # walk through seps until we get to the middle
            splitIndex = 0

            # it might be only one value
            if middle == 0:
                splitIndex = verbatimCoordinates.index(seps[0])
                verbatimLat = verbatimCoordinates[0:splitIndex].strip()
                verbatimLng = verbatimCoordinates[splitIndex + 1:].strip()
            else:
                currSepIndex = 0
                startSearchIndex = 0
                while currSepIndex <= middle:
                    splitIndex = verbatimCoordinates.index(seps[currSepIndex], startSearchIndex)
                    startSearchIndex = splitIndex + 1
                    currSepIndex += 1
                
                verbatimLat = verbatimCoordinates[0:splitIndex].strip()
                verbatimLng = verbatimCoordinates[splitIndex + 1:].strip()
        
        # All done!!
        # just truncate the decimals appropriately
        if math.isnan(ddLat) and ',' in ddLat:
            ddLat = ddLat.replace(',', '.')
        
        ddLat = round(ddLat,decimalPlaces)

        if math.isnan(ddLng) and ',' in ddLng:
            ddLng = ddLng.replace(',', '.')

        ddLng = round(ddLng,decimalPlaces)

        return [ddLat,ddLng, latdir,lngdir]   
        # FIGURE OUT HOW TO DO RETURN HERE!!!!!!!!!!!! 
    else:
        raise ValueError("coordinates pattern match failed") #correct error type?

def checkMatch(match): #test if the matched groups arrays are 'balanced'. match is the resulting array
    if not math.isnan(match.group(1)): #we've matched a number, not what we want..
        return False
    
    #first remove the empty values from the array
    filteredMatch = [x for x in match if x != ""] #CHECK THIS

    #we need to shift the array because it contains the whole coordinates string in the first item
    newFilteredMatch = filteredMatch.pop(0)

    
    #if minutes or seconds are out of bounds, the array length is wrong
    # if (filteredMatch.length == 4) {
    #     return false
    # }

    #then check the array length is an even number else exit
    if (len(filteredMatch) % 2) > 0:
        return False

    #regex for testing corresponding values match
    numerictest = "/^[-+]?(\d+|\d+\.\d*|\d*\.\d+)$/" #for testing numeric values
    stringtest = "/[A-Za-z]+/" #strings - the contents of strings are already matched when this is used

    halflen = len(newFilteredMatch)/2
    result = True
    for i in range(0, halflen+1):
        if numerictest.search(newFilteredMatch[i]) != numerictest.search(newFilteredMatch[i+halflen]) or stringtest.search(newFilteredMatch[i] != stringtest.search(newFilteredMatch[i+halflen])):
            result = False
            break
    
    return result

# functions for coordinate validation

# as decimal arithmetic is not straightforward, we approximate

def decimalsCloseEnough(dec1, dec2):
    originaldiff = abs(dec1 - dec2)
    diff = int(round(originaldiff, 6))
    if diff == 0.00001:
        return True
    else:
        return False

def coordsCloseEnough(coordsToTest):
    if ',' in coordsToTest:
        coords = coordsToTest.split(',')
        if math.isnan(int(coords[0])) == True or math.isnan(int(coords[1])) == True:
            raise ValueError("coords are not valid decimals") # check is error type is correct
        # else:
            # return decimalsCloseEnough(this.decimalLatitude, int(coords[0])) and decimalsCloseEnough(this.decimalLongitude, coords[1]) # this here will be the converted coordinates object
            # CHECK HOW TO DO .this IN PYTHON
    else:
        raise ValueError("coords being tested must be separated by a comma") # check if error type is correct




# CONVERT BELOW TO PYTHON
# to = Object.freeze({
#   DMS: 'DMS',
#   DM: 'DM'
# })

# converter.to = to

# module.exports = converter
