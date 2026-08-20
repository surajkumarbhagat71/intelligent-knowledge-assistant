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
        
    

def get_contact_number(name: str):
    """
    Find a contact's mobile number by name.
    """
    
    CONTACTS = {
        "Rahul Kumar": "9876543210",
        "Amit Sharma": "9123456780",
        "Priya Singh": "9988776655",
        "Rohan Verma": "9012345678",
        "Neha Gupta": "9234567890",
        "Ankit Kumar": "9345678901",
        "Pooja Sharma": "9456789012",
        "Raj Singh": "9567890123",
        "Sneha Kumari": "9678901234",
        "Aman Yadav": "9789012345",
        "Rohit Kumar": "9890123456",
        "Anjali Singh": "9901234567",
        "Vikas Sharma": "9812345678",
        "Simran Gupta": "9723456789",
        "Nikhil Verma": "9634567890",
        "Kavya Kumari": "9545678901",
        "Abhishek Singh": "9456789012",
        "Riya Sharma": "9367890123",
        "Manish Kumar": "9278901234",
        "Sakshi Gupta": "9189012345",
        "Simran": "9827325191",
    }

    number = CONTACTS.get(name)

    if not number:
        return {
            "found": False,
            "message": f"No contact found for {name}"
        }

    return {
        "found": True,
        "name": name,
        "mobile": number,
    }
    
    

from urllib.parse import quote

def open_whatsapp(name: str, mobile: str):
    """
    Open WhatsApp Web for the given contact.
    """

    if not name:
        return {
            "success": False,
            "message": "Name is required."
        }

    if not mobile:
        return {
            "success": False,
            "message": "Mobile number is required."
        }

    # Remove spaces, +, -, etc.
    mobile = "".join(filter(str.isdigit, mobile))

    # Add India country code if 10-digit number
    if len(mobile) == 10:
        whatsapp_number = f"91{mobile}"
    else:
        whatsapp_number = mobile

    whatsapp_url = (
        f"https://web.whatsapp.com/send?phone={whatsapp_number}"
    )

    return {
        "success": True,
        "name": name,
        "mobile": mobile,
        "whatsapp_url": whatsapp_url,
        "message": f"WhatsApp opened for {name}."
    }
    
    
from langchain_openai import ChatOpenAI
from django.conf import settings


def ask_llm(question: str):
    """
    Ask the LLM directly for a general question.
    Use this when no specific tool is required.
    """

    if not question:
        return {
            "success": False,
            "message": "Please provide a question."
        }

    llm = ChatOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=settings.NVIDIA_API_KEY,
        model="openai/gpt-oss-20b",
        temperature=0.2,
    )

    response = llm.invoke(question)

    return {
        "success": True,
        "question": question,
        "answer": response.content,
    }