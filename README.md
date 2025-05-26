# Property Analyzer

**Property Analyzer is an effortless tool to get property data from Zillow or OneHome without having to manually scan the listing yourself.**

## Why did I make this?
- Back in 2020 or so I got really into real estate investing. I made a Google Drive folder with real estate analyzers to calculate cash-on-cash
returns, compound annual growth rates, operating income, estimated monthly costs, projected property appreciation, ARV with comparable properties and
timelines for mortgage amortization; wrote a step-by-step guide to closing a real estate deal; created spreadsheets for prospective properties and 
mortgage/agent cold-call tracking. The works. I wanted to househack and purchase a multi-family home as quick as I could
- I recently got back into it because I want to buy a single family home for my parents so they can retire in their early-mid 60s.
- Before this project, my deal flow looked like this:
    1. Find an affordable property on Zillow or OneHome that my family and I liked
    2. Duplicate my main analyzer worksheet and copy the property's data into it (each prospective property had it's own giant analyzer sheet).
    3. The analyzer would do some magic (computes a bunch of numbers like the above^), and we'd have a rough idea of affortability and long-term prospect.
    4. *Then* I'd have to go and copy the numbers from the analyzer sheet into the prospective property sheet - this housed a quick table for my family
to compare properties with one another so we wouldn't have to look at analyzers all day. We can sort by sqft, sticker price, estimated monthly cost, etc.
- This was repetitive and took a lot of time. It needed to be automated...

## What does it do?
1. Running main.py, it'll prompt the user for a Zillow or OneHome property URL
2. Scrapes the listing for property data with BeautifulSoup and Selenium
3. Creates a duplicate of my main analyzer sheet, filling in the property data it gathered and stores it in a centralized Analyzer folder
4. Adds a row to the prospective properties sheet with the data that the analyzer calculated

## How this helps me
- My deal flow is now like this
    1. Find an affordable property on Zillow or OneHome that my family and I liked
    2. Paste the link into my tool
    3. ???
    4. Profit
- So, down from 4 steps with a bunch of mini-steps to basically just pasting a link into the CLI
- This has already saved my family countless hours. We have ~30 properties in our prospect list and the sheet links out to all the analyzer
sheets it's duplicated, so it's really easy for us to keep track of each property and project monthly costs/appreciation/etc.

## Future goals
- I expect to continue to use this tool in the foreseeable future, especially when I get back into the mutli-family/commercial side of things.

## Enhancement Ideas
- I have a list of enhancement ideas I'll track in enhancements.txt
