import hug
import falcon
from core.plotter import CommandPlotter, CommandError, CountryError, DaysError, PlottingError

@hug.get(examples=['command=total&country=chile&days=2','command=recovered&country=united+kingdom&days=0'], response={'status': 'ok'})
def plot(command: hug.types.one_of(['total', 'new', 'deaths', 'recovered']), country, days: hug.types.in_range(0, 8) = 0):
    """Returns the plot image URL in the format {'status': 'ok', 'message': 'url.to/plot/image'}"""
    return {'status': 'ok', 'message': CommandPlotter().execute(command, country, days)}

@hug.get()
def info():
    """Returns the plot image URL in the format {'status': 'ok', 'message': 'large text'}"""
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
