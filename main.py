from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState, StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Markdown
import streamlit as st
from config import Config
from toolsSetUp import ToolsSetup

class TravelPlanner:
    def __init__(self, toolsSetUp: ToolsSetup):
        self.toolsSetUp = toolsSetUp
        self.tools = toolsSetUp
        self.system_prompt = SystemMessage(
            content="""You are an expert AI Travel Agent and Expense Planner, assisting users in planning trips to any city worldwide using real-time data. Your goal is to deliver comprehensive, accurate, and immediately actionable travel plans in a single, well-structured Markdown-formatted response.

            Your Responsibilities:
            Always respond with a complete, ready-to-use travel plan. Never delay or say “I’ll prepare that” or “Hold on.” Your responses must always include:
            1. Day-by-Day Itinerary
              - Clearly break down the trip by day.
              - Include morning, afternoon, and evening activities.
              - Tailor recommendations to the city, travel duration, and traveler preferences (if provided).

            2. Attractions & Activities
              - List specific landmarks, museums, events, or nature spots.
              - Include brief descriptions, timings, entry fees (if applicable), and tips.
            
            3. Food & Dining Recommendations
              - Suggest 2–3 restaurants or food places per day.
              - Include cuisine type, average pricing, and location.
              - Prioritize local, authentic, and budget-conscious options unless told otherwise.
              
            4. Cost Estimation
               - Provide a line-by-line breakdown of expected expenses.
               - Categories: accommodation, food, transportation, attractions, and extras.
               - Clearly state total estimated budget per day and overall.

            5. Transport Guidance
              - Include transport modes between places (e.g., metro, taxi, walk).
              - Share estimated durations and costs.
              - If airport transfers are relevant, include them.

            6. Weather Forecast
              - Show the weather summary for each day using real-time data.
              - Include temperature, rain chance, and any advisories.

              Response Format:
              - Use Markdown formatting for clarity.
              - Use bullet points, numbered lists, and tables where helpful.
              - Bold headings for each day or section (e.g., Day 1: Arrival & Exploration).
              - Keep the tone friendly, knowledgeable, and professional.

              Data Use & Tool Behavior:
              - Use all available tools to pull real-time weather, location, transport, and pricing data.
              - Ensure calculations (budgets, distances, durations) are accurate.
              - Never guess—if real-time data isn't available, clearly state it and suggest best alternatives.

              TIP: In the end provide a tip to the user about clothes to wear based on the weather forecast.Which type of shoes to wear, if the climate is rainy carry an umbrella, etc.   
            """
        )

    def call_model(self, state: MessagesState):
        question = state["messages"]    
        question_with_system_prompt = [self.system_prompt] + question   
        response = self.tools.llm_with_tools.invoke(question_with_system_prompt)
        
        return {
            "messages": [response]
        }    

    def createWorkflow(self):
        builder = StateGraph(MessagesState) 
        builder.add_node("llm_decision_step", self.call_model)
        builder.add_node("tools", ToolNode(self.toolsSetUp.tools))

        builder.add_edge(START, "llm_decision_step")
        builder.add_conditional_edges(
            "llm_decision_step",
            ## if last messages is tools call then call the tools
            ## if last messages is not tools call return end
            tools_condition
        )
        builder.add_edge("tools", "llm_decision_step")

        app = builder.compile()
        return app


if __name__ == "__main__":
    config = Config()
    tools_setup = ToolsSetup(config)

    travel_planner = TravelPlanner(tools_setup)
    graph = travel_planner.createWorkflow()

    limit = {"recursion_limit": 12}

    st.set_page_config(page_title="AI-Powered Travel Planner", layout="wide")
    st.title("✈️ AI-Powered Travel Planner")
    user_input = st.text_area(
    "Excited!! about your next trip plan. Go Ahead and tell me about your trip (e.g., destination, dates, budget, interests, travelers):", 
    height=200,
    value=f"Hi, I want to take a 5-day trip to Venice next month 08 August 2025 to 13 August 2025. My hotel budget is around $100 per night. I’d like to know what the weather will be like, what places I can visit, and how much the whole trip might cost. I’ll be paying in Japanese Yen, but my native currency is USD. Also, I prefer local food and public transportation. Can you plan it all for me?."
    )

    
    if st.button("Generate Trip Plan",type="primary",icon="🔍",use_container_width=True):
        with st.spinner("Please hold on while I prepare your trip plan..."):
            messages = [user_input.strip()]
            try:
                response = graph.invoke({"messages": messages}, config=limit)
                for m in response["messages"]:
                    m.pretty_print()    
                #print(result.ai_message.content)
                # Final check - if still incomplete, force a summary
                if len(response) < 700:
                    summary_prompt = f"""
                    Based on all the information gathered, provide a COMPLETE travel summary now. 
                    Don't use tools anymore. Use the information you have to create a comprehensive plan.
                    Format your response in clean Markdown with proper headers, lists, and formatting.
                    Original request: {user_input}
                    """
                    
                    summary_messages = response["messages"] + [summary_prompt]
                    final_response = travel_planner.tools.llm_with_tools.invoke(summary_messages)
                    # Safely extract content from final_response
                    if isinstance(final_response, dict) and "content" in final_response:
                        print(Markdown(final_response["content"]))
                        st.subheader("Your Complete Trip Plan:")
                        st.markdown(final_response["content"]) # Render markdown output
                        st.success("Trip plan generated successfully!")
                    elif hasattr(final_response, "content"):
                        #print(Markdown(final_response.content))
                        st.subheader("Your Complete Trip Plan:")
                        st.markdown(final_response.content) # Render markdown output
                        st.success("Trip plan generated successfully!")
                    else:
                        #print(Markdown(str(final_response)))
                        st.subheader("Your Complete Trip Plan:")
                        st.markdown(final_response['messages'][-1].content) # Render markdown output
                        st.success("Trip plan generated successfully!")
                else:
                    st.subheader("Your Complete Trip Plan:")
                    st.markdown(response['messages'][-1].content) # Render markdown output
                    st.success("Trip plan generated successfully!")
                
            except Exception as e:
                print(f"Workflow error: {e}")
                Markdown(f"An error occurred: {e}. Please try again or check your input.")  