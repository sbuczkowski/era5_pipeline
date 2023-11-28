# REQUIRES Python 3.6 or higher
# developed and tested with "module load Python/3.6.4-intel-2018a"

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
        'grid': config['DEFAULT']['grid'],
        'expver': '0001',    # 5 for dates within 3 months of present?
        'levelist': config['DEFAULT']['levels'],
        'levtype': 'ml',
        'param': param,
        'stream': 'oper',
        'time': config['DEFAULT']['times'],
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
        'grid': config['DEFAULT']['grid'],
        'expver': '0001',
        'levtype': 'sfc',
        'variable': vlist,
        'stream': 'oper',
        'time': config['DEFAULT']['times'],
        'product_type': 'reanalysis',
        'format': 'netcdf'
    }, target )

#####
# Build monthly average query for surface level params
#####
def get_surf_monthly_avg(cds, year, month, target, config):
    vlist = ['sea_ice_cover',
             'surface_pressure',
             'total_cloud_cover',
             '10m_u_component_of_wind',
             '10m_v_component_of_wind',
             'skin_temperature',
             '2m_temperature',
             '2m_dewpoint_temperature']

    cds.retrieve('reanalysis-era5-single-levels-monthly-means',
                 {
                     'format': 'netcdf',
                     'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
                     'grid': config['DEFAULT']['grid'],
                     'variable': vlist,
                     'year': year,
                     'month': month,
                     #        'date': requestDates,
                     'time': config['DEFAULT']['times'],
                 },
    target)
#####
# Build monthly average query for levels params
#####
def get_levels_monthly_avg(cds, year, month, target, config):
    vlist = [ 
        'fraction_of_cloud_cover', 
        'ozone_mass_mixing_ratio', 
        'specific_cloud_ice_water_content',
        'specific_cloud_liquid_water_content', 
        'specific_humidity', 
        'temperature',
    ]

    cds.retrieve(
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'format': 'netcdf',
            'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
            'grid': config['DEFAULT']['grid'],
            'variable': vlist,
            'pressure_level': [
                '1', '2', '3',
                '5', '7', '10',
                '20', '30', '50',
                '70', '100', '125',
                '150', '175', '200',
                '225', '250', '300',
                '350', '400', '450',
                '500', '550', '600',
                '650', '700', '750',
                '775', '800', '825',
                '850', '875', '900',
                '925', '950', '975',
                '1000',
            ],
            'year': year,
            'month': month,
            'time': config['DEFAULT']['times'],
        },
    target)
#####
# Build monthly average query for 2m params
#####
def get_2m_monthly_avg(cds, year, month, target, config):
    vlist = ['2m_temperature',
             '2m_dewpoint_temperature']

    cds.retrieve('reanalysis-era5-single-levels-monthly-means',
                 {
                     'format': 'netcdf',
                     'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
                     'grid': config['DEFAULT']['grid'],
                     'variable': vlist,
                     'year': year,
                     'month': month,
                     #        'date': requestDates,
                     'time': config['DEFAULT']['times'],
                 },
    target)
#####
# Build monthly average of OLR/ILR params
#####
def get_surf_rad_monthly_avg(cds, year, month, target, config):
    vlist = ['mean_top_net_short_wave_radiation_flux_clear_sky',
             'mean_top_net_long_wave_radiation_flux_clear_sky',
             'mean_surface_net_short_wave_radiation_flux_clear_sky',
             'mean_surface_net_long_wave_radiation_flux_clear_sky',
             'mean_surface_net_short_wave_radiation_flux',
             'mean_surface_net_long_wave_radiation_flux',
             'mean_top_net_short_wave_radiation_flux',
             'mean_top_net_long_wave_radiation_flux']

    cds.retrieve('reanalysis-era5-single-levels-monthly-means',
                 {
                     'format': 'netcdf',
                     'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
                     'grid': config['DEFAULT']['grid'],
                     'variable': vlist,
                     'year': year,
                     'month': month,
                     #        'date': requestDates,
                     'time': config['DEFAULT']['times'],
                 },
    target)
