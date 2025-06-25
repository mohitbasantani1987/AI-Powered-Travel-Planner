# AI-Powered Travel Planner

AI-Powered Travel Planner is an intelligent travel agent and expense planner that helps you plan trips to any city worldwide using real-time data. Instantly receive a comprehensive, actionable, and beautifully formatted Markdown travel plan tailored to your preferences, budget, and travel dates.

## ✨ Features

### Day-by-Day Itinerary
- Detailed breakdown of your trip by day.
- Morning, afternoon, and evening activities.
- Custom recommendations based on your city, duration, and interests.

### Attractions & Activities
- Lists of must-see landmarks, museums, events, and nature spots.
- Includes descriptions, timings, entry fees, and helpful tips.

### Food & Dining Recommendations
- 2–3 restaurant or food place suggestions per day.
- Cuisine type, average pricing, and location.
- Focus on local, authentic, and budget-friendly options.

### Cost Estimation
- Line-by-line breakdown of expected expenses.
- Categories: accommodation, food, transportation, attractions, and extras.
- Clear daily and total budget estimates.

### Transport Guidance
- Recommended transport modes (metro, taxi, walk, etc.) between places.
- Estimated durations and costs.
- Airport transfer info if relevant.

### Weather Forecast
- Real-time weather summary for each day.
- Temperature, rain chance, and advisories.

### Packing & Clothing Tips
- Personalized advice on what to wear and pack based on the weather forecast (e.g., shoes, umbrella, jackets).

## 🖥️ How It Works

1. **Input Your Trip Details:**  
   Enter your destination, dates, budget, interests, and any special preferences.

2. **Get Your Plan:**  
   Instantly receive a complete, ready-to-use travel plan in Markdown format.

3. **Review & Go:**  
   Use the plan as your travel guide—no waiting, no incomplete answers.

## 📋 Example Request

> Hi, I want to take a 5-day trip to Venice next month (08 August 2025 to 13 August 2025). My hotel budget is around $100 per night. I’d like to know what the weather will be like, what places I can visit, and how much the whole trip might cost. I’ll be paying in Japanese Yen, but my native currency is USD. Also, I prefer local food and public transportation. Can you plan it all for me?

## 🛠️ Tech Stack

- Python
- Streamlit (for interactive UI)
- LangChain (for LLM orchestration)
- Real-time APIs (weather, maps, pricing, etc.)

## 🚀 Getting Started

Clone the repository:
```
git clone https://github.com/yourusername/AI-Powered-Travel-Planner.git
cd AI-Powered-Travel-Planner
```

Install dependencies:
```
pip install -r requirements.txt
```

Configure your API keys in config.py.

Run the app:
```
streamlit run main.py
```

### 📑 Response Format
- Markdown for clarity and readability.
- Bullet points, numbered lists, and tables where helpful.
- **Bold headings** for each day/section (e.g., **Day 1: Arrival & Exploration**).
- Friendly, knowledgeable, and professional tone.

### 📝 Notes
- All calculations (budgets, distances, durations) use real-time data when available.
- If real-time data is unavailable, the app will clearly state this and suggest the best alternatives.
- Never delays or partial answers—always a complete plan.

### 💡 Pro Tips
- At the end of each plan, you’ll get advice on what clothes and shoes to pack, and whether to bring an umbrella or other essentials based on the weather.

### 📄 License
MIT License