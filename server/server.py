import hug
import falcon
from core.plotter import CommandPlotter, CommandError, CountryError, DaysError, PlottingError

@hug.get()
def plot(command, country, days=0):
    return {'status': 'ok', 'message': CommandPlotter().execute(command, country, days)}

@hug.get()
def info():
    text =  """
            Plotter created by:
            Kevin Martin
            https://github.com/Inobtenio
            https://twitter.com/Inobtenio

            Open source code at:
            https://github.com/Inobtenio/CoronaPlotter
            {}
            Powered by:
            Johns Hopkins CSSE (https://github.com/CSSEGISandData/COVID-19)
            Coronavirus Tracker (https://thevirustracker.com)
            COVID API by Javier Aviles (https://github.com/javieraviles/covidAPI)
            """

    return {'status': 'ok', 'message': text}

@hug.exception((CommandError,CountryError, DaysError, PlottingError)) 
def handle_custom_exceptions(exception):
    raise falcon.HTTPUnprocessableEntity(title='error', description=str(exception))

@hug.exception(Exception)
def handle_exception(exception):
    raise falcon.HTTPInternalServerError(title='error', description='Python broke again! Don\'t blame me!')
