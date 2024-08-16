import os
import json
import shutil
import csv

def get_product_details_from_csv(csv_file):
    products = []
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "name": row["name"],
                "price": float(row["price"]),
                "set": row["set"],
                "image": row["image"],
                "hoverImage": row["hoverImage"]
            })
    return products

def create_directory(name):
    directory = os.path.join("images", name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def copy_images(product, directory):
    image_dest = os.path.join(directory, os.path.basename(product["image"]))
    shutil.copy(product["image"], image_dest)
    product["image"] = image_dest

    if product["hoverImage"]:
        hover_image_dest = os.path.join(directory, os.path.basename(product["hoverImage"]))
        shutil.copy(product["hoverImage"], hover_image_dest)
        product["hoverImage"] = hover_image_dest
    else:
        product["hoverImage"] = ""

def update_json(product):
    with open("products.json", "r+") as file:
        data = json.load(file)
        data["products"].append(product)
        file.seek(0)
        json.dump(data, file, indent=4)

def main():
    csv_file = "products.csv"
    products = get_product_details_from_csv(csv_file)
    for product in products:
        directory = create_directory(product["name"])
        copy_images(product, directory)
        update_json(product)
        print(f"Product {product['name']} added successfully!")

if __name__ == "__main__":
    main()