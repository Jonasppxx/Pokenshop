import json
import os

# Laden der Produktdaten aus der JSON-Datei
with open('products.json', 'r') as file:
    products = json.load(file)['products']

# Verzeichnis für die Produktseiten
output_dir = 'product_pages'
os.makedirs(output_dir, exist_ok=True)

# HTML-Vorlage für die Produktseiten
product_page_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        body {{
            background-color: #f4f4f9;
            color: #333;
            font-family: 'Montserrat', sans-serif;
            margin: 0;
            padding: 20px;
        }}
        #main-content {{
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        h1 {{
            font-size: 2.5em;
            color: #2C3E50;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 1.5em; /* Schriftgröße erhöht */
            line-height: 1.6;
            margin-bottom: 10px; /* Abstand verringert */
        }}
        a {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #78A1BB;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }}
        a:hover {{
            background-color: #2C3E50;
        }}
        .product-detail {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .product-detail .image-container {{
            position: relative;
            width: 45%;
            margin-bottom: 10px; /* Abstand verringert */
        }}
        .product-detail img {{
            width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background: #fff;
            transition: opacity 0.3s ease;
        }}
        .product-detail img.hover {{
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
        }}
        .product-detail .image-container:hover img.hover {{
            opacity: 1;
        }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const imageContainers = document.querySelectorAll('.image-container');
            imageContainers.forEach(container => {{
                container.addEventListener('click', function() {{
                    const hoverImage = container.querySelector('img.hover');
                    if (hoverImage.style.opacity === '1') {{
                        hoverImage.style.opacity = '0';
                    }} else {{
                        hoverImage.style.opacity = '1';
                    }}
                }});
            }});
        }});
    </script>
</head>
<body>
    <div id="main-content">
        <h1>{name}</h1>
        <div class="product-detail">
            <div class="image-container">
                <img src="../{image}" alt="{name}" class="normal">
                <img src="../{hoverImage}" alt="{name}" class="hover">
            </div>
            <div>
                <p>Price: CHF{price}</p>
                <p>Set: {set}</p>
            </div>
        </div>
        <a href="../products.html">Back to Shop</a>
    </div>
</body>
</html>
"""

# Generieren der Produktseiten
for product in products:
    product_page_content = product_page_template.format(
        name=product['name'],
        image=product['image'],
        hoverImage=product['hoverImage'],
        price=product['price'],
        set=product['set']
    )
    output_path = os.path.join(output_dir, f"{product['name']}.html")
    with open(output_path, 'w') as output_file:
        output_file.write(product_page_content)

print("Product pages generated successfully.")