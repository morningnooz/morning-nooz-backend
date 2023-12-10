import azure.functions as func
from blueprints import bp

app = func.FunctionApp()
app.register_blueprint(bp)
