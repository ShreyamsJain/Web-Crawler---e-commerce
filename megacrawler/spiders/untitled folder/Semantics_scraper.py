from semantics3 import Products

sem3 = Products(
	api_key = "SEM310D8563D0E07BA3AC280829F8076605D",
	api_secret = "ZTliZjI1NTg5ZDQ2ZjdhNDMyNmRmMTc4Mjg3NjJmN2M"
)

product_list = ['laptop', 'phone']
results = []
all_products = []
for product in product_list:
	sem3.products_field("search", product)
	results = sem3.get_products()
	if product == 'laptop':
		for i, p in enumerate(results['results']):
			title = results['results'][i]['name']
			price = results['results'][i]['price']
			if 'color' in results['results'][i].keys():
				color = results['results'][i]['color']
			else:
				color = None
			image = results['results'][i]['images']
			url = results['results'][i]['sitedetails'][0]['url']
			product_data = {
	            'product' : 'Laptop',
	            'title': title,
	            'price': price,
	            'color' : color,
	            'image' : image,
	            'url' : url,
	        }

	if product == 'phone':
		sem3.products_field("search", product)
		results = sem3.get_products()
		for i, p in enumerate(results['results']):
			title = results['results'][i]['name']
			price = results['results'][i]['price']
			if 'color' in results['results'][i].keys():
				color = results['results'][i]['color']
			else:
				color = None
			if 'model' in results['results'][i].keys():
				model = results['results'][i]['model']
			else:
				model = None
			if 'size' in results['results'][i].keys():
				size = results['results'][i]['size']
			else:
				size = None
			image = results['results'][i]['images']
			url = results['results'][i]['sitedetails'][0]['url']
			product_data = {
	            'product' : 'Laptop',
	            'title': title,
	            'price': price,
	            'size' : size,
	            'model': model,
	            'color' : color,
	            'image' : image,
	            'url' : url,
	        }
	all_products.append(product_data)

print(all_products)
        #result = collection.insert_one(product_data)
        #print('One post: {0}'.format(result.inserted_id))
'''
            if current_key == 'Tablets':
                title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = properties.split(',')                
                size = ''
                os = ''
                processor = ''
                color = ''
                storage = ''
                for item in prop_list:
                    if '"' in item: 
                        size = item
                    if 'Android' in item:
                        os = item
                    if 'GHz' in item:
                        processor = item
                    if 'Black' in item or 'White' in item:
                        color = item
                    if 'GB' in item:
                        storage = item
                product_data = {
                    'product' : 'Tablet',
                    'title' : title,
                    'price' : price,
                    'size' : size,
                    'os' : os,
                    'processor' : processor,
                    'color' : color,
                    'storage' : storage
                }
                result = collection.insert_one(product_data)
                print('One post: {0}'.format(result.inserted_id))

            if current_key == 'Phones':
                title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = properties.split(',')
                os = ''
                size = ''
                for item in prop_list:
                    if 'Android' in item:
                        os = item
                    if '"' in item:
                        size = item
                product_data = {
                    'product' : 'Phone',
                    'title' : title,
                    'price' : price,
                    'os' : os,
                    'size' : size
                }
                result = collection.insert_one(product_data)
                print('One post: {0}'.format(result.inserted_id))


collection = getCollection()

def getCollection(self):
    client = MongoClient('ds227865.mlab.com', 27865)
    db = client['productdb']
    db.authenticate('admin', 'admin')
    collection = db.product_collection
    return collection
'''