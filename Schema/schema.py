from marshmallow import Schema, fields

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    city = fields.Str()

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()    

class StoreSchema(PlainStoreSchema): 
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only = True)

class ItemSchema(PlainItemSchema):  
    store_id = fields.Int(required=True)
    store = fields.Nested(PlainStoreSchema(),dump_only = True)  

