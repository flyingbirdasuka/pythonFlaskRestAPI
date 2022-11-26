import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Schema.schema import ItemSchema, ItemUpdateSchema
from Model import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return ItemModel.query.all()
        except KeyError:
            abort(404, message="Something went wrong")

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,new_item_data):
        item = ItemModel(**new_item_data)
        try:
            db.session.add(item) 
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occurred while inserting the item")  

        return item      




@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            return item
        except KeyError:
            abort(404, message="Item not found.")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, new_item_data, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            if item:
                item.price = new_item_data["price"]
                item.name = new_item_data["name"]
            else:
                item = ItemModel(id=item_id, **new_item_data)    
            db.session.add(item) 
            db.session.commit()
            return item
        except KeyError:    
            abort(404, message="Item not found.")         

    def delete(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item) 
            db.session.commit()
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")  

