import pandas as pd
import numpy as np
import categorisation
import pickle
import numpy as np
import extract_from_text
import handle_xml
import json
from tensorflow import keras
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from sharepoint import SharePoint
from supporting_files import get_supporting_files
from OCR import ocr_image


c1 = extract_from_text.create_categoriser()
ingredients_set = extract_from_text.get_ingredients_set()
lifestyles_set = extract_from_text.get_lifestyles_set()
AUTHENTICATION_ROOT =r'C:\\Users\\Clamfighter\\Documents\\GitHub\\00-Authentication\\Impact-Score-Extraction'

'''
Download the newst version of the Product Image information spreadsheet to get details for each product
'''
#get_supporting_files(file_name='Product Image Information.xlsx',folder_name='Supporting Files')
pd_PII = pd.read_excel('Supporting Files/Product Image Information.xlsx')
foldernames=pd_PII['Foldername'].to_list() #extract the foldername for each 
sp=SharePoint()


config_path = '\\'.join([AUTHENTICATION_ROOT, 'OCR_config.json'])
# read json file
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['cognitive_services']

OCR_SUBSCRIPTION_KEY = config['subscription_key']
OCR_ENDPOINT = config['endpoint']

exampletext=r'BISTO FAVOURITE GRAVY GRANULES Put 4 heaped teaspoons (20g) of 1 Bisto granules into a measuring jug - for extra thick gravy add more granules at this point. serving 2 Add 280ml (1/2 pint) of boiling suggestion water to the granules. Ingredie Salt, Wheat 3 Stir vigorously and continually contain until you get a smooth gravy. Allerg Serve & Enjoy! BISTO trade m this pack an Mon SUITAR z Intake* FREEPOS es prepared): DRUM - CARD RO widely recycled CAP - PLASTIC check local recycling Find us on 5 000354 904820 > facebook/AahBisto NEW WEIGHT ENECO 350g ℮ BEST BEFORE END SEE BASE OF DRUM Store in a cool dry place away from direct heat and Sunlight. Some settling of contents may have occurred during transit. 3030929  Sausage and Mash serving hedens suggestion Ingredients: Potato Starch, Maltodextrin, Palm Oil, Salt, Wheat Flour (with added Calcium, Iron, Niacin, Thiamin), Colour (E150c), Sugar, Flavourings (contain Barley), Flavour Enhancers (E621, E635), Emulsifier (E322) (contains Soya). Allergy Advice: For allergens, including cereals containing gluten, see ingredients in bold BISTO trade marks, designs and logos appearing on this pack are owned by the Premier Foods Group. If you have any problems please keep the packaging and phone 0800 234 6328 Mon - Fri.9.00am - 5.00pm (ROI 1800 93 2814). FREEPOST PREMIER FOODS CONSUMER RELATIONS ROK Premier Foods ROI, PO Box No 13008, Dublin 1, Ireland www.bisto.co.uk NUTRITION INFORMATION Typical Values PER 100g PER 50ml as sold portion as ENERGY- (kJ)/(kcal) prepared 1665kJ 55kJ Fat 397kcal 13kcal of which Saturates 16.3g 0.5g 0.4g Carbohydrate 11.2g of which Sugars 59.8g 2.0 Fibre 12.2g <0.5g <0.5 Protein 2.1g 1.7g <0.5g Salt 14.33g 0.47g *Reference Intake of an average adult (8400KJ / 2000kcal). This pack makes approximately 106 portions  aah! BISTO JUST ADD BOILING WATER GRAVY GRANULES ESTD . THE . 1908 NATIONS FAVOURITE  BISTO FAVO GRAVY GRA OW SUGAR LOW FAT LOW SU CAR 1 Put 4 hennes Bisto me Per 50ml portion jug . for en as prepared contains more pro Energy 55kJ <1% 2 Add 200ml 13kcal water to the Fat 0.5g <1% 3 Stir vigor Saturates until you all 0.4g 2% Sugars Serve & Enjoy! <0.5g <1% Salt JUST ADD 0.47g 8% BOILING of an adults Reference Intake* WATER Typical values per 100ml (as prepared): Energy 110KJ / 26kcal CAP - 12 NES Find us on facebook/AahBisto 00354 NEW WEIGHT ITE 350g ℮ 04820 BEST BEFORE END SEE BASE OF DRUM 00 N Store in a cool dry place away from direct heat and V sunlight. Some settling of contents may have occurred during transit.'

for index, row in pd_PII.iterrows(): #for each product in the product information table
    
    #get data for each prodocut from table
    foldername = row['Foldername'] #take the folder name of the product
    GTIN='01010101010'
    impactScoreID='1010101010101'
    companyName='example CompanyName'
    productName='Example ProductName'

    print(foldername)
    folderdir='Images/'+foldername
    files = sp.get_subfiles(folder_name=folderdir)#find all the files in the product's folder
    

    '''
    for each image file, download the image 
    send it through Azure Cognitive Service to OCR the image
    combine all the strings from each image
    '''
    print('Processing Images')


    product_text=''
    for file in files: 
        print(file['Name'])
        image = SharePoint().download_file(file_name=file['Name'], folder_name=folderdir) 
        with open('tmp/tmp.jpg', 'wb') as f:
            f.write(image)
            f.close()
        image_file = open('tmp/tmp.jpg', "rb")
        #imagetext=ocr_image(image_file,OCR_SUBSCRIPTION_KEY,OCR_ENDPOINT) 
        #product_text=product_text+' '+imagetext 
    print(product_text)
    product_text = exampletext


    '''
    Now we have the text for the product, we can extract information from it
    '''
    pl1 = extract_from_text.get_pl1(product_text,c1)
    print('PL1: ',pl1)

    PL = [pl1,'undefined','undefined']

    ingredients = extract_from_text.get_ingredients(product_text.lower(),ingredients_set)
    print('Ingredients: ', ingredients)
    print(lifestyles_set)
    lifestyles = extract_from_text.get_lifestyles(product_text.lower(), lifestyles_set)
    print('Lifestyles: ', lifestyles)

    nutrition = extract_from_text.get_nutritional_info(product_text.lower())
    print(nutrition['sugars'])
    print(nutrition['fat'])
    print(nutrition['saturates'])
    print(nutrition['salt'])


    ''' format into xml'''

    root = handle_xml.create_xml(GTIN=GTIN, 
                          impactScoreID=impactScoreID, 
                          companyName=companyName,
                          productName=productName,
                          product_text=product_text,
                          PL=PL,
                          lifestyles=lifestyles,
                          ingredients=ingredients,
                          nutrition=nutrition)
    handle_xml.export_xml(root, 'output.xml')