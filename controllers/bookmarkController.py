from flask import jsonify, request
from models.bookmark import Bookmark
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookmarkController:
    @staticmethod
    def getBookmarkByUserId():
        # NOTE: body contain userId
        body = request.get_json()
        try:
            bookmarks = db.session.query(Bookmark).filter_by(user=body['userId']).all()
            bookmarks = Bookmark.serialize_list(bookmarks)
            products = []
            for b in bookmarks:
                userId = b['user']
                products.append(b['product'])
            result = {'userID': userId, 'products': products}
            return jsonify(result)
        except:
            return jsonify({'message': 'The bookmark for userID {} is not existed'.format(body['userId'])}), 400


    @staticmethod
    def addBookmark():
        # NOTE: body contain userId and serialNo
        body = request.get_json()
        bookmark = Bookmark(body['userId'], body['serialNo'])
        try:
            db.session.add(bookmark)
            db.session.commit()
        except:
            return jsonify({'message': 'This bookmark information went wrong'}), 404
        return jsonify({'message': 'The bookmark is added successfully'})

    @staticmethod
    def removeBookmark():
        # NOTE: body contain userId and serialNo
        body = request.get_json()
        bookmark = db.session.query(Bookmark).filter_by(user=body['userId'], product=body['serialNo']).first()
        try:
            db.session.delete(bookmark)
            db.session.commit()
        except:
            return jsonify({'message': 'This bookmark is not existed'}), 404
        return jsonify({'message': 'The bookmark is deleted successfully'})