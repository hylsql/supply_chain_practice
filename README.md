# Supply Chain Analytics & Automation Project

An end-to-end Supply Chain Analytics and Automation project built using Python, PostgreSQL, SQL, pandas, and Power BI.

This project simulates real-world supply chain, operations, and business intelligence workflows commonly used by:
- Supply Chain Analysts
- Operations Analysts
- Inventory Analysts
- Business Analysts
- Data Analysts

The project includes:
- SQL and Python ETL workflows
- Automated KPI reporting
- Operations automation
- Freight audit automation
- Inventory alerts
- AI-generated business summaries
- Interactive Power BI dashboards

---

# Project Objectives

- Build job-ready supply chain analytics skills
- Practice real-world SQL and Python workflows
- Automate operational reporting
- Develop business intelligence dashboards
- Create a portfolio-ready analytics project

---

# Technologies Used

- Python
- PostgreSQL
- SQL
- pandas
- SQLAlchemy
- Power BI
- dotenv
- smtplib

---

# Skills Covered

## SQL
- Data cleaning and validation
- Joins and aggregations
- Window functions
- Common Table Expressions (CTEs)
- KPI calculations
- Exception reporting

## Python
- ETL automation
- PostgreSQL integration
- CSV automation
- Automated reporting
- KPI calculations
- Email automation
- AI-style summary generation

## Supply Chain Analytics
- Inventory Turnover
- Days on Hand
- Fill Rate
- Lead Time
- Freight % of Revenue
- ABC Analysis
- Stockout Rate
- Supplier Performance
- Freight Audit Analysis
- Inventory Reorder Automation

## Business Intelligence
- Interactive dashboards
- KPI visualization
- Operational analytics
- Executive reporting
- Dashboard automation
- Exception monitoring

---

# Project Architecture

```text
PostgreSQL
↓
Python ETL & Automation
↓
Cleaned Business Datasets
↓
KPI Reporting Layer
↓
Power BI Dashboards
↓
Automated Operational Reporting
```

---

# Dataset Overview

The project uses realistic supply chain datasets with intentionally messy operational data including:
- missing values
- inconsistent text formatting
- duplicate records
- freight anomalies
- inventory inconsistencies
- supplier performance issues

| Dataset | Description |
|---|---|
| customer_orders | Sales order data |
| order_items | Line-item sales transactions |
| products | Product master and cost data |
| inventory | Warehouse inventory balances |
| suppliers | Supplier information |
| purchase_orders | Purchase order transactions |
| shipments | Freight and delivery data |

---

# Business Datasets

## Sales Dataset

Joined Tables:
- customer_orders
- order_items
- products

Created Metrics:
- Revenue
- Gross Profit
- Total Cost

---

## Inventory Dataset

Joined Tables:
- inventory
- products

Created Metrics:
- Inventory Value
- Reorder Point
- Stockout Risk

---

## Purchase Order Dataset

Joined Tables:
- purchase_orders
- suppliers
- products

Created Metrics:
- Lead Time
- Fill Rate
- Supplier Performance

---

## Shipment Dataset

Joined Tables:
- shipments
- customer_orders

Created Metrics:
- Delivery Delay
- Freight Cost
- On-Time Delivery Flag

---

# Phase 1 — KPI & Reporting Automation

## KPI Report Automation

Automated KPI reporting pipeline that calculates and exports:

- Revenue
- Gross Profit
- Inventory Turnover
- Days on Hand
- Fill Rate
- Lead Time
- Freight % of Revenue
- Stockout Rate
- On-Time Delivery Rate

### Output Files

```text
kpi_summary.csv
abc_analysis.csv
supplier_performance.csv
```

---

## CSV Cleaning Automation

Automated ETL pipeline that:
- connects to PostgreSQL
- reads operational tables
- cleans and standardizes data
- validates operational records
- exports cleaned datasets

---

## Email Summary Automation

Automated reporting workflow that:
- generates KPI summaries
- attaches CSV reports
- sends automated email updates

---

# Phase 2 — Operations Automation

## Inventory Alerts

Automated inventory monitoring system that identifies:
- stockout risk
- low inventory levels
- reorder point alerts

### Business Logic

```text
Reorder Point =
Average Daily Sales × Lead Time
```

---

## Freight Audit Automation

Automated freight exception reporting that detects:
- freight cost outliers
- potential overbilling
- high-cost shipments

### Output

```text
freight_audit_exceptions.csv
```

---

## Reconciliation Automation

Automated reconciliation workflow that identifies:
- orders without shipments
- missing operational records
- revenue/shipment mismatches

### Output

```text
reconciliation_exceptions.csv
```

---

# Phase 3 — Analyst Automation

## SQL Auto Reporting

Automated SQL reporting workflows generate:
- top product reports
- supplier reports
- inventory valuation reports
- operational summaries

---

## Dashboard Refresh Workflows

Centralized automation workflow:
- refreshes datasets
- regenerates KPI reports
- updates dashboard-ready outputs

## Workflow Scheduling Automation

Windows Task Scheduler was used to automate the end-to-end reporting and analytics workflow.

### Automated Workflow

```text
Windows Task Scheduler
↓
run_supply_chain_automation.bat
↓
run_all_automations.py
↓
Data Cleaning ETL
↓
KPI Report Generation
↓
Operations Automation
↓
SQL Auto Reporting
↓
AI Summary Generation
↓
Power BI Dataset Refresh
```

### Scheduling Features

- Daily automated execution
- Centralized orchestration workflow
- Automated logging
- Dashboard-ready dataset refresh
- End-to-end analytics automation

### Batch Automation Script

```text
run_supply_chain_automation.bat
```

Example workflow:

```bat
@echo off
cd /d "YOUR_PROJECT_PATH"

"..\.venv\Scripts\python.exe" "run_all_automations.py" >> logs\automation_log.txt 2>&1
```

### Logging

Automation logs are stored in:

```text
logs/automation_log.txt
```

The logging workflow helps monitor:
- ETL execution
- automation failures
- reporting refresh status
- operational exceptions
```

---

## AI Summaries

Automated AI-style operational summaries generated from KPI and exception outputs.

### Example Insights

```text
SKUs projected to stock out within supplier lead time
Warehouses carrying excess inventory
Suppliers with declining fill rates
Freight cost outliers and routing risks
Root-cause analysis for fill rate declines
```

---

# Inventory Forecasting & Predictive Analytics

The project includes predictive inventory forecasting workflows built using Python and pandas to simulate real-world supply chain planning and replenishment analysis.

## Inventory Forecasting

Automated forecasting workflows estimate future inventory depletion based on:
- current inventory levels
- historical sales velocity
- supplier lead times

### Forecast Metrics

- Average Daily Sales
- Days Until Stockout
- Projected Stockout Date
- Recommended Reorder Quantity
- Stockout Within Lead Time Flag

### Forecast Outputs

```text
inventory_forecast.csv
stockout_forecast.csv
```

---

## Stockout Forecasting

The stockout forecasting workflow identifies SKUs projected to stock out before suppliers can replenish inventory.

### Forecast Logic

```text
Days Until Stockout =
Quantity On Hand ÷ Average Daily Sales
```

```text
Stockout Risk =
Days Until Stockout < Supplier Lead Time
```

### Example Forecast Insights

```text
SKU-0045 projected to stock out in 6 days
Supplier lead time is 14 days
Recommended replenishment action required
```

---

## Predictive Analytics Features

- Inventory depletion forecasting
- Reorder planning
- Stockout risk prediction
- Supplier lead time risk analysis
- Warehouse inventory risk monitoring
- Inventory coverage analysis

---

## Power BI Forecast Dashboards

Forecast outputs are integrated into Power BI dashboards for:
- projected stockout tracking
- inventory coverage analysis
- replenishment planning
- warehouse inventory monitoring
- operational risk management

---
# Power BI Dashboards

The project includes interactive Power BI dashboards built from automated CSV outputs.

## Executive Dashboard
- Revenue KPIs
- Inventory Turnover
- Fill Rate
- Freight % of Revenue
- Revenue Trends

## Inventory Dashboard
- Inventory by Warehouse
- Stockout Risk
- Reorder Alerts
- ABC Analysis

## Supplier Dashboard
- Supplier Fill Rate
- Lead Time Analysis
- Supplier Ranking
- Low Performance Suppliers

## Freight Dashboard
- Freight Spend by Carrier
- Freight Outliers
- Late Shipments
- Delivery Performance

---

# Example KPIs

| KPI | Description |
|---|---|
| Inventory Turnover | Measures inventory efficiency |
| Days on Hand | Inventory coverage estimate |
| Fill Rate | Supplier fulfillment performance |
| Lead Time | Supplier delivery speed |
| Freight % of Revenue | Logistics cost efficiency |
| Stockout Rate | Inventory availability risk |
| On-Time Delivery Rate | Shipment performance |

---

# Output Files

```text
sales_dataset.csv
inventory_dataset.csv
purchase_order_dataset.csv
shipment_dataset.csv
kpi_summary.csv
abc_analysis.csv
supplier_performance.csv
inventory_alerts.csv
inventory_forecast.csv
stockout_forecast.csv
freight_audit_exceptions.csv
reconciliation_exceptions.csv
ai_summary.txt
```

---

# How to Run

## 1. Run Data Cleaning

```bash
python data_cleaning.py
```

## 2. Run KPI Dashboard

```bash
python kpi_dashboard.py
```

## 3. Run Operations Automation

```bash
python operations_automation.py
```

## 4. Run SQL Auto Reporting

```bash
python sql_auto_reporting.py
```

## 5. Run AI Summary

```bash
python ai_summary.py
```

## 6. Run Full Automation Workflow

```bash
python run_all_automations.py
```

---

# Power BI Workflow

```text
Python Automation
↓
Export CSV Outputs
↓
Power BI Refresh
↓
Updated Dashboards
```

---

# Future Enhancements

Planned future improvements:
- Power BI Service scheduled refresh
- Cloud deployment
- Forecasting models
- Demand planning automation
- AI-powered anomaly detection
- Real-time dashboard refresh
- API integrations

---

# Key Skills Demonstrated

## Data Engineering
- ETL pipelines
- Data cleaning workflows
- PostgreSQL integration
- Data validation

## Supply Chain Analytics
- Inventory analysis
- Freight analysis
- Supplier performance
- Operational KPI reporting
- Inventory forecasting
- Stockout forecasting
- Predictive replenishment analysis
- Demand-driven inventory planning

## Automation
- Automated reporting
- Inventory alerts
- Freight auditing
- Reconciliation workflows
- Email automation

## Business Intelligence
- KPI development
- Interactive dashboards
- Executive reporting
- Operational analytics
- Predictive analytics dashboards
- Forecast visualization

---

# Author

Built as a portfolio project focused on:
- Supply Chain Analytics
- Operations Automation
- Business Intelligence
- Python Automation
- SQL Reporting
- Power BI Analytics
