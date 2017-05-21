# -*- coding: utf-8 -*-
"""
Display Yahoo! Weather forecast.

Based on Yahoo! Weather. forecast, thanks guys !
http://developer.yahoo.com/weather/

Find your woeid using:
        http://woeid.rosselliot.co.nz/

Configuration parameters:
    cache_timeout: how often to check for new forecasts (default 7200)
    forecast_days: how many forecast days you want shown (default 3)
    forecast_include_today: show today's forecast. Note that
        `{today}` in `format` shows the current conditions, while this variable
        shows today's forecast. (default False)
    forecast_text_separator: separator between forecast entries. (default ' ')
    format: uses 2 placeholders
        `forecast_text_separator`
        (default '{today} {forecasts}')
    format_forecast: format of a forecast item (default '{icon}')
    format_today: format for today `{today}` in format
        example:
        format = "Now: {icon}{temp}°{units} {text}"
        output:
        Now: ☂-4°C Light Rain/Windy
        (default '{icon}')
    icon_cloud: cloud icon, (default '☁')
    icon_default: unknown weather icon, (default '?')
    icon_rain: rain icon, (default '☂')
    icon_snow: snow icon, (default '☃')
    icon_sun: sun icon, (default '☀')
    request_timeout: check timeout (default 10)
    units: Celsius (C) or Fahrenheit (F) (default 'c')
    woeid: Yahoo woeid (extended location) (default None)

Format placeholders:
    {today} text generated by `format_today`
    {forecasts} text generated by `format_forecast`, separated by

Forcast placeholders:
    {icon} Icon representing weather
    {low} low temperature
    {high} high temperature
    {units} units 'C' or 'F'
    {text} text description of forecats

The WOEID in this example is for Paris, France => 615702

```
weather_yahoo {
    woeid = 615702
    format_today = "Now: {icon}{temp}°{units} {text}"
    forecast_days = 5
}
```

@author ultrabug, rail

SAMPLE OUTPUT
{'full_text': u'\u2602 \u2601 \u2601 \u2601'}
"""


class Py3status:

    # available configuration parameters
    cache_timeout = 7200
    forecast_days = 3
    forecast_include_today = False
    forecast_text_separator = ' '
    format = u'{today} {forecasts}'
    format_forecast = u'{icon}'
    format_today = u'{icon}'
    icon_cloud = u''
    icon_default = u'?'
    icon_rain = u''
    icon_snow = u''
    icon_sun = u'🌞'
    #icon_cloud = u''
    #icon_default = u'?'
    #icon_rain = u''
    #icon_snow = u''
    #icon_sun = u''
    request_timeout = 10
    units = 'c'
    woeid = None

    def _get_forecast(self):
        """
        Ask Yahoo! Weather. for a forecast
        """
        try:
            q = self.py3.request(
                'https://query.yahooapis.com/v1/public/yql?q=' +
                'select * from weather.forecast ' +
                'where woeid="{woeid}" and u="{units}"&format=json'.format(
                    woeid=self.woeid, units=self.units.lower()[0]) +
                '&env=store://datatables.org/alltableswithkeys',
                timeout=self.request_timeout
            )
        except (self.py3.RequestException):
            return None, None
        if q.status_code != 200:
            self.py3.log('Non 200 http response returned code %s' % q.status_code)
            return None, None
        r = q.json()
        try:
            today = r['query']['results']['channel']['item']['condition']
            forecasts = r['query']['results']['channel']['item']['forecast']
        except TypeError:
            return None, None
        if not self.forecast_include_today:
            # Do not include today in forecasts
            forecasts.pop(0)
        # limit to forecast_days
        forecasts = forecasts[:self.forecast_days]
        # return current today + forecast_days days forecast
        return today, forecasts

    def _get_icon(self, forecast):
        """
        Return an unicode icon based on the forecast code and text
        See: http://developer.yahoo.com/weather/#codes
        """
        code = int(forecast['code'])
        text = forecast['text'].lower()

        # sun
        if 'sun' in text or code in [31, 32, 33, 34, 36]:
            return self.icon_sun

        # cloud / early rain
        if 'cloud' in text or code in [
                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                44
        ]:
            return self.icon_cloud

        # rain
        if 'rain' in text or code in [
                0, 1, 2, 3, 4, 5, 6, 9,
                11, 12,
                37, 38, 39,
                40, 45, 47
        ]:
            return self.icon_rain

        # snow
        if 'snow' in text or code in [
                7, 8,
                10, 13, 14, 15, 16, 17, 18,
                35,
                41, 42, 43, 46
        ]:
            return self.icon_snow

        return self.icon_default

    def weather_yahoo(self):
        """
        This method gets executed by py3status
        """
        if not self.woeid:
            raise Exception('missing woeid setting, please configure it')
        response = {
            'cached_until': self.py3.time_in(self.cache_timeout),
            'full_text': ''
        }

        today, forecasts = self._get_forecast()
        if today is None and forecasts is None:
            response['cached_until'] = self.py3.time_in(30)
            return response
        units = self.units.upper()[0]
        today_text = self.py3.safe_format(
            self.format_today,
            dict(icon=self._get_icon(today), units=units, **today)
        )
        forecast_text = self.forecast_text_separator.join(
            self.py3.safe_format(
                self.format_forecast,
                dict(icon=self._get_icon(f), units=units, **f)
            ) for f in forecasts)

        response['full_text'] = self.py3.safe_format(
            self.format, dict(today=today_text, forecasts=forecast_text)
        )
        return response


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
