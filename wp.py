import streamlit as st
import urllib.request
import urllib.error
import json

# ---------- PAGE CONFIG ----------
# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
/* ---------- BACKGROUND GRADIENT (Green to Blue) ---------- */
.stApp {
    background: linear-gradient(135deg, #a8e6cf, #4db6ac); /* light green to teal-blue */
    color: #ffffff;
}

/* ---------- TITLE & SUBTITLE ---------- */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 0px;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    margin-top: 0px;
    opacity: 0.85;
}

/* ---------- INPUT & BUTTON STYLING ---------- */
input[type="text"] {
    padding: 12px;
    border-radius: 12px;
    border: none;
    width: 300px;
    margin-bottom: 10px;
}

.stButton>button {
    background: linear-gradient(to right, #43a047, #1e88e5); /* green to blue */
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
}

/* ---------- WEATHER CARD ---------- */
.weather-card {
    background: rgba(255,255,255,0.2);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin: 15px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
}
.weather-big {
    font-size: 36px;
    font-weight: bold;
}
.weather-small {
    font-size: 18px;
}

/* ---------- 7-DAY FORECAST CARDS ---------- */
.forecast-card {
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin: 10px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


# ---------- TITLE ----------
st.markdown("<div class='title'>🌍 Weather Forecast App</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by Visual Crossing</div>", unsafe_allow_html=True)

# ---------- FUNCTION TO FETCH DATA ----------
def fetch_weather_data(location, api_key):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    url = f"{base_url}{location}?unitGroup=metric&contentType=json&key={api_key}"

    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError:
        st.error("❌ City not found or API error")
    except urllib.error.URLError:
        st.error("❌ Network problem. Check internet connection")
    return None

# ---------- INPUT ----------
API_KEY = "7DL4GRAAG8GXPTQSU5SPEK868"
city = st.text_input("", placeholder="Enter city, e.g., Mumbai, London, Pune")

# ---------- BUTTON ----------
if st.button("🔍 Get Weather"):
    if city.strip() == "":
        st.warning("⚠️ Please enter a city name")
    else:
        data = fetch_weather_data(city, API_KEY)

        if data:
            current = data["currentConditions"]

            st.markdown("---")

            # ---------- CURRENT WEATHER CARD ----------
            st.markdown(f"""
            <div class="weather-card">
                <div class="weather-big">🌡️ {current['temp']} °C</div>
                <div class="weather-small">📍 {data['resolvedAddress']}</div>
                <div class="weather-small">🌥️ {current['conditions']}</div>
                <div class="weather-small">💧 Humidity: {current['humidity']} % | 💨 Wind: {current['windspeed']} km/h | 🌡️ Feels like: {current['feelslike']} °C</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # ---------- 7-DAY FORECAST ----------
            st.subheader("📆 7-Day Forecast")
            forecast_cols = st.columns(7)

            for i, day in enumerate(data["days"][:7]):
                forecast_cols[i].markdown(f"""
                <div class="forecast-card">
                    <div class="weather-big">{day['datetime']}</div>
                    <div class="weather-small">🌡️ {day['temp']} °C</div>
                    <div class="weather-small">🌥️ {day['conditions']}</div>
                    <div class="weather-small">💧 {day['humidity']} %</div>
                </div>
                """, unsafe_allow_html=True)



