from flask import jsonify, request
from models.bookmark import Bookmark
from models.product import Product
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookmarkController:
    @staticmethod
    def getBookmarkByUserId():
        # NOTE: body contain userId
        userId = request.get_json()['userId']
        try:
            bookmarks = db.session.query(Bookmark).filter_by(user=userId).all()
            bookmarks = Bookmark.serialize_list(bookmarks)
            if(not len(bookmarks)):
                raise
            products = []
            for b in bookmarks:
                products.append(Product.query.filter_by(serial_no=b['product']).first().serialize)
            result = {'userID': userId, 'products': products}
            return jsonify(result)
        except:
            return jsonify({'message': 'The bookmark for userID {} is not existed'.format(userId)}), 400

    @staticmethod
    def addBookmark():
        # NOTE: body contain userId and serialNo
        try:
            userId = request.get_json()['userId']
            serialNo = request.get_json()['serialNo']
            if(not userId or not serialNo):
                raise
            bookmark = Bookmark(userId, serialNo)
            try:
                db.session.add(bookmark)
                db.session.commit()
            except:
                return jsonify({'message': 'This bookmark information went wrong'}), 404
            return jsonify({'message': 'The bookmark is added successfully'})
        except:
            return jsonify({'message': 'The userId, and serialNo are required'}), 400
    @staticmethod
    def removeBookmark():
        # NOTE: body contain userId and serialNo
        try:
            userId = request.get_json()['userId']
            serialNo = request.get_json()['serialNo']
            if (not userId or not serialNo):
                raise
            bookmark = db.session.query(Bookmark).filter_by(user=userId, product=serialNo).first()
            try:
                db.session.delete(bookmark)
                db.session.commit()
            except:
                return jsonify({'message': 'This bookmark is not existed'}), 404
            return jsonify({'message': 'The bookmark is deleted successfully'})
        except:
            return jsonify({'message': 'The userId, and serialNo are required'}), 400