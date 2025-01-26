# Doctor Who: Pharmacy Management System

## Overview
Doctor Who is a pharmacy management system built using Python, Tkinter, and MySQL to streamline pharmacy operations. This project provides a user-friendly interface to manage customers, suppliers, medicine inventory, sales, and purchases efficiently.

## Features

### 1. Customer Management
- Add, update, view, and delete customer details like name and contact information.
- Automatically validates inputs to prevent duplicate or incomplete entries.
- Provides a dedicated interface for browsing and managing customer data.

### 2. Supplier Management
- Manage supplier details, including name, phone, email, and company information.
- Edit supplier details or remove suppliers no longer active.
- View supplier records in a structured table format for better tracking.

### 3. Medicine Inventory
- Add new medicines with details such as name, price, stock quantity, and unique codes.
- Update medicine details, including pricing and stock levels.
- Delete medicines that are discontinued.
- View a complete inventory with search and sorting functionality.

### 4. Cart and Sales Management
- Add medicines to a shopping cart with specified quantities.
- Automatically calculate total prices based on quantity and pricing.
- Save cart data to the database as sales records once the transaction is completed.
- Track all sales history for auditing purposes.

### 5. Purchase Management
- Record purchases from suppliers with details like medicine name, price, quantity, and supplier info.
- Automatically update inventory when new stock is purchased.
- Maintain a log of purchase records for future reference.

## Technology Stack
- **Language:** Python
- **GUI Framework:** Tkinter
- **Database:** MySQL (with MySQL Connector)
- **Other Tools:** PIL for image handling, Tkinter TTK for advanced widgets

## Instructions video for the app

[![Watch the video](https://img.youtube.com/vi/7QPH2KEjlN4/0.jpg)](https://www.youtube.com/watch?v=7QPH2KEjlN4&t=6s)

## Setup Instructions

### Prerequisites
- Install Python 3.x.
- Install MySQL and create a database named `pharmacy_system`.
- Install the required Python libraries using the following command:
  ```bash
  pip install mysql-connector-python pillow

## Database Structure

### Tables
- **customer**: Stores customer details (ID, name, phone).
- **seller**: Stores supplier information (ID, name, phone, email, company).
- **medicine**: Tracks medicine details (ID, name, price, stock quantity, code).
- **cart**: Temporary table for managing active sales.
- **sales**: Logs completed sales transactions.
- **purchase**: Logs medicine purchases from suppliers.

## Key Functionalities

### GUI
- Built with Tkinter, featuring multiple windows for different operations:
  - **Main Menu:** Navigate between customer, supplier, and medicine management.
  - **Customer/Supplier Windows:** Forms and table views for CRUD operations.
  - **Cart Window:** Add medicines, calculate totals, and save transactions.
  - **Sales and Purchase History:** View logs of completed transactions.

### Error Handling
- Handles exceptions for invalid inputs, missing data, and database errors gracefully.
- User feedback is provided through dialog boxes for success or failure notifications.

### Centralized Data Storage
- MySQL ensures all data is stored securely and supports multi-table relationships for optimized queries.
- Deletes are cascaded to prevent orphaned records (e.g., when removing a customer or medicine).

### Future Improvements 
- Implement reporting features to generate monthly sales and purchase summaries.
- Allow the update in quantity 
  
