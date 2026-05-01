# Tokopedia Product Scraper (Playwright)

## Overview

A Python scraper that extracts product data from Tokopedia search results using Playwright.

Instead of parsing HTML, it intercepts internal GraphQL responses to obtain structured and stable data.

## Features

* Extracts up to 60 products per run
* Fields:

  * Product name
  * Price
  * Rating
  * Sold info
  * Shop name
  * Location
  * Product URL
* Exports data to Excel

## Tech Stack

* Python
* Playwright
* OpenPyXL

## How It Works

The scraper listens to network responses and captures product data directly from Tokopedia’s GraphQL API responses.

## Output

Excel file with clean, structured data ready for analysis.

## Use Cases

* Market research
* Competitor analysis
* Price monitoring
* E-commerce insights
