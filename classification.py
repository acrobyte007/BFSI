from langchain.tools import tool
import sqlite3
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field
import pandas as pd
import asyncio
import dotenv
dotenv.load_dotenv()
DB_NAME = "bfsi.db"



@tool
def get_taxonomy() -> str:
    """Fetch BFSI taxonomy (driver, sub-driver, description) from database"""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT driver, sub_driver, description FROM taxonomy")
    rows = cursor.fetchall()

    conn.close()

    taxonomy_text = "\n".join(
        f"Driver: {r[0]} | Sub-driver: {r[1]} | Description: {r[2]}"
        for r in rows
    )

    return taxonomy_text

llm = ChatMistralAI(
    model="ministral-8b-latest",
    temperature=0
)

class Output(BaseModel):
    driver: str = Field()
    sub_driver: str = Field()

agent = create_agent(
    llm,
    tools=[get_taxonomy],
    response_format=Output
)

async def classify(text):

    SYSTEM_PROMPT = """
You are a BFSI classification agent.

Use the get_taxonomy tool to understand classification categories.

Classify the text into:
- Driver
- Sub-driver

Rules:
- Choose only one driver and sub-driver
- Do not create new categories
"""

    result = await agent.ainvoke({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    })

    return result["structured_response"]



async def process_csv():

    df = pd.read_csv(r"E:\BFSI\BFSI\data\cleaned_data.csv")

    df["driver"] = ""
    df["sub_driver"] = ""

    for i, row in df.iterrows():
        text = row["processed_text"]
        if pd.isna(text):
            text = ""
        result = await classify(text)
        df.at[i, "driver"] = result.driver
        df.at[i, "sub_driver"] = result.sub_driver
        print(i)

    df.to_csv(r"E:\BFSI\BFSI\data\final_output.csv", index=False)


asyncio.run(process_csv())