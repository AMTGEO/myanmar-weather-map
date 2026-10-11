from datetime import datetime
import folium
from folium.plugins import HeatMap
import requests
import streamlit as st
from streamlit_folium import st_folium

# --- 1. Mobile App UI Configuration ---
st.set_page_config(page_title="Myanmar Weather App", page_icon="🌡️", layout="centered")

# Custom CSS for Mobile Frame, Vertical/Horizontal Scrolls, and Styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 450px;
        margin: 0 auto;
        background-color: #f4f6f9;
        border-radius: 25px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-family: sans-serif;
        padding-top: 15px;
        font-weight: bold;
    }
    /* Vertical Scroll Container for Cities List */
    .vertical-scroll-container {
        max-height: 420px;
        overflow-y: auto;
        padding-right: 5px;
    }
    .vertical-scroll-container::-webkit-scrollbar {
        width: 6px;
    }
    .vertical-scroll-container::-webkit-scrollbar-thumb {
        background-color: #cbd5e1;
        border-radius: 10px;
    }
    /* Horizontal Scroll Container for Featured Cities */
    .horizontal-scroll-container {
        display: flex;
        overflow-x: auto;
        gap: 12px;
        padding: 10px 5px;
        white-space: nowrap;
        margin-bottom: 15px;
    }
    .horizontal-scroll-container::-webkit-scrollbar {
        height: 6px;
    }
    .horizontal-scroll-container::-webkit-scrollbar-thumb {
        background-color: #cbd5e1;
        border-radius: 10px;
    }
    .badge-card {
        background: white;
        padding: 10px 15px;
        border-radius: 12px;
        min-width: 110px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        flex-shrink: 0;
        border: 1px solid #e2e8f0;
    }
    .city-card {
        background: white;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 4px solid #3498db;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 2. Expanded Myanmar Cities & Notable Places Data ---
MYANMAR_CITIES = [
    {"name": "Yangon", "lat": 16.8661, "lon": 96.1951, "region": "Yangon"},
    {"name": "Mandalay", "lat": 21.9588, "lon": 96.0891, "region": "Mandalay"},
    {"name": "Naypyidaw", "lat": 19.7633, "lon": 96.0785, "region": "Naypyidaw"},
    {"name": "Bagan", "lat": 21.1717, "lon": 94.8584, "region": "Mandalay"},
    {"name": "Taunggyi", "lat": 20.7832, "lon": 97.0382, "region": "Shan"},
    {"name": "Pyin Oo Lwin", "lat": 22.0333, "lon": 96.4667, "region": "Mandalay"},
    {"name": "Mawlamyine", "lat": 16.4914, "lon": 97.6256, "region": "Mon"},
    {"name": "Pathein", "lat": 16.7833, "lon": 94.7333, "region": "Ayeyarwady"},
    {"name": "Myitkyina", "lat": 25.3833, "lon": 97.4000, "region": "Kachin"},
    {"name": "Sittwe", "lat": 20.1500, "lon": 92.9000, "region": "Rakhine"},
    {"name": "Bago", "lat": 17.3361, "lon": 96.4800, "region": "Bago"},
    {"name": "Taungoo", "lat": 18.9333, "lon": 96.4333, "region": "Bago"},
    {"name": "Magway", "lat": 20.1500, "lon": 94.9333, "region": "Magway"},
    {"name": "Hpa-An", "lat": 16.8900, "lon": 97.6333, "region": "Kayin"},
    {"name": "Loikaw", "lat": 19.6742, "lon": 97.2104, "region": "Kayah"},
    {"name": "Dawei", "lat": 14.0833, "lon": 98.2000, "region": "Tanintharyi"},
    {"name": "Myeik", "lat": 12.4381, "lon": 98.6000, "region": "Tanintharyi"},
    {"name": "Lashio", "lat": 22.9456, "lon": 97.7519, "region": "Shan"},
    {"name": "Inle Lake", "lat": 20.5731, "lon": 96.9214, "region": "Shan"},
]

# --- 3. Sidebar Configuration ---
st.sidebar.header("App Settings")
api_key = st.sidebar.text_input(
    "OpenWeatherMap API Key",
    type="password",
    help="Leave blank to use live simulation data",
)

# --- 4. Fetch Weather Data Function ---


def get_weather_data():
    weather_data = []
    for city in MYANMAR_CITIES:
        temp = 32.0
        condition = "Sunny"

        if api_key:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={city['lat']}&lon={city['lon']}&appid={api_key}&units=metric"
                res = requests.get(url, timeout=4)
                if res.status_code == 200:
                    data = res.json()
                    temp = data["main"]["temp"]
                    condition = data["weather"][0]["description"].capitalize()
            except:
                pass
        else:
            import random

            temp = round(random.uniform(26.0, 39.5), 1)

        weather_data.append(
            {
                "name": city["name"],
                "region": city["region"],
                "lat": city["lat"],
                "lon": city["lon"],
                "temp": temp,
                "condition": condition,
            }
        )
    return weather_data


# Load data
with st.spinner("Fetching latest updates..."):
    cities_weather = get_weather_data()

# --- 5. Mobile App Header ---
st.markdown(
    "<h3 class='main-header'>🇲🇲 Myanmar Weather</h3>", unsafe_allow_html=True
)
st.markdown(
    f"<p style='text-align:center; color:gray; font-size:11px; margin-bottom: 10px;'>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>",
    unsafe_allow_html=True,
)

# --- 6. Horizontal Scroll Quick Bar (Featured Cities) ---
st.markdown(
    "<p style='font-size:12px; font-weight:bold; color:#555; margin-bottom:2px;'>⚡ Quick Overview (Swipe ➡️)</p>",
    unsafe_allow_html=True,
)
quick_html = '<div class="horizontal-scroll-container">'
for c in cities_weather[:8]:
    quick_html += f"""
    <div class="badge-card">
        <div style="font-size:12px; font-weight:bold; color:#2c3e50;">{c['name']}</div>
        <div style="font-size:15px; font-weight:bold; color:#e74c3c; margin-top:4px;">{c['temp']}°C</div>
    </div>
    """
quick_html += "</div>"
st.markdown(quick_html, unsafe_allow_html=True)

# --- 7. Mobile Tabs Creation ---
tab1, tab2 = st.tabs(["🗺️ Heat Map", "🏙️ Myanmar Cities"])

# --- TAB 1: Heat Map View with Zoom ---
with tab1:
    st.markdown(
        "<p style='font-size:13px; font-weight:bold;'>Temperature Heat Map & Zoom</p>",
        unsafe_allow_html=True,
    )

    m = folium.Map(
        location=[21.9162, 95.9560],
        zoom_start=5,
        min_zoom=5,
        max_zoom=12,
        tiles="CartoDB positron",
    )

    heat_points = [[c["lat"], c["lon"], c["temp"]] for c in cities_weather]

    HeatMap(
        heat_points,
        radius=28,
        blur=18,
        max_zoom=1,
        gradient={0.2: "blue", 0.5: "lime", 0.8: "orange", 1: "red"},
    ).add_to(m)

    for c in cities_weather:
        folium.CircleMarker(
            location=[c["lat"], c["lon"]],
            radius=5,
            color="black",
            fill=True,
            fill_color="red",
            fill_opacity=0.8,
            popup=f"<b>{c['name']}</b> ({c['region']})<br>Temp: {c['temp']}°C",
        ).add_to(m)

    st_folium(m, width=380, height=360)
    st.caption(
        "🔍 Use map zoom buttons (+/-) or pinch to explore regions closely."
    )

# --- TAB 2: Myanmar Cities List View with Vertical Scroll ---
with tab2:
    st.markdown(
        "<p style='font-size:13px; font-weight:bold;'>All Districts & Notable Places</p>",
        unsafe_allow_html=True,
    )

    scrollable_list_html = '<div class="vertical-scroll-container">'
    for c in cities_weather:
        scrollable_list_html += f"""
        <div class="city-card">
            <div>
                <strong style="font-size: 15px; color: #2c3e50;">{c['name']}</strong><br>
                <span style="font-size: 11px; color: #7f8c8d;">Region: {c['region']} | {c['condition']}</span>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold; color: #e74c3c;">{c['temp']}°C</span>
            </div>
        </div>
        """
    scrollable_list_html += "</div>"

    st.markdown(scrollable_list_html, unsafe_allow_html=True)
    