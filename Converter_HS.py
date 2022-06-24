import re
import math
# from toCoordinateFormat import *

# Coordinates pattern matching regex
#Decimal degrees
dd_re = "(NORTH|SOUTH|[NS])?[\s]*([+-]?[0-8]?[0-9](?:[\.,]\d{3,}))([•º°]?)[\s]*(NORTH|SOUTH|[NS])?[\s]*[,/;]?[\s]*(EAST|WEST|[EW])?[\s]*([+-]?[0-1]?[0-9]?[0-9](?:[\.,]\d{3,}))([•º°]?)[\s]*(EAST|WEST|[EW])?"

# degrees minutes seconds with '.' as separator - gives array with 15 values
#dms_periods = "(NORTH|SOUTH|[NS])?[\ \t]*([+-]?[0-8]?[0-9])[\ \t]*(\.)[\ \t]*([0-5]?[0-9])[\ \t]*(\.)?[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(NORTH|SOUTH|[NS])?(?:[\ \t]*[,/;][\ \t]*|[\ \t]*)(EAST|WEST|[EW])?[\ \t]*([+-]?[0-1]?[0-9]?[0-9])[\ \t]*(\.)[\ \t]*([0-5]?[0-9])[\ \t]*(\.)?[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(EAST|WEST|[EW])?"
dms_periods = "(NORTH|SOUTH|[NS])?\s*([+-]?[0-8]?[0-9])\s*(\.)\s*([0-5]?[0-9])\s*(\.)\s*((?:[0-5]?[0-9])(?:[\.,]\d{1,3})?)?\s*(NORTH|SOUTH|[NS])?(?:\s*[,/;]\s*|\s*)(EAST|WEST|[EW])?\s*([+-]?[0-1]?[0-9]?[0-9])\s*(\.)\s*([0-5]?[0-9])\s*(\.)\s*((?:[0-5]?[0-9])(?:[\.,]\d{1,3})?)?\s*(EAST|WEST|[EW])?"

# degrees minutes seconds with words 'degrees, minutes, seconds' as separators (needed because the s of seconds messes with the S of SOUTH) - gives array of 17 values
dms_abbr = "(NORTH|SOUTH|[NS])?[\ \t]*([+-]?[0-8]?[0-9])[\ \t]*(D(?:EG)?(?:REES)?)[\ \t]*([0-5]?[0-9])[\ \t]*(M(?:IN)?(?:UTES)?)[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(S(?:EC)?(?:ONDS)?)?[\ \t]*(NORTH|SOUTH|[NS])?(?:[\ \t]*[,/;][\ \t]*|[\ \t]*)(EAST|WEST|[EW])?[\ \t]*([+-]?[0-1]?[0-9]?[0-9])[\ \t]*(D(?:EG)?(?:REES)?)[\ \t]*([0-5]?[0-9])[\ \t]*(M(?:IN)?(?:UTES)?)[\ \t]*((?:[0-5]?[0-9])(?:\.\d{1,3})?)?(S(?:EC)?(?:ONDS)?)[\ \t]*(EAST|WEST|[EW])?"

#everything else - gives array of 17 values; ADDED BACK SLASHES FOR INVERTED COMMAS!
coords_other = "(NORTH|SOUTH|[NS])?[\ \t]*([+-]?[0-8]?[0-9])[\ \t]*([•º°\.:]|D(?:EG)?(?:REES)?)?[\ \t]*,?([0-5]?[0-9](?:\.\d{1,})?)?[\ \t]*(['′´’\.:]|M(?:IN)?(?:UTES)?)?[\ \t]*,?((?:[0-5]?[0-9])(?:\.\d{1,3})?)?[\ \t]*(''|′′|’’|´´|[\"″”\.])?[\ \t]*(NORTH|SOUTH|[NS])?(?:\s*[,/;]\s*|\s*)(EAST|WEST|[EW])?[\ \t]*([+-]?[0-1]?[0-9]?[0-9])[\ \t]*([•º°\.:]|D(?:EG)?(?:REES)?)?[\ \t]*,?([0-5]?[0-9](?:\.\d{1,})?)?[\ \t]*(['′´’\.:]|M(?:IN)?(?:UTES)?)?[\ \t]*,?((?:[0-5]?[0-9])(?:\.\d{1,3})?)?[\ \t]*(''|′′|´´|’’|[\"″”\.])?[\ \t]*(EAST|WEST|[EW])?"

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
    match = None
    matchSuccess = False
    
    if re.search(dd_re, coordsString, re.I): # .search() returns only first match
        match = re.match(dd_re, coordsString, re.I) 
        matchSuccess = checkMatch(match)
        
        if matchSuccess == True:
            ddLat = match.group(2)
            ddLng = match.group(6)
                        
            # need to fix if there are ','s instead of '.'
            if ',' in ddLat:
                ddLat = ddLat.replace(',','.')

            if ',' in ddLng:
                ddLng = ddLng.replace(',', '.')
                
            # get directions
            if match.group(1):
                latdir = match.group(1)
                lngdir = match.group(5)
            elif match.group(4):
                latdir = match.group(4)
                lngdir = match.group(8)
        else:
            raise Exception("invalid decimal coordinate format") # correct error type? Should it be ValueError?
    

    elif re.search(dms_periods, coordsString, re.I):
        match = re.match(dms_periods, coordsString, re.I)
        matchSuccess = checkMatch(match)
        
        if matchSuccess:
            ddLat = abs(int(match.group(2)))

            if match[4]:
                ddLat += int(match[4])/60
            if match[6]:
                latdec = match[6].replace(',', '.')
                ddLat += float(latdec)/3600

            if int(match.group(2)) < 0:
                ddLat = -1 * ddLat

            ddLng = abs(int(match[9]))

            if match[11]:
                ddLng += int(match[11])/60
            if match[13]:
                lngdec = match[13].replace(',', '.')
                ddLng += float(lngdec)/3600
                

            if int(match[9]) < 0:
                ddLng = -1 * ddLng
            
            if match[1]:
                latdir = match[1]
                lngdir = match[8]
            elif match[7]:
                latdir = match[7]
                lngdir = match[14]

            #we have to catch an edge case where we have same or missing direction indicators
            if (latdir == '' or lngdir == '') or (latdir == lngdir):
               raise Exception("invalid DMS coordinates format") 
            
        else:
            raise Exception("invalid DMS coordinates format") # correct error type? 
    

    elif re.search(dms_abbr, coordsString, re.I):
        match = re.match(dms_abbr, coordsString, re.I)
        matchSuccess = checkMatch(match)
        
        if matchSuccess:
            ddLat = abs(int(match.group(2)))
            if match[4]:
                ddLat += int(match[4])/60
                if not match[3]:
                    match[3] = ' '
            if match[6]:
                ddLat += float(match[6])/3600
                if not match[5]:
                    match[5] = ' '
            if int(match.group(2)) < 0:
                ddLat = -1 * ddLat
            
            ddLng = abs(int(match.group(10)))
            if match[12]:
                ddLng += int(match[12])/60
                if not match[11]:
                    match[11] = ' '
            if match[14]:
                ddLng += float(match[14])/3600
                if not match[13]:
                    match[13] = ' '
            if int(match.group(10)) < 0:
                ddLng = -1 * ddLng
                            
            if match[1]:
                latdir = match[1]
                lngdir = match[9]
            elif match[8]:
                latdir = match[8]
                lngdir = match[16]
        else:
            raise Exception("invalid DMS coordinates format") # correct error type? 
    

    elif re.search(coords_other, coordsString, re.I):
        match = re.match(coords_other, coordsString, re.I)
        matchSuccess = checkMatch(match)
        
        if matchSuccess:
            ddLat = abs(int(match.group(2))) # Error "'re.Match' object does not support item assignment"

            if match[4]:
                ddLat += int(match[4])/60
                if not match[3]:
                    match[3] = ' '
            if match[6]:
                ddLat += float(match[6])/3600
                if not match[5]:
                    match[5] = ' '
            if int(match.group(2)) < 0:
                    ddLat = -1 * ddLat
            
            ddLng = abs(int(match.group(10)))
            if match[12]:
                ddLng += int(match[12])/60
                if not match[11]:
                    match[11] = ' '
            if match[14]:
                ddLng += float(match[14])/3600
                if not match[13]:
                    match[13] = ' '
            if int(match.group(10)) < 0:
                    ddLat = -1 * ddLng
                       
            if match[1]:
                latdir = match[1]
                lngdir = match[9]
            elif match[8]:
                latdir = match[8]
                lngdir = match[16]
        else:
            raise Exception("invalid coordinates format") # correct error type? 
    
    # check longitude value - it can be wrong!
    if abs(float(ddLng)) >= 180:
        raise Exception("invalid longitude value")

    ddLat = float(ddLat)
    ddLng = float(ddLng)
    if matchSuccess:
        # make sure the signs and cardinal directions match
        patt = "(S|SOUTH)"
        if re.search(patt, latdir, re.I):
            if ddLat > 0:
                ddLat = -1 * ddLat
            
        patt = "(W|WEST)"
        if re.search(patt, lngdir, re.I):
            if ddLng > 0:
                ddLng = -1 * ddLng
        
        # we need to get the verbatim coords from the string
        # we can't split down the middle because if there are decimals they may have different numbers on each side
        # so we need to find the separating character, or if none, use the match values to split down the middle

        # verbatimCoordinates = match[0].strip()
        # verbatimLat = None
        # verbatimLng = None
        # sepChars = "/[,/;\u0020]/g" #comma, forward slash and spacebar
        # seps = verbatimCoordinates.match(sepChars)

        # if seps == None:
        #     # split down the middle
        #     middle = len(coordsString)/2
        #     verbatimLat = verbatimCoordinates[0:middle].strip()
        #     verbatimLng = verbatimCoordinates[middle].strip()
        # else:          # if length is odd then find the index of the middle value
        #     #get the middle index
        #     middle = None
        #     #easy for odd numbers
        #     if (len(seps) % 2) == 1:
        #         middle = len(seps)/2
        #     else:
        #         middle = (len(seps)/2) -1
            
        #     # walk through seps until we get to the middle
        #     splitIndex = 0

        #     # it might be only one value
        #     if middle == 0:
        #         splitIndex = verbatimCoordinates.index(seps[0])
        #         verbatimLat = verbatimCoordinates[0:splitIndex].strip()
        #         verbatimLng = verbatimCoordinates[splitIndex + 1].strip()
        #     else:
        #         currSepIndex = 0
        #         startSearchIndex = 0
        #         while currSepIndex <= middle:
        #             splitIndex = verbatimCoordinates.index(seps[currSepIndex], startSearchIndex)
        #             startSearchIndex = splitIndex + 1
        #             currSepIndex += 1
                
        #         verbatimLat = verbatimCoordinates[0:splitIndex].strip()
        #         verbatimLng = verbatimCoordinates[splitIndex + 1].strip()
        
        # All done!!
        # just truncate the decimals appropriately
        if math.isnan(ddLat) and ',' in ddLat:
            ddLat = ddLat.replace(',', '.')
        
        ddLat = round(ddLat, decimalPlaces)

        if math.isnan(ddLng) and ',' in ddLng:
            ddLng = ddLng.replace(',', '.')

        ddLng = round(ddLng, decimalPlaces)

        return [ddLat,ddLng]  
        
    else:
        raise Exception("coordinates pattern match failed") #correct error type?

def checkMatch(match): #test if the matched groups arrays are 'balanced'. match is the resulting array
        
    groups = match.groups()
    filteredMatch = []
    for item in groups:
        if item is None or item.strip() == "":
            continue
        else:
            filteredMatch.append(item.strip())  

                    
          
    #if minutes or seconds are out of bounds, the array length is wrong
    # if (filteredMatch.length == 4) {
    #     return false
    # }

    #then check the array length is an even number else exit
    if (len(filteredMatch) % 2) > 0:
        return False

    #regex for testing corresponding values match
    numerictest = "^[-+]?\d+([\.,]{1}\d+)$" #for testing numeric values
   
    halflen = int(len(filteredMatch)/2)
    
    for i in range(0, halflen+1):
        leftside = filteredMatch[i]
        rightside = filteredMatch[i + halflen]
        if ((re.match(numerictest, leftside) and re.match(numerictest, rightside)) or (type(leftside)== str and type(rightside) == str) or leftside == rightside):
            return True
           
        else:
            return False

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
            raise Exception("coords are not valid decimals") # check is error type is correct
        # else:
            # return decimalsCloseEnough(this.decimalLatitude, int(coords[0])) and decimalsCloseEnough(this.decimalLongitude, coords[1]) # this here will be the converted coordinates object
            # CHECK HOW TO DO .this IN PYTHON
    else:
        raise Exception("coords being tested must be separated by a comma") # check if error type is correct




