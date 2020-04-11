import hug
import falcon
from core.plotter import CommandPlotter, CommandError, CountryError, DaysError, PlottingError

@hug.get(examples=['command=total&country=chile&days=2','command=recovered&country=united+kingdom&days=0'])
def plot(command, country, days=0):
    """ Returns the plot image URL in the format {'status': 'ok', 'message': 'url.to/plot/image'}
    Accepted values for <command> are: (total|new|deaths|recovered)
    <days> must be in the (0,8) range. This includes 0 and 7."""

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
            """

    return {'status': 'ok', 'message': text}

@hug.exception((CommandError,CountryError, DaysError, PlottingError)) 
def handle_custom_exceptions(exception):
    raise falcon.HTTPUnprocessableEntity(title='error', description=str(exception))

@hug.exception(Exception)
def handle_exception(exception):
    raise falcon.HTTPInternalServerError(title='error', description='Python broke again! Don\'t blame me!')
