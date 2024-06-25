import matplotlib.pyplot as plt
import netCDF4
import numpy as np
from mpl_toolkits.basemap import Basemap


def get_u_v_currents(nc_file: str, target_lat: float, target_lon: float):
    dataset = netCDF4.Dataset(nc_file)

    # Extrae las variables necesarias
    latitudes = dataset.variables['Latitude'][:]
    longitudes = dataset.variables['Longitude'][:]
    u_currents = dataset.variables['u_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa
    v_currents = dataset.variables['v_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa

    # Manejar valores inválidos
    longitudes = np.where(np.greater_equal(longitudes, 500), np.nan, longitudes)

    # Normalizar las longitudes para que estén en el rango [-180, 180]
    longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)

    # Encontrar el índice más cercano a la latitud y longitud objetivo
    lat_diff = np.abs(latitudes - target_lat)
    lon_diff = np.abs(longitudes - target_lon)
    total_diff = lat_diff + lon_diff

    min_diff_index = np.unravel_index(np.nanargmin(total_diff, axis=None), total_diff.shape)
    nearest_lat = latitudes[min_diff_index]
    nearest_lon = longitudes[min_diff_index]
    u_current = u_currents[min_diff_index]
    v_current = v_currents[min_diff_index]

    # Asegúrate de que los valores no sean NaN
    if np.isnan(nearest_lat) or np.isnan(nearest_lon):
        print("Error: No se encontraron coordenadas válidas cercanas a las especificadas.")
        return

    # Cierra el dataset
    dataset.close()

    return u_current, v_current


def process(nc_file: str, target_lat: float, target_lon: float):
    dataset = netCDF4.Dataset(nc_file)

    # Extrae las variables necesarias
    latitudes = dataset.variables['Latitude'][:]
    longitudes = dataset.variables['Longitude'][:]
    u_currents = dataset.variables['u_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa
    v_currents = dataset.variables['v_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa

    # Manejar valores inválidos
    longitudes = np.where(np.greater_equal(longitudes, 500), np.nan, longitudes)

    # Normalizar las longitudes para que estén en el rango [-180, 180]
    longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)

    # Encontrar el índice más cercano a la latitud y longitud objetivo
    lat_diff = np.abs(latitudes - target_lat)
    lon_diff = np.abs(longitudes - target_lon)
    total_diff = lat_diff + lon_diff

    min_diff_index = np.unravel_index(np.nanargmin(total_diff, axis=None), total_diff.shape)
    nearest_lat = latitudes[min_diff_index]
    nearest_lon = longitudes[min_diff_index]
    u_current = u_currents[min_diff_index]
    v_current = v_currents[min_diff_index]

    print(f"nearest_lat: {nearest_lat}")
    print(f"nearest_lon: {nearest_lon}")
    print(f"u_current: {u_current}")
    print(f"v_current: {v_current}")

    # Asegúrate de que los valores no sean NaN
    if np.isnan(nearest_lat) or np.isnan(nearest_lon):
        print("Error: No se encontraron coordenadas válidas cercanas a las especificadas.")
        return

    # Configura la proyección del mapa
    m = Basemap(projection='mill', lat_ts=10,
                llcrnrlon=nearest_lon - 1, urcrnrlon=nearest_lon + 1,
                llcrnrlat=nearest_lat - 1, urcrnrlat=nearest_lat + 1,
                resolution='c')

    # Convierte los valores de lat/lon a x/y en la proyección del mapa
    x, y = m(nearest_lon, nearest_lat)

    # Crear una figura
    plt.figure(figsize=(12, 8))

    # Añadir la malla de corrientes marinas usando quiver
    m.quiver(x, y, u_current, v_current, scale=10, color='b', alpha=0.5)

    # Añadir líneas de costa y otras características del mapa
    m.drawcoastlines()
    m.fillcontinents(color='lightgray', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')
    m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

    # Añadir título y mostrar el gráfico
    plt.title(f'Corrientes marinas en ({nearest_lat:.2f}, {nearest_lon:.2f})')
    plt.show()

    # Cierra el dataset
    dataset.close()


def view_data(nc_file: str):
    dataset = netCDF4.Dataset(nc_file)

    # Extrae las variables necesarias
    latitudes = dataset.variables['Latitude'][:]
    longitudes = dataset.variables['Longitude'][:]
    u_currents = dataset.variables['u_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa
    v_currents = dataset.variables['v_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa

    # print(dataset.variables["Latitude"])
    # print(dataset.variables["Longitude"])

    # Print all latitudes values
    print("Latitudes----------------")
    print(latitudes)
    print("Longitudes----------------")
    print(longitudes)


def print_dataset_stats(nc_file: str):
    dataset = netCDF4.Dataset(nc_file)
    print("Dataset.variables----------------")
    print(dataset.variables)


def find_first_non_empty_uv(nc_file: str):
    dataset = netCDF4.Dataset(nc_file)

    # Extrae las variables necesarias
    u_currents = dataset.variables['u_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa
    v_currents = dataset.variables['v_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa

    # Encuentra el índice del primer valor no "--" en u_velocity
    u_index = np.where(u_currents != "--")
    if len(u_index[0]) == 0:
        print("No se encontraron valores válidos en u_velocity.")
    else:
        u_lat_index, u_lon_index = u_index
        first_u_lat = u_lat_index[0]
        first_u_lon = u_lon_index[0]
        print(f"Primer valor no '--' en u_velocity encontrado en latitud: {first_u_lat}, longitud: {first_u_lon}")

    # Encuentra el índice del primer valor no "--" en v_velocity
    v_index = np.where(v_currents != "--")
    if len(v_index[0]) == 0:
        print("No se encontraron valores válidos en v_velocity.")
    else:
        v_lat_index, v_lon_index = v_index
        first_v_lat = v_lat_index[0]
        first_v_lon = v_lon_index[0]
        print(f"Primer valor no '--' en v_velocity encontrado en latitud: {first_v_lat}, longitud: {first_v_lon}")

    # Cierra el dataset
    dataset.close()


# Ejemplo de uso:
if __name__ == "__main__":
    nc_file = "../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
    target_lat = 20
    target_lon = -60

    # process(nc_file, target_lat, target_lon)
    find_first_non_empty_uv(nc_file)
    # view_data(nc_file)
    print_dataset_stats(nc_file)
    # find_first_non_empty_uv(nc_file)
    # get_u_v_currents(nc_file, target_lat, target_lon)
