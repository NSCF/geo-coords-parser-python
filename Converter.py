import re
import math
from regex import dd_re, dms_periods, dms_abbr, coords_other

# Function for converting coordinates in a variety of formats to decimal coordinates
# @param {string} coordsString The coordinates string to convert
# @param {number} decimalPlaces The number of decimal places for converted coordinates; default is 5
# @returns {object} { verbatimCoordinates, decimalCoordinates, decimalLatitude, decimalLongitude }#

def convert(coordsString, decimalPlaces=5): #why use convert instead of converter like in JS?
  # TODO add exact match to entered string, so that it can be used to filter out superflous text around it
  
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
      raise Exception("invalid decimal coordinate format") 
  

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
      raise Exception("invalid DMS coordinates format") 
  

  elif re.search(dms_abbr, coordsString, re.I):
    match = re.match(dms_abbr, coordsString, re.I)
    matchSuccess = checkMatch(match)
    
    if matchSuccess:
      ddLat = abs(int(match.group(2)))
      if match[4]:
        ddLat += int(match[4])/60
          
      if match[6]:
        ddLat += float(match[6])/3600
          
      if int(match.group(2)) < 0:
        ddLat = -1 * ddLat
      
      ddLng = abs(int(match.group(10)))
      if match[12]:
        ddLng += int(match[12])/60
          
      if match[14]:
        ddLng += float(match[14])/3600
          
      if int(match.group(10)) < 0:
        ddLng = -1 * ddLng
                      
      if match[1]:
        latdir = match[1]
        lngdir = match[9]
      elif match[8]:
        latdir = match[8]
        lngdir = match[16]
    else:
      raise Exception("invalid DMS coordinates format") 
  

  elif re.search(coords_other, coordsString, re.I):
    match = re.match(coords_other, coordsString, re.I)
    matchSuccess = checkMatch(match)
    
    if matchSuccess:
      ddLat = abs(int(match.group(2))) 

      if match.group(4):
        ddLat += float(match[4])/60
          
      if match[6]:
        ddLat += float(match[6])/3600
          
      if int(match.group(2)) < 0:
        ddLat = -1 * ddLat
      
      ddLng = abs(int(match.group(10)))
      if match[12]:
        ddLng += float(match[12])/60
          
      if match[14]:
        ddLng += float(match[14])/3600
          
      if int(match.group(10)) < 0:
        ddLng = -1 * ddLng
                  
      if match[1]:
        latdir = match[1]
        lngdir = match[9]
      elif match[8]:
        latdir = match[8]
        lngdir = match[16]
    else:
      raise Exception("invalid coordinates format") 
  
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
    # we can't split down the middle because if there are decimals they may have different precision on each side
    # so we need to find the separating character, or if none, use the match values to split down the middle
    verbatimCoordinates = match[0].strip()
    verbatimLat = None
    verbatimLng = None

    sepChars = "[,;\s+/]" #comma, semicolon, forward slash and spacebar
    seps = list(re.finditer(sepChars, verbatimCoordinates)) #seps is a list of Matches, and Matches remember where they found the char in the string

    if len(seps) == 0:
      # split down the middle
      middle = int(len(coordsString)/2)
      verbatimLat = verbatimCoordinates[:middle].strip()
      verbatimLng = verbatimCoordinates[middle:].strip()
      i = 1
    else:  
      # get the middle index of the returned seps
      if len(seps) == 1:
        middle = seps[0].span()[0] #span gets the position of the char in the string
        verbatimLat = verbatimCoordinates[:middle].strip()
        verbatimLng = verbatimCoordinates[(middle + 1):].strip()
      
      # if length is odd then find the index of the middle value
      if (len(seps) % 2) == 1:
        middleSep = seps[len(seps)//2] #// is floor
        middle = middleSep.span()[0]
        verbatimLat = verbatimCoordinates[:(middle)].strip()
        verbatimLng = verbatimCoordinates[(middle + 1):].strip()

      else:
        middleSep = seps[(len(seps)//2) - 1]
        middle = middleSep.span()[0] 
        verbatimLat = verbatimCoordinates[:(middle)].strip()
        verbatimLng = verbatimCoordinates[(middle + 1):].strip()

    verbatimLat = re.sub(sepChars + "+$", "", verbatimLat)
    verbatimLng = re.sub("^" + sepChars + "+", "", verbatimLng)

    #ALL DONE!
    # just truncate the decimals appropriately
    if math.isnan(ddLat) and ',' in ddLat:
      ddLat = ddLat.replace(',', '.')
    
    ddLat = round(ddLat, decimalPlaces)

    if math.isnan(ddLng) and ',' in ddLng:
      ddLng = ddLng.replace(',', '.')

    ddLng = round(ddLng, decimalPlaces)

    return {
        "verbatimCoordinates":verbatimCoordinates,
        "verbatimLatitude":verbatimLat,
        "verbatimLongitude":verbatimLng,
        "decimalLatitude":ddLat, 
        "decimalLongitude":ddLng,
        "decimalCoordinates":str(ddLat) + ", " + str(ddLng)
        }   
  else:
      raise Exception("coordinates pattern match failed") 

def checkMatch(match): #test if the matched groups arrays are 'balanced'. match is the resulting array
      
  groups = match.groups()
  filteredMatch = []
  for item in groups:
    if item is None or item.strip() == "":
      continue
    else:
      filteredMatch.append(item.strip())                 

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
  if diff <= 0.00001:
    return True
  else:
    return False

def coordsCloseEnough(convertedLatitude, convertedLongitude, correctLatitude, correctLongitude):
  if isinstance(convertedLatitude, float) and isinstance(convertedLongitude, float) and isinstance(correctLatitude, float) and isinstance(correctLongitude, float):
    return decimalsCloseEnough(convertedLatitude, correctLatitude) and decimalsCloseEnough(convertedLongitude, correctLongitude) # this here will be the converted coordinates object
  else:
    raise Exception("coords are not valid decimals")

      




