import requests
import bs4
import collections

WeatherReport = collections.namedtuple('WeatherReport', 'cond, temp, scale, loc')



def main():
    print_header()

    code = input('What zipcode do you want the weather for (91210)? ')

    html = get_html_from_web(code)

    #print(code)
    # get zipcode from user
    # get html from web
    html = get_html_from_web(code)

    report = get_weather_from_html(html)
    # parse html
    # display forecast

    print('The temp in {} is {} {} and {}.'.format(
        report.loc,
        report.temp,
        report.scale,
        report.cond
    ))

def print_header():
    print('------------------------------')
    print('           Weather App')
    print('------------------------------')
    print()

def get_html_from_web(zipcode):

    url = 'https://www.wunderground.com/weather-forecast/{}'.format(zipcode)
    #print(url)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text[0:250])
    return response.text

def get_weather_from_html(html):
    soup = bs4.BeautifulSoup(html, 'lxml')
    loc = soup.find(class_='region-content-header').find('h1').get_text()
    condition = soup.find(class_='condition-icon').find('p').get_text()
    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()
    scale = soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text()
    #print(soup)


    loc = cleanup_text(loc)
    loc = find_city_and_state_from_location(loc)
    condition = cleanup_text(condition)
    temp = cleanup_text(temp)
    scale = cleanup_text(scale)

    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)
    return report



def find_city_and_state_from_location(loc: str):
    parts = loc.split('\n')
    return parts[0].strip()


def cleanup_text(text: str):
    if not text:
        return text

    text = text.strip()
    return text


if __name__ == '__main__':
    main()
