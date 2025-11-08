#!/usr/bin/env python

import os, cdsapi, datetime, pandas as pd
server = cdsapi.Client()
from optparse import OptionParser
class clr:END,RED,GREEN,MAGENTA,CYAN = '\033[0m','\033[31m','\033[32m','\033[35m','\033[36m'

usage = f'''
  {clr.GREEN}python down_era5.get_nudging.py --start-date=<yyyymmdd> --final-date=<yyyymmdd> --output-root=<path>{clr.END}
'''
parser = OptionParser(usage=usage)
parser.add_option('--start-date',  dest='start_date',  default=None,  help='date of first file [yyyymmdd]')
parser.add_option('--final-date',  dest='final_date',  default=None,  help='date of last file [yyyymmdd]')
parser.add_option('--output-root', dest='output_root', default='./',  help='Output path for data files (default is PWD)')
(opts, args) = parser.parse_args()

# check that input arguments are valid
if opts.start_date is None: raise ValueError(f'{clr.RED}initialization date was not specified{clr.END}')
if opts.final_date is None: opts.final_date = opts.start_date

beg_date = datetime.datetime.strptime(f'{opts.start_date}', '%Y%m%d')
end_date = datetime.datetime.strptime(f'{opts.final_date}', '%Y%m%d')
datetime_list = pd.date_range(beg_date, end_date, freq="MS")
print(datetime_list)

lev = [  '1',  '2',  '3',  '5',  '7', '10', '20', '30', '50', '70','100','125',
       '150','175','200','225','250','300','350','400','450','500','550','600',
       '650','700','750','775','800','825','850','875','900','925','950','975','1000']

get_atm = True
get_sfc = True
get_lnd = False

for t in datetime_list:
  #-----------------------------------------------------------------------------
  # parse date/time information
  yr = t.strftime("%Y")
  mn = t.strftime("%m")
  dy = t.strftime("%d")
  #-----------------------------------------------------------------------------
  # Specify output file names
  output_file_plv = f'{opts.output_root}/ERA5.atm.{yr}-{mn}.nc'
  output_file_mlv = output_file_plv.replace('.atm.','.mlev.')
  output_file_sfc = output_file_plv.replace('.atm.','.sfc.')
  #-----------------------------------------------------------------------------
  # atmossphere pressure level data
  if get_atm:
      server.retrieve('reanalysis-era5-pressure-levels',{
        'product_type'  : 'reanalysis',
        'format'        : 'netcdf',
        'pressure_level': lev,
        'time'          : ['00:00', '06:00', '12:00','18:00'],
        'day'           : ['01', '02', '03','04', '05', '06',
                           '07', '08', '09','10', '11', '12',
                           '13', '14', '15','16', '17', '18',
                           '19', '20', '21','22', '23', '24',
                           '25', '26', '27','28', '29', '30',
                           '31'],
        'month'         : mn,
        'year'          : yr,
        'variable'      : ['temperature'
                          ,'specific_humidity'
                          ,'geopotential'
                          ,'u_component_of_wind'
                          ,'v_component_of_wind'
                          ,'ozone_mass_mixing_ratio'
                          ,'specific_cloud_ice_water_content'
                          ,'specific_cloud_liquid_water_content'
                          ],
      }, output_file_plv)
  #-----------------------------------------------------------------------------
  # surface data
  if get_sfc:
      server.retrieve('reanalysis-era5-single-levels',{
        'product_type'  : 'reanalysis',
        'format'        : 'netcdf',
        'time'          : ['00:00', '06:00', '12:00','18:00'],
        'day'           : ['01', '02', '03','04', '05', '06',
                           '07', '08', '09','10', '11', '12',
                           '13', '14', '15','16', '17', '18',
                           '19', '20', '21','22', '23', '24',
                           '25', '26', '27','28', '29', '30',
                           '31'],
        'month'         : mn,
        'year'          : yr,
        'variable'      : ['surface_pressure'
                          ,'skin_temperature'
                          ,'sea_surface_temperature'
                          ,'2m_temperature'
                          ,'soil_temperature_level_1'
                          ,'soil_temperature_level_2'
                          ,'soil_temperature_level_3'
                          ,'soil_temperature_level_4'
                          ,'snow_depth'
                          ,'temperature_of_snow_layer'
                          ,'geopotential'
                          ,'sea_ice_cover'
                          ],
      }, output_file_sfc)