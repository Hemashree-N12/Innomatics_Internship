from fastapi import FastAPI, Query

app = FastAPI()

# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse',      'price': 499, 'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',            'price':  99, 'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',             'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',             'price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Laptop Stand',        'price': 599, 'category': 'Electronics', 'in_stock': True },
    {'id': 6, 'name': 'Mechanical Keyboard', 'price':1599, 'category': 'Electronics', 'in_stock': True },
    {'id': 7, 'name': 'Web Cam',             'price': 799, 'category': 'Electronics', 'in_stock': True },
]

# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}
 
# ── Endpoint 2 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

#Get product by its category Question--2
@app.get('/products/category/{Category}')
def get_category_name(Category:str):
    result = []
    for p in products:
        if(p['category'] == Category):
            result.append(p)
    if result:
        return {"category": Category, "products": result, "total": len(result)}
    else:
        return {"error":"No Products found in this category"}
    
#Question 3: Products in Stock
@app.get('/instock')
def get_instock():
    stock = [p for p in products if p['in_stock'] == True]
    return {"in_stock_products": stock, "Count": len(stock)}
    
#Question 4:Store summary
@app.get('/store/summary')
def store_summary():
   in_stock_count = len([p for p in products if p['in_stock'] == True])
   out_of_stock_count = len(products)-in_stock_count
   categories = list(set([p['category'] for p in products]))
   return {"Store_Name":"My Ecommerce Store","total":len(products),"In_Stock":in_stock_count,"Out_of_stock":out_of_stock_count,"Categories":categories}

#Question 5 Search for item
@app.get("/products/search/{keyword}")
def product_search(keyword: str):
    match = [p for p in products if keyword.lower() in p['name'].lower()]
    if match:
        return {"keyword": keyword, "Matched_Results": match, "Total_matches": len(match)}
    else:
        return {"message": "No products matched your search"}
    
#Bonus Question
@app.get("/deals")
def product_deals():
    best_pick = min(products, key=lambda p: p["price"])
    premium = max(products, key=lambda p: p["price"])
    return {"best_deal": best_pick,"premium_pick": premium}