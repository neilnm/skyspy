import configparser

# Load configs
config = configparser.ConfigParser()
config.read('skyspy.cfg')


def get_geo_fence():
    geo_fence_coords = []
    for key in config['GEO_FENCE'].keys():
        tmp_list = config['GEO_FENCE'][key].split(',')
        # convert to float
        for index in range(len(tmp_list)):
            tmp_list[index] = float(tmp_list[index])
        geo_fence_coords.append(tuple(tmp_list))
    return geo_fence_coords


def get_home_coords():
    home_coords = config['HOME']['p1'].split(',')
    for index in range(len(home_coords)):
        home_coords[index] = float(home_coords[index])
    return tuple(home_coords)


def get_user_alt():
    return int(config['ALTITUDE']['alt'])


def get_station():
    return config['AIRPORT']['station']


def get_runway():
    return int(config['AIRPORT']['runway'])
