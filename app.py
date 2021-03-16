import logging
import uuid
import traceback
from conf import settings
from flask import Flask, url_for, request, g, has_request_context
from flask.logging import default_handler
from markupsafe import escape
from myapp.database import db_session, init_db
from myapp.route.web import auth_blueprint, api_blueprint
from myapp.common.ReturnCode import ReturnError, ReturnCode
from myapp.model.users import User


class RequestFormatter(logging.Formatter):
    log_uuid = None

    def format(self, record):
        if has_request_context():
            g.uuid = uuid.uuid4().hex if 'uuid' not in g else g.uuid
            self.log_uuid = g.uuid
        record.uuid = self.log_uuid
        return super().format(record)


logger_format = '[%(uuid)s]-(%(thread)d-%(process)d)-[%(asctime)s]-[%(levelname)s] %(message)s'
ch = logging.StreamHandler()
# default_handler.setFormatter(RequestFormatter(fmt=logger_format))
ch.setFormatter(RequestFormatter(fmt=logger_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

app = Flask(__name__, static_url_path='/static', static_folder='./static')
app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/index')
def index():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         pass
#     else:
#         return

@app.before_request
def before_requests():
    logging.info('before_request')
    logging.info(f'{request.headers.environ}')
    # logging.info(f'{dict(request.headers)}')
    # headers = dict(request.headers)
    # headers = request.headers.environ
    # print(headers)
    try:
        if request.content_type != 'application/json':
        # if headers.get('CONTENT_TYPE') != 'application/json':
            raise ReturnError(901, 'Invalid content type')
        # return with not need Authorization
        if request.path in settings.except_auth_path:
            return

        if request.headers.get('Authorization') is None:
            raise ReturnError(901, 'Not provide Authorization')

        token = request.headers.get('Authorization')
        # g.user_id = User.decode_auth_token(token)
        if 'Bearer ' not in token:
            raise ReturnError(901, 'Invalid Authorization')

        g.user_id = User.decode_auth_token(token.split(' ')[1])
        return
    except ReturnError as e:
        logging.info(str(e))
        return ReturnCode.response(401, 901)

@app.teardown_request
def teardown_requests(s):
    logging.info('teardown_request')
    # def shutdown_session(exception=None):
    db_session.remove()
    return

@app.errorhandler(Exception)
def page_not_found(e):
    print(e)
    logger.debug(traceback.format_exc().replace("\n", ""))
    # raise ReturnError(904, status_code=404)
    return ReturnCode.response(404, 904, msg=str(e))
    # return 'This page does not exist', 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, load_dotenv=True, debug=settings.debug)
    # from myapp.database import init_db
    # init_db()
