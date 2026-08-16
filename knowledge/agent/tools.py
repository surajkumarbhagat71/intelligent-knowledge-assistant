from ..rag import ask_rag
from accounts.models import Employee, LeaveBalance


def search_knowledge_base(question):
    """
    Search company documents using the existing RAG system.
    """

    result = ask_rag(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
    }
    



def get_employee_leave(employee_name):
    """
    Employee ke leave balance ki information database se return karta hai.
    """

    employee = Employee.objects.filter(name__iexact=employee_name).first()

    if not employee:
        return {
            "found": False,
            "message": f"Employee '{employee_name}' was not found."
        }

    leave_balance = getattr(employee, "leave_balance", None)

    if not leave_balance:
        return {
            "found": False,
            "message": f"Leave balance not found for {employee.name}."
        }

    return {
        "found": True,
        "employee_code": employee.employee_code,
        "employee_name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "year": leave_balance.year,
        "total_leaves": leave_balance.total_leaves,
        "used_leaves": leave_balance.used_leaves,
        "remaining_leaves": leave_balance.remaining_leaves,
    }
    
    


from urllib.parse import quote
from urllib.request import urlopen
from xml.etree import ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime
from zoneinfo import ZoneInfo


def get_today_news(query: str = "latest news"):
    """
    Fetch latest 10 news articles from Google News.
    """

    # Google News RSS URL
    search_query = f"{query} when:1d"

    url = (
        "https://news.google.com/rss/search?"
        f"q={quote(search_query)}"
        "&hl=en-IN"
        "&gl=IN"
        "&ceid=IN:en"
    )

    try:
        response = urlopen(url, timeout=10)
        xml_data = response.read()

        root = ET.fromstring(xml_data)

        today = datetime.now(ZoneInfo("Asia/Kolkata")).date()

        news = []

        for item in root.findall(".//item"):

            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pub_date = item.findtext("pubDate", "")
            source = item.findtext("source", "")

            # Check publication date
            try:
                published_datetime = parsedate_to_datetime(pub_date)
                published_datetime = published_datetime.astimezone(
                    ZoneInfo("Asia/Kolkata")
                )

                # Only today's news
                if published_datetime.date() != today:
                    continue

            except Exception:
                pass

            news.append(
                {
                    "title": title,
                    "source": source,
                    "published": pub_date,
                    "url": link,
                }
            )

            # Only 10 news
            if len(news) == 10:
                break

        return {
            "query": query,
            "count": len(news),
            "news": news,
        }

    except Exception as e:

        return {
            "query": query,
            "count": 0,
            "news": [],
            "error": str(e),
        }
        
        


import requests


def get_weather(city: str):
    """
    Get current weather for a city using Open-Meteo.
    No API key required.
    """

    if not city:
        return {
            "error": "Please provide a city name."
        }

    try:
        # 1. City -> Latitude/Longitude
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "error": f"City '{city}' not found."
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # 2. Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        return {
            "city": location["name"],
            "country": location.get("country"),
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Weather service error: {str(e)}"
        }

    except Exception as e:
        return {
            "error": str(e)
        }
        
       
        
from ddgs import DDGS


def web_search(query: str):
    """
    Search the web using DuckDuckGo.
    No API key required.
    """

    if not query:
        return {
            "error": "Please provide a search query."
        }

    try:
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=5
            )

            for result in search_results:
                results.append({
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "content": result.get("body"),
                })

        return {
            "query": query,
            "count": len(results),
            "results": results,
        }

    except Exception as e:
        return {
            "error": f"Web search failed: {str(e)}"
        }