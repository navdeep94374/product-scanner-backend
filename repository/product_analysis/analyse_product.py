from fastapi.responses import JSONResponse
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse , clean_text
from fastapi import status
import openfoodfacts
from carcinogens_model.detect_carcinogens import check_carcinogen

def analyze_allergens(user_allergen,product_allergen):
    allergens = []
    for elem in product_allergen:
        cnt = user_allergen.count(elem.replace("en:","").lower())
        if cnt:
            allergens.append(elem)
    return allergens


def filter_allergen_tags(allergens):
  filter_data = [allergen.replace("en:","") for allergen in allergens]
  return filter_data

# data= {
#     "code": "3017620422003",
#     "name": "Nutella",
#     "ingredients": [
#       {
#         "ciqual_proxy_food_code": "31016",
#         "ecobalyse_code": "8f075c25-9ebf-430c-b41d-51d165c6e0d8",
#         "id": "en:sugar",
#         "is_in_taxonomy": 1,
#         "percent_estimate": 38.35,
#         "percent_max": 60,
#         "percent_min": 16.7,
#         "text": "Sucre",
#         "vegan": "yes",
#         "vegetarian": "yes"
#       },
#       {
#         "ciqual_food_code": "16129",
#         "ecobalyse_code": "45658c32-66d9-4305-a34b-21d6a4cef89c",
#         "from_palm_oil": "yes",
#         "id": "en:palm-oil",
#         "is_in_taxonomy": 1,
#         "percent_estimate": 24.75,
#         "percent_max": 36.5,
#         "percent_min": 13,
#         "text": "huile de palme",
#         "vegan": "yes",
#         "vegetarian": "yes"
#       },
#       {
#         "ciqual_food_code": "15004",
#         "ecobalyse_code": "hazelnut-unshelled-non-eu",
#         "id": "en:hazelnut",
#         "is_in_taxonomy": 1,
#         "percent": 13,
#         "percent_estimate": 13,
#         "percent_max": 13,
#         "percent_min": 13,
#         "text": "NOISETTES",
#         "vegan": "yes",
#         "vegetarian": "yes"
#       },
#       {
#         "ciqual_proxy_food_code": "18100",
#         "id": "en:fat-reduced-cocoa",
#         "is_in_taxonomy": 1,
#         "percent": 7.4,
#         "percent_estimate": 7.4,
#         "percent_max": 7.4,
#         "percent_min": 7.4,
#         "text": "cacao maigre",
#         "vegan": "yes",
#         "vegetarian": "yes"
#       },
#       {
#         "ciqual_food_code": "19054",
#         "ecobalyse_code": "b6776a28-ec84-4bf3-988c-07b3c29f6136",
#         "id": "en:skimmed-milk-powder",
#         "is_in_taxonomy": 1,
#         "percent": 6.6,
#         "percent_estimate": 6.6,
#         "percent_max": 6.6,
#         "percent_min": 6.6,
#         "text": "LAIT écrémé en poudre",
#         "vegan": "no",
#         "vegetarian": "yes"
#       },
#       {
#         "id": "en:whey-powder",
#         "is_in_taxonomy": 1,
#         "percent_estimate": 3.3,
#         "percent_max": 6.6,
#         "percent_min": 0,
#         "text": "LACTOSERUM en poudre",
#         "vegan": "no",
#         "vegetarian": "maybe"
#       },
#       {
#         "id": "en:emulsifier",
#         "ingredients": [
#           {
#             "id": "en:e322",
#             "ingredients": [
#               {
#                 "ciqual_food_code": "42200",
#                 "id": "en:soya-lecithin",
#                 "is_in_taxonomy": 1,
#                 "percent_estimate": 3.3,
#                 "percent_max": 6.6,
#                 "percent_min": 0,
#                 "text": "lécithines de SOJA",
#                 "vegan": "yes",
#                 "vegetarian": "yes"
#               }
#             ],
#             "is_in_taxonomy": 1,
#             "percent_estimate": 3.3,
#             "percent_max": 6.6,
#             "percent_min": 0,
#             "text": "lécithines",
#             "vegan": "maybe",
#             "vegetarian": "maybe"
#           }
#         ],
#         "is_in_taxonomy": 1,
#         "percent_estimate": 3.3,
#         "percent_max": 6.6,
#         "percent_min": 0,
#         "text": "émulsifiants"
#       },
#       {
#         "id": "en:vanillin",
#         "is_in_taxonomy": 1,
#         "percent_estimate": 3.30000000000001,
#         "percent_max": 6.6,
#         "percent_min": 0,
#         "text": "vanilline"
#       }
#     ],
#     "nutriscore_data": {
#       "components": {
#         "negative": [
#           {
#             "id": "energy",
#             "points": 6,
#             "points_max": 10,
#             "unit": "kJ",
#             "value": 2252
#           },
#           {
#             "id": "sugars",
#             "points": 15,
#             "points_max": 15,
#             "unit": "g",
#             "value": 56.3
#           },
#           {
#             "id": "saturated_fat",
#             "points": 10,
#             "points_max": 10,
#             "unit": "g",
#             "value": 10.6
#           },
#           {
#             "id": "salt",
#             "points": 0,
#             "points_max": 20,
#             "unit": "g",
#             "value": 0.11
#           }
#         ],
#         "positive": [
#           {
#             "id": "fiber",
#             "points": 0,
#             "points_max": 5,
#             "unit": "g",
#             "value": None
#           },
#           {
#             "id": "fruits_vegetables_legumes",
#             "points": 0,
#             "points_max": 5,
#             "unit": "%",
#             "value": 0
#           }
#         ]
#       },
#       "count_proteins": 0,
#       "count_proteins_reason": "negative_points_greater_than_or_equal_to_11",
#       "grade": "e",
#       "is_beverage": 0,
#       "is_cheese": 0,
#       "is_fat_oil_nuts_seeds": 0,
#       "is_red_meat_product": 0,
#       "is_water": 0,
#       "negative_points": 31,
#       "negative_points_max": 55,
#       "positive_nutrients": [
#         "fiber",
#         "fruits_vegetables_legumes"
#       ],
#       "positive_points": 0,
#       "positive_points_max": 10,
#       "score": 31
#     },
#     "thumbnail": "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_en.633.400.jpg",
#     "allergens_tags": [
#       "en:milk",
#       "en:nuts",
#       "en:soybeans"
#     ],
#     "user_sensitive_to_allergens":["milk"]
#   }

def analyse_product(db,user,payload):
    try:
        api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
        product = api.product.get(payload.product_code)

        if product is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=ApiError("Sorry this product is not in our database", status_code=status.HTTP_404_NOT_FOUND, success=False).get_info())

        analysis =  {
        "name": product.get("product_name", "Unknown Product"),
        "code": product.get("code", "N/A"),
        "nutriscore_grade": product.get("nutriscore_grade", "unknown"),
        "nutriscore_data": product.get("nutriscore_data", {}),
        "ingredients": [item.strip() for item in product.get("ingredients_text", "").split(",") if item.strip()],
        "thumbnail": product.get("selected_images", {}).get("front", {}).get("display", {}).get("en", product.get("image_front_small_url","https://cdn-icons-png.flaticon.com/512/7621/7621217.png")),
        "allergens_tags": filter_allergen_tags(product.get("allergens_tags", [])),
        "user_sensitive_to_allergens":analyze_allergens(user["allergen_info"],product.get("allergens_tags", [])),
         "carcinogens" : clean_text(check_carcinogen(product.get("ingredients_text", "")))
        }

        print(analysis["ingredients"])
       
        return JSONResponse(status_code=200,content=ApiResponse("Product analysis sucess",200,True,analysis).get_info())


    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=ApiError("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,err=str(e)).get_info())
