def load_catalog(catalog,storage):
    for p in storage.load_products():
        catalog.add_product(p)

