from flask import Flask, jsonify
from flask.views import MethodView

import task3


app = Flask(__name__)

class BaseView(MethodView):
    def get(self):
        data = task3.main()
        return jsonify(data)



app.add_url_rule('/', view_func=BaseView.as_view('test3'))

if __name__ == '__main__':
    app.run()