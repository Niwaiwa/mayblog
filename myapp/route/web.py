from flask import Blueprint, request, make_response, jsonify
from myapp.controller.Auth import Register, Login, Logout
from myapp.controller.User import UserAPI
from myapp.controller.Article import ArticleAPI


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

auth_blueprint.add_url_rule("/register", view_func=Register.as_view('register'))
auth_blueprint.add_url_rule("/login", view_func=Login.as_view('login'))
auth_blueprint.add_url_rule("/logout", view_func=Logout.as_view('logout'))

api_blueprint.add_url_rule("/user/profile", view_func=UserAPI.as_view('UserAPI'))

article_view = ArticleAPI.as_view('ArticleAPI')
api_blueprint.add_url_rule("/article",
                           view_func=article_view, methods=['GET', 'DELETE'])
# api_blueprint.add_url_rule("/article/<int:user_id>",
#                            view_func=article_view, methods=['GET'])
api_blueprint.add_url_rule("/article/edit", view_func=article_view, methods=['POST'])
# api_blueprint.add_url_rule("/article/delete", view_func=article_view, methods=['DELETE'])
