########################################### INFO ####################################################
# This is a Wrangle for obtaining data on NASA's robotic lander 'Insight', which can be found here: #
# https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_raw/sol_0000_0122/                 #
#                                                                                                   #
# Created By Jeanette Schulz | Last Updated: 18 JAN 2022                                            #
########################################## Imports ##################################################
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os

####################################### Data Scraping ###############################################

def web_scrape_all():
    """
    This function takes time to process. The function requests a response from a specific url with a list of
    files to download. This function collects a list of the names of all the csv files, uses this list to 
    download all the csv's individually, and then combines all the csv's into one file named "INSIGHT_DATA.csv".
    This function will also return the new dataframe.
    """
    # Informing the User
    print("Requesting Data...")  
    
    # The web page that will be scraped:
    url = "https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_raw/sol_0000_0122/"
    
    # Requesting page information
    response = get(url)
    
    # Turning page information into chunks of soup
    soup = BeautifulSoup(response.text)
    
    # The csv file names I'm after are under anchor tags
    links = soup.find_all("a")
    
    # Creating a list of all the listed file names written in the "href"
    links = [link["href"] for link in links]
    
    # Delete garbage in the list of links so we only have the .csv names
    temporary_list= []
    for link in links:
        if link.endswith('.csv'): # If the link ends in .csv, add it to new_list
            temporary_list.append(link)

        else: # If link does not end in .csv, move on
            continue
    links = temporary_list
    
    # Informing the User
    print("Creating local copies...")
    
    # Create a local copy of all the .csv files from the website
    for link in links:
        # Read from the internet
        df = pd.read_csv(url + link)
        # Write locally to disk
        df.to_csv(link)
    
    # Informing the User
    print("Combining csv files...")
    
    # Combine all csv files into a SUPER file!
    # Creating the first Dataframe 
    df = pd.DataFrame()
    for link in links: 
        # Append file to dataframe
        df = df.append(pd.DataFrame(pd.read_csv(link)))
    
    # Dropping the additional index column 
    df= df.drop('Unnamed: 0', axis=1)
    
    # If csv file does not exist, create it.
    if os.path.isfile('INSIGHT_DATA.csv'):
        # Informing the User
        print("Creating super file...")
        
        # Now to write the combined csv dataframe to a single file
        df.to_csv('INSIGHT_DATA.csv')
        
        # Informing the User
        print("'INSIGHT_DATA.csv' created.")
    
    return df


def twins_raw_data():
    """
    This function takes time to process, and only scrapes data for TWINS_RAW. The function requests a response from a specific url with a list of
    files to download. This function collects a list of the names of all the csv files, uses this list to 
    download all the csv's individually, and then combines all the csv's into one file named "INSIGHT_TWINS_RAW.csv".
    This function will also return the new dataframe.
    """
    # If csv file exists read in data from csv file.
    if os.path.isfile('INSIGHT_TWINS_RAW.csv'):
        # Informing the User
        print("Reading Data from local file...") 
        df = pd.read_csv('INSIGHT_TWINS_RAW.csv', index_col=0)
    
    else:
        # Informing the User
        print("Requesting Data from web...")  
        
        # The web page that will be scraped:
        url = "https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_raw/sol_0000_0122/"
        
        # Requesting page information
        response = get(url)
        
        # Informing the User
        print("Organizing list of file names...") 

        # Turning page information into chunks of soup
        soup = BeautifulSoup(response.text)
        
        # The csv file names I'm after are under anchor tags
        links = soup.find_all("a")
        
        # Creating a list of all the listed file names written in the "href"
        links = [link["href"] for link in links]
        
        # Delete garbage in the list of links so we only have the .csv names
        temporary_list= []
        for link in links:
            if link.endswith('.csv'): # If the link ends in .csv, add it to new_list
                temporary_list.append(link)

            else: # If link does not end in .csv, move on
                continue
        links = temporary_list
        
        # Separating "twins_raw" data from list
        twins_raw_list = []
        for link in links:
            if link.startswith("twins_rawevent"):
                continue
            elif link.startswith("twins_raw"):
                twins_raw_list.append(link)
            else:
                continue
                
        # Informing the User
        print("Combining twins_raw csv files...")
        
        # Combining all Twins_raw csv files into a SUPER file!
        # Creating the first Dataframe 
        df = pd.DataFrame()

        for link in twins_raw_list: 
            # Append file to dataframe
            df = df.append(pd.DataFrame(pd.read_csv(link)))

        # Dropping the additional index column 
        df= df.drop('Unnamed: 0', axis=1)
      
        # Informing the User
        print("Creating local file...")
        
        # Now to write the combined csv dataframe to a single file
        df.to_csv('INSIGHT_TWINS_RAW.csv')
        
        # Informing the User
        print("'INSIGHT_TWINS_RAW.csv' created.")
        
    return df

##################################### Prepare the Data ##############################################

def prepare_TWINS():
    # Read in data and drop unneeded columns
    df = pd.read_csv('MVP2.csv').reset_index(drop=True)
    df = df.drop(columns=['Unnamed: 0', 'local_true_solar_time'])

    # Converting earth_date to datetime dtype
    df.earth_date = pd.to_datetime(df.earth_date, format = '%Y-%m-%d %H:%M:%S')

    # Setting the 'earth_date' column as the Index and sorting that new Index:
    df = df.set_index('earth_date').sort_index()
    
    return df