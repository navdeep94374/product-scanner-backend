import requests

def get_open_food_facts(barcode):
    url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 1:
            return data['product']
        else:
            print("Product not found.")
            return None
    else:
        print("Error:", response.status_code)
        return None

barcode = "1234567890123"
product_data = get_open_food_facts(barcode)

if product_data:
    nutrition = product_data.get('nutriments', {})
    print(f"Energy: {nutrition.get('energy', 'N/A')} kcal")
    print(f"Fat: {nutrition.get('fat', 'N/A')} g")
    print(f"Sugars: {nutrition.get('sugars', 'N/A')} g")