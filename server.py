import random
import time

from flask import Flask
app = Flask(__name__)
app.debug = True


@app.route('/success')
def success_endpoint():
    return {
        "msg": "Call to this endpoint /success has succeeded"
    }, 200


@app.route('/failure')
def faulty_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        time.sleep(2)

    return {
        "msg": "call to the endpoint /failure has not succeeded"
    }, 500


@app.route('/random')
def fail_randomly_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        return {
            "msg": "Success msg"
        }, 200

    return {
        "msg": "this endpoint  will fail (sometimes)."
    }, 500

if __name__ == "__main__":
    app.run()