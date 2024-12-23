"""
:module: src/python/well_located_events.py
:auth: Benz Poobua
:email: spoobu (at) uw.edu
:org: University of Washington
:license: GNU GPLv3
:purpose:   This module is used to select well-located events from the MtBaker_50km_radius_origins.csv file. 
            The first-pass criteria are as follows:
                1. Events within 20 km from the Mt. Baker summit: mbs_distance_km <= 20
                2. 6+ observations (P or S wave picks): nobs >= 6
                3. 4+ observing stations: nsta >= 4
                4. no fixed values (depth, epicenter, or time): ['fdepth', 'fepi', 'ftime'] are set to False
                5. observing station distance of no more than 10 km: distance <= 10
                6. horizontal and vertical errors of 10 km or less: erhor & sdep <= 10
                7. travel time RMS misfit of no more than 1 second: wrms <= 1

"""
import os, sys, pytz, re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime
from obspy import read
from obspy.core import UTCDateTime
from obspy.clients.fdsn import Client

sys.path.append(os.path.join('..', 'python'))

from util import *

def convert_to_unix(timestamp_obj):
    """
    Convert a timestamp string with a timezone offset to a UNIX timestamp.

    The function processes a timestamp string formatted as 
    'YYYY-MM-DD HH:MM:SS[.ffffff]±HH', where the optional fractional seconds 
    and timezone offset are included. It extracts the timezone offset, localizes 
    the timestamp to that timezone, converts it to UTC, and finally returns 
    the corresponding UNIX timestamp.

    :param timestamp_obj: A string representing the timestamp, including the timezone offset.
    :type timestamp_obj: str
    :return: The UNIX timestamp corresponding to the input timestamp.
    :rtype: float
    :raises ValueError: If the offset is not found in the timestamp string.
    """
    # extract the offset
    match = re.search(r'([+-]\d{2})$', timestamp_obj)
    if match:
        offset_str = match.group(1)
        offset_hours = int(offset_str)
        offset_minutes = offset_hours * 60
    else:
        raise ValueError("Offset not found in timestamp string.")
    
    # remove the offset from the string for parsing
    timestamp_without_offset = timestamp_obj[:-3]

    # determine if there are fractional seconds
    if '.' in timestamp_without_offset:
        dt = datetime.strptime(timestamp_without_offset, '%Y-%m-%d %H:%M:%S.%f')
    else:
        dt = datetime.strptime(timestamp_without_offset, '%Y-%m-%d %H:%M:%S')

    # create timezone-aware datetime
    tz = pytz.FixedOffset(offset_minutes)
    dt = tz.localize(dt)  # localize the naive datetime to the extracted timezone
    
    # convert to UTC
    dt_utc = dt.astimezone(pytz.utc)
    
    # return UNIX timestamp
    return dt_utc.timestamp()  

def prep_data(filename, colmapping={'to_timestamp': 'origin_datetime'}):
    """
    This method reads a raw output CSV file from an AQMS file, renames columns 
    as specified by **colmapping**, and formats POSIX datetimes to UTCDateTimes.

    :param filename: Name of the CSV file to load. This should be a string that specifies the file's name.
    :type filename: str
    :param colmapping: Dictionary for column name relabeling. The keys are the 
                       original column names, and the values are the new names. 
                       Defaults to {'to_timestamp': 'origin_datetime'}.
    :type colmapping: dict, optional
    :return: 
     - **df** (*pandas.DataFrame*) -- Loaded and formatted DataFrame.

    """
    # relative path
    rrpath = os.path.join('..', '..')
    events = os.path.join(rrpath, 'data', 'Events', filename)

    # read a CSV file
    try:
        events_df = pd.read_csv(events)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

    # rename the columns
    events_df.rename(columns=colmapping, inplace=True)

    # delete rows that contain NaN in these two columns
    events_df = events_df.dropna(subset=['origin_datetime', 'nobs', 'nsta', 'distance', 'erhor', 'sdep', 'wrms'])

    events_df['origin_datetime'] = events_df['origin_datetime'].apply(convert_to_unix)

    # convert float to int
    events_df['origin_datetime'] = events_df['origin_datetime'].astype(int)

    # employ unix_to_UTCDateTime function to convert epoch times to UTC datetime
    events_df['origin_datetime'] = events_df['origin_datetime'].apply(lambda x: unix_to_UTCDateTime(x))

    # Boolean correction
    for col in ['fdepth', 'fepi', 'ftime']:
        if col in events_df.columns:
            events_df[col] = events_df[col].apply(lambda x: x=='y')
            
    # events_df.to_csv(output_path, index=False)

    return events_df

def curate_events(events_df, mbs_distance_km = 20, nobs=6, nsta=4, distance=10, erhor=10, sdep=10, wrms=1):
    # extracting well-located events from the criteria
    """
    Curate well-located events from a DataFrame based on specified criteria.

    This function filters events to identify those that are considered well-located 
    based on the following parameters. It uses cleaned data from a previous function 
    (i.e., `prep_data`) and returns a DataFrame containing only the well-located events.

    :param events_df: A DataFrame containing event data that includes observations 
                      and other relevant parameters.
    :type events_df: pd.DataFrame
    :param mbs_distance_km: Maximum distance from the Mt. Baker summit required for an event to be 
                 considered well-located. Default is 20.
    :type mbs_distance_km: int, optional
    :param nobs: Minimum number of observations required for an event to be 
                 considered well-located. Default is 6.
    :type nobs: int, optional
    :param nsta: Minimum number of stations required for an event to be 
                  considered well-located. Default is 4.
    :type nsta: int, optional
    :param distance: Maximum distance from the event to the station for 
                     consideration. Default is 10.
    :type distance: float, optional
    :param erhor: Maximum error in the horizontal location for an event to be 
                   considered well-located. Default is 10.
    :type erhor: float, optional
    :param sdep: Maximum error in the vertical location for an event to be 
                   considered well-located. Default is 10.
    :type sdep: float, optional
    :param wrms: Maximum weighted root mean square for an event to be 
                  considered well-located. Default is 1.
    :type wrms: float, optional

    :return: A DataFrame containing only the well-located events.
    :rtype: pd.DataFrame
    """
    events_df = events_df[(events_df.mbs_distance_km <= mbs_distance_km) 
                          & (events_df.nobs >= nobs)
                          & (events_df.nsta >= nsta)
                          & (events_df.distance <= distance)
                          & (events_df.erhor <= erhor)
                          & (events_df.sdep <= sdep)
                          & (events_df.wrms <= wrms)
                          & (events_df.fdepth == False)
                          & (events_df.fepi == False)
                          & (events_df.ftime == False)]
    
    # events_df.to_csv(output_path, index=False)

    return events_df