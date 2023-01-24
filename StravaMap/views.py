import folium
import pandas as pd
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404
from stravalib.client import Client as StravaClient
from StravaAuth.strava_auth import StravaAuth


# Create your views here.
def base_map(request):
    # Make your map object
    main_map = folium.Map(location=[43.45, -80.476], zoom_start=12)  # Create base map
    main_map_html = main_map._repr_html_()  # Get HTML for website

    context = {
        "main_map": main_map_html
    }
    return render(request, 'index.html', context)


def connected_map(request):
    # Make your map object
    main_map = folium.Map(location=[43.45, -80.476], zoom_start=12)  # Create base map

    client = StravaAuth(request)

    curr_athlete = client.get_athlete()
    print(curr_athlete)
    # activites_url = "https://www.strava.com/api/v3/athlete/activities"

    # # Get activity data
    # header = {'Authorization': 'Bearer ' + str(client.strava_tokens['access_tokens'])}
    # activity_df_list = []
    # for n in range(5):  # Change this to be higher if you have more than 1000 activities
    #     param = {'per_page': 200, 'page': n + 1}
    #
    #     activities_json = requests.get(activites_url, headers=header, params=param).json()
    #     if not activities_json:
    #         break
    #     activity_df_list.append(pd.json_normalize(activities_json))
    # # # Get Polyline Data
    # # activities_df = pd.concat(activity_df_list)
    #
    # activities_df = activities_df.dropna(subset=['map.summary_polyline'])
    # activities_df['polylines'] = activities_df['map.summary_polyline'].apply(polyline.decode)
    #
    # # Plot Polylines onto Folium Map
    # for pl in activities_df['polylines']:
    #     folium.PolyLine(locations=pl, color='red').add_to(main_map)

    # Return HTML version of map
    main_map_html = main_map._repr_html_()  # Get HTML for website
    context = {
        "main_map": main_map_html
    }
    return render(request, 'index.html', context)

#
# @login_required
def profile(request):

    strava_tokens = StravaAuth().strava_tokens()
    client = StravaClient(access_token=strava_tokens['access_token'])
    athlete = client.get_athlete()

    context = {
        "athlete": athlete
    }
    return render(request, 'profile.html', context)




if __name__ == "__main__":
    profile()



#
