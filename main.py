import numpy as np
from netCDF4 import Dataset
from collections import OrderedDict
import numpy as np
from enum import Enum
from datetime import datetime


class Cities(Enum):
	SZCZECIN = 0
	KOSTRZYN_NAD_ODRA = 1
	NOWA_SOL = 2
	TRESTNO = 3


def read_netcdf(netcdf_file):
	contents = OrderedDict()
	data = Dataset(netcdf_file, 'r')
	for var in data.variables:
		attrs = data.variables[var].ncattrs()
		contents[var] = data.variables[var][:]
	data = contents['precip']
	if len(data.shape) == 3:
		data = data.swapaxes(0, 2)
		data = data.swapaxes(0, 1)
		return data
	else:
		return data


def calculate_day_of_year(date):
    return datetime.strptime(date, "%d.%m.%Y").timetuple().tm_yday


def get_rain_amount_array_for_city(array_wit_rain_data, city):
    idx_lat = int((start_lat - coords[city.value][0]) / 0.04)
    idx_lon = int((coords[city.value][1] - start_lon) / 0.04)
    print("Year average for", city.name, "is:", np.sum(array_wit_rain_data[idx_lat][idx_lon])/365)


def get_rain_amount_for_city_and_date(array_wit_rain_data, city, date):
    idx_lat = int((start_lat - coords[city.value][0]) / 0.04)
    idx_lon = int((coords[city.value][1] - start_lon) / 0.04)
    print("Amount of rain for", city.name, "is:", array_wit_rain_data[idx_lat][idx_lon][date])


# Constants
data = read_netcdf("CCS_Poland_2020-03-25104145am_2018.nc")
start_lon = 14.12
start_lat = 54.88
coords = np.array([[53.44, 14.36], [52.72, 14.40], [51.48, 15.44], [51.04, 17.08]])


def main():
    get_rain_amount_array_for_city(data.data, Cities.SZCZECIN)
    get_rain_amount_array_for_city(data.data, Cities.KOSTRZYN_NAD_ODRA)
    get_rain_amount_array_for_city(data.data, Cities.NOWA_SOL)
    get_rain_amount_array_for_city(data.data, Cities.TRESTNO)
    get_rain_amount_for_city_and_date(data.data, Cities.SZCZECIN, calculate_day_of_year("1.01.2018"))


if __name__ == '__main__':
    main()
