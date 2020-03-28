import json
import os.path
import requests
import sys
import pandas as pd
import io

import US_state_daily as US
import Italy_daily as Italy

if __name__=="__main__":

    print("Getting and saving US data")
    US.scrape()
    print("Getting and saving Italy data")
    Italy.scrape()
