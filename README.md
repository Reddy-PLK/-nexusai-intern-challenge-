# NexusAI Intern Challenge

## Overview
This project is a simple AI-powered customer support system built as part of the NexusAI Intern Challenge.

It processes customer messages, generates responses, stores them in a database, and exposes an API.

---

## Features

### Task 1 – Message Handler
- Asynchronous message processing
- Rule-based AI response system (mocked, no external API)
- Error handling for empty input
- Channel-based response formatting

### Task 2 – Database Integration
- SQLite database used
- Stores:
  - Customer ID
  - Message
  - Response
  - Timestamp

### Task 3 – API (FastAPI)
- REST API built using FastAPI
- Endpoint: `/message`
- Accepts POST requests
- Returns structured JSON response

---

## Tech Stack

- Python
- FastAPI
- SQLite
- Asyncio

---

## Project Structure
