import numpy as np
from netCDF4 import Dataset
from collections import OrderedDict
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
        contents[var] = data.variables[var][:]
    data = contents['precip']
    if len(data.shape) == 3:
        data = data.swapaxes(0, 2)
        data = data.swapaxes(0, 1)
        return data.data
    else:
        return data.data


def calculate_day_of_year(date):
    return datetime.strptime(date, "%d.%m.%Y").timetuple().tm_yday


def get_rain_amount_array_for_city(array_wit_rain_data, city):
    idx_lat = int((start_lat - coords[city.value][0]) / 0.04)
    idx_lon = int((coords[city.value][1] - start_lon) / 0.04)
    return np.round(np.sum(array_wit_rain_data[idx_lat][idx_lon]) / 365, 2)


def get_amount_of_rainign_days_for_city(array_wit_rain_data, city):
    idx_lat = int((start_lat - coords[city.value][0]) / 0.04)
    idx_lon = int((coords[city.value][1] - start_lon) / 0.04)
    return (array_wit_rain_data[idx_lat][idx_lon] != 0).sum()


def get_rain_amount_for_city_and_date(array_wit_rain_data, city, date):
    idx_lat = int((start_lat - coords[city.value][0]) / 0.04)
    idx_lon = int((coords[city.value][1] - start_lon) / 0.04)
    return array_wit_rain_data[idx_lat][idx_lon][date]


# Constants
data = read_netcdf("CCS_Poland_2020-03-25104145am_2018.nc")
start_lon = 14.12
start_lat = 54.88
coords = np.array([[53.44, 14.36], [52.72, 14.40], [51.48, 15.44], [51.04, 17.08]])


def main():
    print(data.shape)
    print(data[36][6])
    print("Average year amount of rain for", Cities.SZCZECIN, "is:", get_rain_amount_array_for_city(data, Cities.SZCZECIN))
    print("Average year rain for", Cities.KOSTRZYN_NAD_ODRA, "is:", get_rain_amount_array_for_city(data, Cities.KOSTRZYN_NAD_ODRA))
    print("Average year rain for", Cities.NOWA_SOL, "is:", get_rain_amount_array_for_city(data, Cities.NOWA_SOL))
    print("Average year rain for", Cities.TRESTNO, "is:", get_rain_amount_array_for_city(data, Cities.TRESTNO))
    print("Amount of rain on the 2.01.2018 for", Cities.TRESTNO, "is:", get_rain_amount_for_city_and_date(data, Cities.SZCZECIN, calculate_day_of_year("2.01.2018")-1))
    print(get_amount_of_rainign_days_for_city(data, Cities.SZCZECIN))

if __name__ == '__main__':
    main()
