from bs4 import BeautifulSoup
import csv
import os
import re
import requests

sb6183 = {
    "product information": "http://192.168.100.1/RgSwInfo.asp",
    "addresses": "http://192.168.100.1/RgAddress.asp",
    "status": "http://192.168.100.1/RgConnect.asp",
    "event log": "http://192.168.100.1/RgEventLog.asp",
    "configuration": "http://192.168.100.1/RgConfiguration.asp"
}


def get_soup(url: str, page_name: str) -> BeautifulSoup:
    print(f"Requesting {page_name}...")
    result = requests.get(url)
    assert result.status_code == 200, f"Status code {result.status_code} returned."
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    # print(soup.prettify())
    return soup


def get_product_information() -> None:
    key = "product information"
    soup = get_soup(sb6183[key], key)
    soup_tds = soup.find_all('td')
    tds = [soup_td.text for soup_td in soup_tds]
    fields = [
        'Standard Specification Compliant',
        'Hardware Version',
        'Software Version',
        'Cable Modem MAC Address',
        'Serial Number',
        'Up Time'
    ]
    for field in fields:
        try:
            value_index = tds.index(field)
        except ValueError:
            print(f"Error: {field} not found in {tds}!")
            continue
        data_frame[field] = tds[value_index + 1]


def get_addresses() -> None:
    key = "addresses"
    soup = get_soup(sb6183[key], key)
    soup_tds = soup.find_all('td')
    tds = [soup_td.text for soup_td in soup_tds]
    fields = [
        'Serial Number',
        'HFC MAC Address',
        'Known CPE MAC Address',
        '2'
    ]
    for field in fields:
        try:
            value_index = tds.index(field)
        except ValueError:
            print(f"Error: {field} not found in {tds}!")
            continue
        data_frame[field] = tds[value_index + 1]
    data_frame[fields[-2]] = data_frame.pop(fields[-1])


def get_status() -> None:
    key = "status"
    soup = get_soup(sb6183[key], key)
    soup_tds = soup.find_all('td')
    tds = [soup_td.text for soup_td in soup_tds]
    fields = [
        'Acquire Downstream Channel',
        'Connectivity State',
        'Boot State',
        'Configuration File',
        'Security',
        'DOCSIS Network Access Enabled'
    ]
    for field in fields:
        try:
            value_index = tds.index(field + '\r')
        except ValueError:
            print(f"Error: {field} not found in {tds}!")
            continue
        data_frame[field] = tds[value_index + 1].strip(), tds[value_index + 2].strip()
    downstream_channels = []
    upstream_channels = []
    try:
        downstream_fields = [
            'Channel',
            'Lock Status',
            'Modulation',
            'Channel ID',
            'Frequency',
            'Power',
            'SNR',
            'Corrected',
            'Uncorrectables'
        ]
        upstream_fields = [
            'Channel',
            'Lock Status',
            'US Channel Type',
            'Channel ID',
            'Symbol Rate',
            'Frequency',
            'Power'
        ]
        downstream_index = tds.index(downstream_fields[-1]) + 1
        upstream_index = tds.index(upstream_fields[0], downstream_index + 1)
        while downstream_index < upstream_index:
            downstream_channel = {}
            for field in downstream_fields:
                downstream_channel[field] = tds[downstream_index].strip()
                downstream_index += 1
            downstream_channels.append(downstream_channel)
        data_frame['Downstream Channels'] = downstream_channels
        upstream_index += len(upstream_fields)
        while upstream_index < len(tds):
            upstream_channel = {}
            for field in upstream_fields:
                upstream_channel[field] = tds[upstream_index].strip()
                upstream_index += 1
            upstream_channels.append(upstream_channel)
        data_frame['Upstream Channels'] = upstream_channels
    except ValueError:
        print("Error: Unable to find channel index!")


def get_event_log() -> None:
    key = "event log"
    soup = get_soup(sb6183[key], key)
    soup_tds = soup.find('table', class_='simpleTable').find_all('td')
    tds = [soup_td.text for soup_td in soup_tds]
    tds.pop()  # last td is clear log button
    assert len(tds) % 3 == 0, f"Event log size is {len(tds)} and not divisible by 3!"
    events = []
    event_fields = [
        'Time',
        'Priority',
        'Description'
    ]
    td_index = 0
    while td_index < len(tds):
        event = {}
        for field in event_fields:
            event[field] = tds[td_index].strip()
            td_index += 1
        events.append(event)
    data_frame['Event Log'] = events


if __name__ == '__main__':
    data_frame = {}
    get_product_information()
    get_addresses()
    get_status()
    get_event_log()
    [print(f"{key}: {value}") for key, value in data_frame.items()]
