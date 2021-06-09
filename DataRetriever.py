from covid import Covid
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
import difflib

class DataRetriever():

    def __init__(self):
        self.covid = Covid()
        pass

    def getListOfCountries(self):
        return sorted([[i['name'].lower(), i['id']] for i in self.covid.list_countries()])

    def getWorldData(self):
        world_data = {}
        world_data['global_cases'] = self.covid.get_total_confirmed_cases()
        world_data['global_recovered'] = self.covid.get_total_recovered()
        world_data['global_active_cases'] = self.covid.get_total_active_cases()
        world_data['global_deaths'] = self.covid.get_total_deaths()
        return world_data

    def getDataById(self, country):
        return (self.covid.get_status_by_country_id(country))

    def getCountryDataText(self, country):
        country = self.getDataById(country)
        name = country['country']
        conf_cases = "Confirmed cases: " + locale.format_string('%d', (country['confirmed']), 1)
        act_cases = "Active cases: " + locale.format_string('%d', (country['active']), 1)
        deaths = "Deaths: " + locale.format_string('%d', (country['deaths']), 1)
        recovered = "Recovered: " + locale.format_string('%d', (country['recovered']), 1)
        text = "Country: " + str(name) + "\n" + str(conf_cases) + "\n" + str(act_cases) + "\n" + str(
            deaths) + "\n" + str(recovered)
        return text

    def getWorldDataText(self):
        world_deaths = "Deaths: " + locale.format_string('%d', self.covid.get_total_deaths(), 1)
        world_cases = "Active cases: " + locale.format_string('%d', self.covid.get_total_active_cases(), 1)
        world_recovered = "Recovered: " + locale.format_string('%d', self.covid.get_total_recovered(), 1)
        world_confirmed_cases = "Confirmed cases: " + locale.format_string('%d', self.covid.get_total_confirmed_cases(), 1)
        text = "Coronavirus Worldwide 🌍🌎" + "\n" + str(world_confirmed_cases) + "\n" + str(world_cases) + "\n" + str(
            world_deaths) + "\n" + str(world_recovered)
        return text

    def getListOfCountriesText(self):
        return (', '.join(i[0] for i in self.getListOfCountries()))

    def didYouMean(self, word):
        matches = difflib.get_close_matches(word, self.getListOfCountries(), 10, 0.4)
        return '\n'.join(sorted(matches))

    def convertCountryToId(self,country):
        for i in self.getListOfCountries():
            if i[0] == country:
                return i[1]
