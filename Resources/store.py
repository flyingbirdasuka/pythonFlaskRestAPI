import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from Schema.schema import StoreSchema
from Model import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store")
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        try:
            return StoreModel.query.all()
        except KeyError:
            abort(404, message="Something went wrong")

    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, new_store_data):
        store = StoreModel(**new_store_data) 
        try:
            db.session.add(store) 
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )    
        except SQLAlchemyError:
            abort(500, message="an error occurred while inserting the item")  
            
        return store    


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id) 
            return store
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id) 
            db.session.delete(store) 
            db.session.commit()
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")  

