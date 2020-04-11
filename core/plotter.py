import os
import json
import pathlib
import subprocess
from core.utils import url, decode, no_cache_params

HOST = os.environ['HOST']
CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
BASH_SCRIPTS_PATH = pathlib.Path(CURRENT_PATH, 'bash_scripts')
COUNTRIES_JSON_PATH = pathlib.Path(CURRENT_PATH, 'data', 'countries.json')

class Plotter(object):

    def __init__(self, country):
        with open(COUNTRIES_JSON_PATH, 'rb') as file:
            self.countries = json.load(file)

        self.country = country

    def country_name(self):
        return self.countries[self.country]['name']

    def run_command(self):
        return subprocess.run(['bash', self.BASH_COMMAND, self.country_name()], cwd=BASH_SCRIPTS_PATH, stdout=subprocess.PIPE)

    def plot(self):
        result = self.run_command()
        if result.returncode == 1: raise PlottingError('Unknown')
        return url(HOST, decode(result.stdout), no_cache_params())


class TotalPlotter(Plotter):
    BASH_COMMAND = 'plot_total.sh'
    DATAFILE_PATH = pathlib.Path(CURRENT_PATH, 'data', 'total_history.csv')

    def __init__(self, country, days):
        self.days = str(days)
        super().__init__(country)

    def run_command(self):
        return subprocess.run(['bash', self.BASH_COMMAND, self.country_name(), self.days], cwd=BASH_SCRIPTS_PATH, stdout=subprocess.PIPE)


class NewCasesPlotter(Plotter):
    BASH_COMMAND = 'plot_new.sh'
    DATAFILE_PATH = pathlib.Path(CURRENT_PATH, 'data', 'total_history.csv')


class DeathsPlotter(Plotter):
    BASH_COMMAND = 'plot_deaths.sh'
    DATAFILE_PATH = pathlib.Path(CURRENT_PATH, 'data', 'deaths_history.csv')


class RecoveredPlotter(Plotter):
    BASH_COMMAND = 'plot_recovered.sh'
    DATAFILE_PATH = pathlib.Path(CURRENT_PATH, 'data', 'recovered_history.csv')


class PlottingError(Exception):
    pass

class CommandError(Exception):
    pass

class CountryError(Exception):
    pass

class DaysError(Exception):
    pass


class CommandValidator(object):
    VALID_COMMANDS = ['total', 'new', 'deaths', 'recovered']
    with open(COUNTRIES_JSON_PATH, 'rb') as file:
        COUNTRY_NAMES = [*json.load(file).keys()]

    def valid_number(self, target):
        try:
            number = int(target)
            return number in range(0,8)
        except ValueError:
            return False

    def validate(self, command, country, days):
        if not command in self.VALID_COMMANDS: raise CommandError(f'I don\'t recognize that command. Accepted ones are {self.VALID_COMMANDS}.')
        if not country in self.COUNTRY_NAMES: raise CountryError('That\'s a country I have no data for.')
        if not self.valid_number(days): raise DaysError('Not a valid value for <days_back>. Use a number between 0 and 7 instead.')


class CommandPlotter:
    def execute(self, command, country, days):
        plotter = factory.get_command_plotter(command, country, days)
        return plotter.plot()


class CommandPlotterFactory:
    def get_command_plotter(self, command, country, days):
        CommandValidator().validate(command, country, days)
        if command == 'total':
            return TotalPlotter(country, days)
        if command == 'new':
            return NewCasesPlotter(country)
        if command == 'deaths':
            return DeathsPlotter(country)
        if command == 'recovered':
            return RecoveredPlotter(country)

factory = CommandPlotterFactory()
