import json
import os.path
import requests
import sys
import pandas as pd
import io

import US_state_daily as US_state
import US_county_daily as US_county
import Italy_daily as Italy
import country_daily as world
import China_jhu as China
import Canada_jhu as Canada
import Australia_jhu as Australia

if __name__=="__main__":

    print("Getting and saving US state data")
    US_state.scrape()
    print("Getting and saving US county data")
    US_county.scrape()
    print("Getting and saving Italy data")
    Italy.scrape()
    print("Getting and saving World data from JHU website")
    world.scrape()
    print("Getting and saving China data from JHU website timeseries")
    China.scrape()
    print("Getting and saving Canada data from JHU website timeseries")
    Canada.scrape()
    print("Getting and saving Australia data from JHU website timeseries")
    Australia.scrape()
