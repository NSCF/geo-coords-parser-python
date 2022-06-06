//return an array of coordinate strings for testing


//coordinations-parser formats
//https://www.npmjs.com/package/coordinate-parser
var coordsParserFormats = [
  {
    verbatimCoordinates: '40.123, -74.123',
    verbatimLatitude: '40.123', 
    verbatimLongitude: '-74.123' 
  },
  {
    verbatimCoordinates: '40.123° N 74.123° W',
    verbatimLatitude: '40.123° N', 
    verbatimLongitude: '74.123° W'
  },
  {
    verbatimCoordinates: '40.123° N 74.123° W',
    verbatimLatitude: '40.123° N', 
    verbatimLongitude: '74.123° W'
  },
  {
    verbatimCoordinates: '40° 7´ 22.8" N 74° 7´ 22.8" W',
    verbatimLatitude: '40° 7´ 22.8" N', 
    verbatimLongitude: '74° 7´ 22.8" W'
  },
  {
    verbatimCoordinates: '40° 7.38’ , -74° 7.38’',
    verbatimLatitude: '40° 7.38’', 
    verbatimLongitude: '-74° 7.38’'
  },
  {
    verbatimCoordinates: 'N40°7’22.8’’, W74°7’22.8’’',
    verbatimLatitude: 'N40°7’22.8’’', 
    verbatimLongitude: 'W74°7’22.8’’'
  },
  {
    verbatimCoordinates: '40°7’22.8"N, 74°7’22.8"W',
    verbatimLatitude: '40°7’22.8"N', 
    verbatimLongitude: '74°7’22.8"W'
  },
  {
    verbatimCoordinates: '40°7\'22.8"N, 74°7\'22.8"W',
    verbatimLatitude: '40°7\'22.8"N', 
    verbatimLongitude: '74°7\'22.8"W'
  },
  {
    verbatimCoordinates: '40 7 22.8, -74 7 22.8',
    verbatimLatitude: '40 7 22.8', 
    verbatimLongitude: '-74 7 22.8'
  },
  {
    verbatimCoordinates: '40.123 -74.123',
    verbatimLatitude: '40.123', 
    verbatimLongitude: '-74.123'
  },
  {
    verbatimCoordinates: '40.123°,-74.123°',
    verbatimLatitude: '40.123°', 
    verbatimLongitude: '-74.123°'
  },
  {
    verbatimCoordinates: '40.123N74.123W',
    verbatimLatitude: '40.123N', 
    verbatimLongitude: '74.123W'
  },
  {
    verbatimCoordinates: '4007.38N7407.38W',
    verbatimLatitude: '4007.38N', 
    verbatimLongitude: '7407.38W'
  },
  {
    verbatimCoordinates: '40°7’22.8"N, 74°7’22.8"W',
    verbatimLatitude: '40°7’22.8"N', 
    verbatimLongitude: '74°7’22.8"W'
  },
  {
    verbatimCoordinates: '400722.8N740722.8W',
    verbatimLatitude: '400722.8N', 
    verbatimLongitude: '740722.8W'
  },
  {
    verbatimCoordinates: 'N 40 7.38 W 74 7.38',
    verbatimLatitude: 'N 40 7.38', 
    verbatimLongitude: 'W 74 7.38'
  },
  {
    verbatimCoordinates: '40:7:22.8N 74:7:22.8W',
    verbatimLatitude: '40:7:22.8N', 
    verbatimLongitude: '74:7:22.8W'
  },
  {
    verbatimCoordinates: '40:7:23N,74:7:23W',
    verbatimLatitude: '40:7:23N', 
    verbatimLongitude: '74:7:23W',
    decimalLatitude: 40.1230555555,
    decimalLongitude: -74.1230555555
  },
  {
    verbatimCoordinates: '40°7’23"N 74°7’23"W',
    verbatimLatitude: '40°7’23"N', 
    verbatimLongitude: '74°7’23"W',
    decimalLatitude: 40.1230555555,
    decimalLongitude: -74.12305555555555
  },
  {
    verbatimCoordinates: '40°7’23" -74°7’23"',
    verbatimLatitude: '40°7’23"', 
    verbatimLongitude: '-74°7’23"',
    decimalLatitude: 40.1230555555,
    decimalLongitude: -74.123055555
  },
  {
    verbatimCoordinates: '40d 7’ 23" N 74d 7’ 23" W',
    verbatimLatitude: '40d 7’ 23" N', 
    verbatimLongitude: '74d 7’ 23" W',
    decimalLatitude: 40.1230555555,
    decimalLongitude: -74.123055555
  },
  {
    verbatimCoordinates: '40.123N 74.123W',
    verbatimLatitude: '40.123N', 
    verbatimLongitude: '74.123W'
  },
  {
    verbatimCoordinates: '40° 7.38, -74° 7.38',
    verbatimLatitude: '40° 7.38', 
    verbatimLongitude: '-74° 7.38'
  },
  {
    verbatimCoordinates: '40° 7.38, -74° 7.38',
    verbatimLatitude: '40° 7.38', 
    verbatimLongitude: '-74° 7.38'
  },
  {
    verbatimCoordinates: '40 7 22.8; -74 7 22.8', //semicolon separator
    verbatimLatitude: '40 7 22.8', 
    verbatimLongitude: '-74 7 22.8'
  }
]

var coordsParserDecimals = {
  decimalLatitude: 40.123, 
  decimalLongitude: -74.123
}

//formats from https://gist.github.com/moole/3707127/337bd31d813a10abcf55084381803e5bbb0b20dc 

var coordsRegexFormats = [
  {
    verbatimCoordinates: '50°4\'17.698"south, 14°24\'2.826"east',
    verbatimLatitude: '50°4\'17.698"south', 
    verbatimLongitude: '14°24\'2.826"east',
    decimalLatitude: -50.0715827777777778,
    decimalLongitude: 14.400785

  },
  {
    verbatimCoordinates: '50d4m17.698S 14d24m2.826E',
    verbatimLatitude: '50d4m17.698S', 
    verbatimLongitude: '14d24m2.826E',
    decimalLatitude: -50.0715827777777778,
    decimalLongitude: 14.400785
  },
  {
    verbatimCoordinates: '40:26:46N,79:56:55W',
    verbatimLatitude: '40:26:46N', 
    verbatimLongitude: '79:56:55W',
    decimalLatitude: 40.4461111111111111,
    decimalLongitude: -79.9486111111111111
  },
  {
    verbatimCoordinates: '40:26:46.302N 79:56:55.903W',
    verbatimLatitude: '40:26:46.302N', 
    verbatimLongitude: '79:56:55.903W',
    decimalLatitude: 40.446195,
    decimalLongitude: -79.9488619444444444
  },
  {
    verbatimCoordinates: '40°26′47″N 79°58′36″W',
    verbatimLatitude: '40°26′47″N', 
    verbatimLongitude: '79°58′36″W',
    decimalLatitude: 40.4463888888888889,
    decimalLongitude: -79.9766666666666667

  },
  {
    verbatimCoordinates: '40d 26′ 47″ N 79d 58′ 36″ W',
    verbatimLatitude: '40d 26′ 47″ N', 
    verbatimLongitude: '79d 58′ 36″ W',
    decimalLatitude: 40.4463888888888889,
    decimalLongitude: -79.9766666666666667
  },
  {
    verbatimCoordinates: '40.446195N 79.948862W',
    verbatimLatitude: '40.446195N', 
    verbatimLongitude: '79.948862W',
    decimalLatitude: 40.446195,
    decimalLongitude: -79.948862
  },   
  {
    verbatimCoordinates: '40,446195° 79,948862°',
    verbatimLatitude: '40,446195°', 
    verbatimLongitude: '79,948862°',
    decimalLatitude: 40.446195,
    decimalLongitude: 79.948862
  }, 
  {
    verbatimCoordinates: '40° 26.7717, -79° 56.93172',
    verbatimLatitude: '40° 26.7717', 
    verbatimLongitude: '-79° 56.93172',
    decimalLatitude: 40.446195,
    decimalLongitude: -79.948862
  }, 
  {
    verbatimCoordinates: '40.446195, -79.948862',
    verbatimLatitude: '40.446195', 
    verbatimLongitude: '-79.948862',
    decimalLatitude: 40.446195,
    decimalLongitude: -79.948862
  },
  {
    verbatimCoordinates: '40.123256; -74.123256', //testing semicolon
    verbatimLatitude: '40.123256', 
    verbatimLongitude: '-74.123256',
    decimalLatitude: 40.123256, 
    decimalLongitude: -74.123256 
  }  
]

var otherFormats = [
  // additional formats we've encountered
  {
    verbatimCoordinates: '18.24S 22.45E', //this is read as degrees and minutes
    verbatimLatitude: '18.24S', 
    verbatimLongitude: '22.45E', 
    decimalLatitude: -18.4,
    decimalLongitude: 22.75
  }, 
  {
    verbatimCoordinates: '27deg 15min 45.2sec S 18deg 32min 53.7sec E',
    verbatimLatitude: '27deg 15min 45.2sec S', 
    verbatimLongitude: '18deg 32min 53.7sec E',
    decimalLatitude: -27.2625555555555556,
    decimalLongitude: 18.54825
  }, 
  {
    verbatimCoordinates: '-23.3245° S / 28.2344° E',
    verbatimLatitude: '-23.3245° S', 
    verbatimLongitude: '28.2344° E',
    decimalLatitude: -23.3245,
    decimalLongitude: 28.2344
  },
  {
    verbatimCoordinates: '40° 26.7717 -79° 56.93172',
    verbatimLatitude: '40° 26.7717', 
    verbatimLongitude: '-79° 56.93172', 
    decimalLatitude: 40.446195,
    decimalLongitude: -79.948862

  },
  {
    verbatimCoordinates: '27.15.45S 18.32.53E',
    verbatimLatitude: '27.15.45S', 
    verbatimLongitude: '18.32.53E',
    decimalLatitude: -27.2625,
    decimalLongitude: 18.548055
  }, 
  {
    verbatimCoordinates: '27,71372° S 23,07771° E', //decimals with commas
    verbatimLatitude: '27,71372° S', 
    verbatimLongitude: '23,07771° E',
    decimalLatitude: -27.71372,
    decimalLongitude: 23.07771
  }
]

let userProvidedFormats = [
  {
    //issue https://github.com/ianengelbrecht/geo-coordinates-parser/issues/1
    verbatimCoordinates: 'N 52d0m0s E 000d0m0s',
    verbatimLatitude: 'N 52d0m0s', 
    verbatimLongitude: 'E 000d0m0s',
    decimalLatitude: 52.00000,
    decimalLongitude: 0.0000
  },
  {
    // https://github.com/ianengelbrecht/geo-coordinates-parser/issues/1
    verbatimCoordinates: 'N49 0.000 E02 33.314',
    verbatimLatitude: 'N49 0.000', 
    verbatimLongitude: 'E02 33.314',
    decimalLatitude: 49.00000,
    decimalLongitude: 2.5552333333333333
  }
]

function getAllTestFormats() {
  var arr1 = []
  coordsParserFormats.forEach(item => {
    if (item.decimalLatitude){
      arr1.push(item)
    }
    else {
      arr1.push({...item, ...coordsParserDecimals})
    }
  })
  
  return [...arr1, ...coordsRegexFormats, ...otherFormats, ...userProvidedFormats]
 
}

module.exports = getAllTestFormats();