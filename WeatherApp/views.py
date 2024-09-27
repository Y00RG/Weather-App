from django.shortcuts import render, redirect
import urllib.request
import json

def index(request):
    data = {}  # Initialize data variable
    if request.method == 'POST':
        city_input = request.POST['city'].strip()
        # Validate city input before sending a request
        if city_input:
            if ',' in city_input:
                city, country_code = city_input.split(',')
                city = city.strip().title()
                country_code = country_code.strip().upper()
            else:
                city = city_input.strip().title()
                country_code = ''
            # Construct the API URL
            if country_code:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&units=metric&appid=92702fdec9c200c93a8224384ad257d4'
            else:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=92702fdec9c200c93a8224384ad257d4'
            
            print(f"Requesting URL: {url}")  # Debugging line
            try:
                # Fetch weather data
                source = urllib.request.urlopen(url).read()
                list_of_data = json.loads(source)
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                    "temp": f"{list_of_data['main']['temp']} °C",
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": f"{list_of_data['main']['humidity']}%",
                    "main": str(list_of_data['weather'][0]['main']),
                    "description": str(list_of_data['weather'][0]['description']),
                    "icon": list_of_data['weather'][0]['icon'],
                }
                # Store data in session and redirect to prevent POST on refresh
                request.session['weather_data'] = data
                return redirect('index')  # Redirect to the same page (GET request)
            except urllib.error.HTTPError as e:
                error_message = e.read().decode()  # Read the error message
                data = {"error": f"City not found. {error_message}"}
                request.session['weather_data'] = data
                return redirect('index')

    # If a GET request or after redirect, retrieve weather data from session
    data = request.session.get('weather_data', {})
    return render(request, "index.html", data)
