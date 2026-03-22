# E-Commerce System
## 1. Summary
This project is used for demonstration purposes, as part of the interviewing process for eBag.
The project requires creation of a service, that will be used for E-Commerce system.
The core functionality will be to manage operations on products in this system.
## 2. Requirements
// ADD Requirements here
## 3. Setup
The project is uses FastAPI and Tortois ORM, and, for the initial version - uses SQLite as DB.
It is also made on Python v3.14.
The commands, needed to run it, are as follows:
- Install requirements
```bash
pip install -r requirements.txt
```
- Run the initial migrations
```bash
tortoise --config-file confs/db.json migrate 
```
- In case of model changes - update the migrations
```bash
tortoise --config-file confs/db.json makemigrations 
```
- Run the actual service (the setup also utilizes uvicorn)
```bash
uvicorn run:app --host 0.0.0.0 --port 8090
```
- Once all of this is setup - the API is exposed on localhost:8090
```bash
[GET | POST | UPDATE | DELETE] http://localhost:8090/api/category
[GET | POST | UPDATE | DELETE] http://localhost:8090/api/product
```
