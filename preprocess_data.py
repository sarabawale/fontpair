import json, urllib.request, re
import pandas as pd
from contextlib import closing
# from pprint import pprint
# from urllib.request import urlopen

# Initialize font lists for both databases
# col_names =  ['name', 'family', 'category','italic','weight']
# gf = pd.DataFrame(columns = col_names)
# fs = pd.DataFrame(columns = col_names)
gf = []
fs = []

# font weights:
# ultra light = 100
# light = 300
# regular = 400
# medium = 500
# bold = 700
# black = 900

# Request URLS for databases
# "https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyAMBY2XP1dQ67L3SX2rOOrZ505Is99Fm40"
# "http://www.fontsquirrel.com/api/fontlist/all"
# "https://www.fontsquirrel.com/api/familyinfo/{family}"

# def getVariantName(weight,family,italic):
#     # Get name based on weight
#     if weight == 100:
#         name = family + " Ultra Light"
#     elif weight == 300:
#         name = family + " Light"
#     elif weight == 400:
#         name = family + " Regular"
#     elif weight == 500:
#         name = family + " Medium"
#     elif weight == 700:
#         name = family + " Bold"
#     else weight == 900:
#         name = family + " Black"

#     # Check for italic
#     if italic:
#         name = name + " Italic"

#     return name

# Import Google Fonts metadata
with closing(urllib.request.urlopen("https://www.googleapis.com/webfonts/v1/webfonts?sort=alpha&key=AIzaSyAMBY2XP1dQ67L3SX2rOOrZ505Is99Fm40")) as urlGF:
    gfData = json.loads(urlGF.read().decode())
    fontlist = gfData['items'] # Get actual list of fonts (Google wraps them in a 2-column list for some reason)

    for font in fontlist:
        # Initialize feature variables
        name = ""
        family = font['family']
        category = font['category']
        italic = 0 # default is 0: not italic
        weight = 400 # default is regular
        variants = font['variants']

        # Check for font variants
        if len(variants) > 1:
            for var in variants:
                # Get weight
                temp = var.split("00")
                if len(temp) == 1:
                    weight = 400
                else:
                    weight = int(temp[0])*100
                print("family: ",family)
                print("var: ",var)
                print("temp: ",temp)
                # print("temp[0]: ",temp[0])
                print("weight: ",weight)
                # Get name based on weight (if not regular)
                if weight == 100:
                    name = family + " Ultra Light"
                elif weight == 300:
                    name = family + " Light"
                elif weight == 500:
                    name = family + " Medium"
                elif weight == 700:
                    name = family + " Bold"
                elif weight == 900:
                    name = family + " Black"
                else:
                    name = family

                print("name: ",name)
                print("\n")

                # Check if italic
                if len(temp) > 1 and temp[1] == 'italic':
                    italic = 1
                    name = name + " Italic"
        print("final name: ",name)
        print("italic: ",italic)
        print("\n")
        # Create tuple to be appended to list
        current = {}
        current['name'] = name
        current['family'] = family
        current['category'] = category
        current['italic'] = italic
        current['weight'] = weight
        #print(current['name'])
        gf.append(current)
#print(gf)
# Import Fontsquirrel metadata
with closing(urllib.request.urlopen("http://www.fontsquirrel.com/api/fontlist/all")) as urlFS:
    fsData = json.loads(urlFS.read().decode())

    for font in fsData:
        # Initialize feature variables
        name = ""
        family = font['family_name']
        category = font['classification']
        italic = 0 # default is 0: not italic
        weight = 400 # default is regular
        numVariants = int(font['family_count'])

        # Create tuple to be appended to list
        current = {}
        current['name'] = name
        current['family'] = family
        current['category'] = category
        current['italic'] = italic
        current['weight'] = weight

        # Clean up category features
        c = category.lower()
        # if c == 'dingbat': # exclude dingbat
        #     continue
        if c == 'monospaced':
            category = 'monospace'
        elif c == 'handdrawn':
            category = 'handwriting'
        else:
            category = c

        # Check for font variants
        if numVariants > 1:
            # Get information about the current font's variants
            variantURL = "https://www.fontsquirrel.com/api/familyinfo/" + font['family_urlname']
            with closing(urllib.request.urlopen(variantURL)) as v:
                varData = json.loads(v.read().decode())

            for var in varData:
                # f = var['family_name'] + " " + var['style_name']
                # current['name'] = f

                # Get variant name

                # Split font style into words based on capital letters
                styleWords = re.findall('[A-Z][^A-Z]*', font['style_name'])

                # Change style phrasings to match GF phrasings

                # Add a space after all but the last word
                for i in range(0,len(styleWords)-1):
                    styleWords[i] = styleWords[i] + " "

                # Combine style with family to create variant name
                name = (family + " ").join(styleWords)

                # Check italic
                if 'italic' in var['style_name']:
                    current['italic'] = 1

                # Check weight (default is regular = 400):
                elif 'UltraLight' in var['style_name'] or 'ExtraLight' in var['style_name']:
                    current['weight'] = 100
                elif 'Light' in var['style_name']:
                    current['weight'] = 300
                elif 'Bold' in var['style_name']:
                    current['weight'] = 700
                elif 'Black' in var['style_name'] or 'ExtraBold' in var['style_name']:
                    current['weight'] = 900

                # Create tuple and append to list
                # current['name'] = name
                # current['family'] = family
                # current['category'] = category
                # current['italic'] = italic
                # current['weight'] = weight
                fs.append(current)
        else:
            # current['name'] = font['family_name']
            name = family
            fs.append(current)

# Convert lists to dataframes
col_names =  ['name', 'family', 'category','italic','weight']
dfGF = pd.DataFrame(gf, columns = col_names)
dfFS = pd.DataFrame(fs, columns = col_names)
print(dfGF)
print(dfFS)

# Merge dataframes into one, getting rid of duplicates at the same time
dataset = dfGF.merge(dfFS, left_on='name', right_on='name')