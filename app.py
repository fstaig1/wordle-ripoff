from flask import Flask, render_template
from home.views import homeBlueprint

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY="LongAndRandomKey",
)


@app.route("/")
def index():
    return(render_template("index.html"))


app.register_blueprint(homeBlueprint)
app.add_url_rule("/", endpoint="index")

if __name__ == "__main__":
    app.run(debug=True)
