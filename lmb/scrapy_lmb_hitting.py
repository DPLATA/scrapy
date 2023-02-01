from selenium import webdriver
import pandas as pd
import json
import csv

player_hitting_lmb_stats_url = 'https://www.milb.com/mexican/stats/'
team_hitting_lmb_stats_url = 'https://www.milb.com/mexican/stats/team'

player_hitting_lmb_stats_table_xpath = '/html/body/main/div[2]/section/section/div[3]/div[1]/div/table'
team_hitting_lmb_stats_table_xpath = '/html/body/main/div[2]/section/section/div[3]/div[1]/div/table'
team_hitting_lmb_stats_table_xpath_2 = '/html/body/main/div[2]/section/section/div[3]/div[1]/div/table/tbody'


def parse_json():
    pass
    # delete first {}
    # beautify json with selenium using https://csvjson.com


def csv_to_json(csv_path, json_path):
    player_fieldnames = ['id', 'player', 'team', 'G', 'AB', 'R', 'H', '2B', '3B',
                         'HR', 'RBI', 'BB', 'SO', 'SB', 'CS',
                         'AVG', 'OBP', 'SLG', 'OPS']
    team_fieldnames = ['id', 'team', 'league', 'G', 'AB', 'R', 'H', '2B', '3B',
                       'HR', 'RBI', 'BB', 'SO', 'SB', 'CS',
                       'AVG', 'OBP', 'SLG', 'OPS']
    json_array = []

    with open(csv_path, encoding='utf-8') as csv_file:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(csv_file, fieldnames=team_fieldnames)

        for row in csv_reader:
            # add this python dict to json array
            json_array.append(row)

    # convert python json_array to JSON String and write to file
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_string = json.dumps(json_array, indent=4)
        json_file.write(json_string)


def table_to_csv(table):
    table.to_csv('../stats_files/team_hitting_LMB_stats.csv')


def scrape_table(url, xpath):
    driver = webdriver.Firefox()
    driver.get(url)
    table = pd.read_html(driver.find_element('xpath', xpath).get_attribute('outerHTML'))[0]
    table_to_csv(table)
    driver.quit()


if __name__ == '__main__':
    url = team_hitting_lmb_stats_url
    xpath = team_hitting_lmb_stats_table_xpath
    scrape_table(url, xpath)
    # JSON file append to fmex data project
    csv_to_json('../stats_files/team_hitting_LMB_stats.csv', '../stats_files/team_hitting_LMB_stats.json')
