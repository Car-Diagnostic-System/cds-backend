from flask import Blueprint
from controllers.bookmarkController import BookmarkController

class BookmarkBlueprint:
    bookmark_bp = Blueprint('bookmark_bp', __name__, url_prefix='/bookmarks')
    bookmark_bp.route('/', methods=['POST'])(BookmarkController.getBookmarkByUserId)
    bookmark_bp.route('/add', methods=['POST'])(BookmarkController.addBookmark)
    bookmark_bp.route('/remove', methods=['POST'])(BookmarkController.removeBookmark)
