from flask import Flask, request, abort, jsonify

from .pudding_model.single_data_processor import SingleDataProcessor
from .pudding_model.trainer import Trainer

fpm = Trainer().train_model()
sdp = SingleDataProcessor()

app = Flask(__name__)


@app.route('/health-probe')
def hello_pudding():
    if fpm is not None:
        return 'Hello from pudding!'
    else:
        return 'Pudding is not ready! ://'


@app.errorhandler(404)
@app.route('/', methods=['POST'])
def predict():
    json = request.get_json()
    if json is None:
        abort(400, 'Expected a JSON object but not found')

    name = json["name"]
    year = json["year"]

    if name is None or year is None:
        abort(400, "Json doesn't contain name and year field")

    x = sdp.film_to_input(name, year)
    pred = fpm.predict(x)[0] * 5
    print(pred)

    return jsonify({"prediction": pred})
