######
# Build and execute query for model level parameter
######
def get_level_param(cds, requestDates, param, target, config):

    #
    # cds : CDS API object
    # requestDates : string with start and end dates i.e. "20190101/TO/20190105"
    # param : ECMWF MARS variable param number i.e. 133 - specific_humidity
    # target : output filename path target
    # config : dictionary with common query params (which might change over time)
    # i.e. config = {'grid':'0.25/0.25', 'levels':'1/TO/137', 'times':'00/to/23/by/3'}

    cds.retrieve('reanalysis-era5-complete', {
        'class': 'ea',
        'date': requestDates,
        'grid': config['grid'],
        'expver': '0001',    # 5 for dates within 3 months of present?
        'levelist': config['levels'],
        'levtype': 'ml',
        'param': param,
        'stream': 'oper',
        'time': config['times'],
        'type': 'an',
        'format': 'netcdf'
    }, target )

######
# Build and execute query for surface level parameters
######
def get_surf_params(cds, requestDates, target, config):

#
# cds : CDS API object
# requestDates : string with start and end dates i.e. "20190101/TO/20190105"
# target : output filename path target
# config : dictionary with common query params (which might change over time)
#
    # surface parameters

    # params = '31.128/134.128/164.128/165.128/166.128/235.128'
    vlist = ['sea_ice_cover',
             'surface_pressure',
             'total_cloud_cover',
             '10m_u_component_of_wind',
             '10m_v_component_of_wind',
             'skin_temperature']
    cds.retrieve('reanalysis-era5-single-levels', {
        'class': 'ea',
        'date': requestDates,
        'grid': config['grid'],
        'expver': '0001',
        'levtype': 'sfc',
        'variable': vlist,
        'stream': 'oper',
        'time': config['times'],
        'product_type': 'reanalysis',
        'format': 'netcdf'
    }, target )

