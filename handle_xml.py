import xml.etree.ElementTree as ET
from datetime import datetime

def create_xml(GTIN, impactScoreID,companyName,productName,product_text,PL,lifestyles,ingredients,nutrition):
    # Create the root element
    current_datetime = datetime.now()
    root = ET.Element("Product", VersionDateTime=current_datetime.strftime("%Y-%m-%d %H:%M:%S"), UpdateType="AddOrUpdate")

    # Create the Identity element
    identity = ET.SubElement(root, "Identity")

    # Add child elements to the Identity element

    product_codes = ET.SubElement(identity, "ProductCodes")
    code_gtin = ET.SubElement(product_codes, "Code", Scheme=GTIN)
    code_gtin.text = GTIN
    code_brandbank_pvid = ET.SubElement(product_codes, "Code", Scheme="IMPACTSCORE:PVID")
    code_brandbank_pvid.text = impactScoreID

    subscription = ET.SubElement(identity, "Subscription", Id="48541", Code="ALAR002")
    subscription.text = companyName

    diagnostic_description = ET.SubElement(identity, "DiagnosticDescription", Code="en-GB")
    diagnostic_description.text = productName

    default_language = ET.SubElement(identity, "DefaultLanguage")
    default_language.text = "en-GB"

    # Create the Data element
    data = ET.SubElement(root, "Data")

    # Create the Language element
    language = ET.SubElement(data, "Language", Code="en-GB", Source="OffPack", GroupingSetId="0", GroupingSetName="No Grouping")

    # Add child elements to the Language element
    description = ET.SubElement(language, "Description")
    description.text = product_text

    categorisations = ET.SubElement(language, "Categorisations")
    categorisation = ET.SubElement(categorisations, "Categorisation", Scheme="BRANDBANK")
    level_1 = ET.SubElement(categorisation, "Level", Code="00")
    level_1.text = PL[0]
    level_2 = ET.SubElement(categorisation, "Level", Code="00")
    level_2.text = PL[1]
    level_3 = ET.SubElement(categorisation, "Level", Code="00")
    level_3.text = PL[2]

    item_type_group = ET.SubElement(language, "ItemTypeGroup", Id="0", Name="All Attributes")

    # Add child elements to the ItemTypeGroup element
    if lifestyles:
        for lifestyle in lifestyles:
            statements = ET.SubElement(item_type_group, "Statements", Id="2", Name="Lifestyle")
            statement = ET.SubElement(statements, "Statement", Id="69")
            statement.text = lifestyle
            
    if ingredients:
        for ingredient in ingredients:
            long_text_items = ET.SubElement(item_type_group, "longtextitems")
            long_text_item = ET.SubElement(long_text_items, "longtextitem", Id="1", Name="Ingredients")
            text = ET.SubElement(long_text_item, "Text")
            text.text = ingredient

    textual_nutrition = ET.SubElement(item_type_group, "TextualNutrition", Id="85", Name="Nutrition")
    headings = ET.SubElement(textual_nutrition, "Headings")
    heading = ET.SubElement(headings, "Heading")
    heading.text = "Per 100g"

    # Add Nutrient elements to the TextualNutrition element
    nutrients = [
        {"Name": "Fat", "Value": nutrition['fat']},
        {"Name": "of which saturates", "Value": nutrition['saturates']},
        {"Name": "of which sugars", "Value": nutrition['sugars']},
        {"Name": "Salt", "Value": nutrition['salt']}
    ]

    for nutrient in nutrients:
        nutrient_element = ET.SubElement(textual_nutrition, "Nutrient")
        nutrient_name = ET.SubElement(nutrient_element, "Name")
        nutrient_name.text = nutrient["Name"]
        values = ET.SubElement(nutrient_element, "Values")
        value = ET.SubElement(values, "Value")
        value.text = nutrient["Value"]

    numeric_nutrition = ET.SubElement(item_type_group, "NumericNutrition", Id="86", Name="Calculated Nutrition")
    per_100_unit = ET.SubElement(numeric_nutrition, "Per100Unit")
    per_100_unit.text = "g"
    per_100_heading = ET.SubElement(numeric_nutrition, "Per100Heading")
    per_100_heading.text = "per 100"
    per_serving_heading = ET.SubElement(numeric_nutrition, "PerServingHeading")
    per_serving_heading.text = "Per 30g Serving"

    # Add NutrientValues elements to the NumericNutrition element
    nutrient_values = [
        {"Id": "1189", "Name": "Fat (g)", "Value": nutrition['fat']},
        {"Id": "1190", "Name": "of which saturates (g)", "Value": nutrition['saturates']},
        {"Id": "1186", "Name": "of which sugars (g)", "Value": nutrition['sugars']},
        {"Id": "1214", "Name": "Salt (g)", "Value": nutrition['salt']}
    ]

    for nutrient_value in nutrient_values:
        nutrient_values_element = ET.SubElement(numeric_nutrition, "NutrientValues", Id=nutrient_value["Id"], Name=nutrient_value["Name"])
        per_100 = ET.SubElement(nutrient_values_element, "Per100")
        value = ET.SubElement(per_100, "Value")
        value.text = nutrient_value["Value"]

    return(root)

def export_xml(root,filepath):
    # Create the ElementTree object
    tree = ET.ElementTree(root)

    # Specify the file path to save the XML
    file_path = filepath

    # Save the XML to the file
    tree.write(file_path, encoding="utf-8", xml_declaration=True)