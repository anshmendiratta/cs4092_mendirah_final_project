# Requirements

## Overview
- Author: Ansh Mendiratta
- Type: Ecommerce platform.
- Intended Users: Customers, staff.

Security has not been enforced here. The system assumes that each user is who they claim to be and that they only perform operations they are supposed to be permitted.

## Kinds of Users
- Customer (it is atypical giving them direct access to the DB, but we assume a benevolent user and do not sanitize queries.)
- Staff 

## Business Rules
- Each customer is uniquely identified by a Customer ID.
- Each staff member is uniquely identified by a Staff ID.
- Each product is managed by one staff member.
- A customer may own multiple credit cards.
- A purchase belongs to exactly one customer.
- A purchase uses exactly one credit card.
- A purchase may contain one or more products.
- A product may appear in multiple purchases.
- Product prices and inventory quantities cannot be negative.

## Functions
- Store customer account information.
- Allow customers to save multiple credit cards.
- Store information about products, including prices and inventory.
- Allow staff members to add and update products.
- Record purchases made by customers.
- Allow each purchase to contain multiple products.
- Record the quantity and purchase price of each product in a purchase.

## Data Required
- **Customer:** CustomerID; First name; Last name; Email address; Phone number.
- **Staff:** StaffID; First name; Last name; Job position.
- **Credit Card:** Card ID; CustomerID; Card number; Expiration month; Expiration year; Cardholder name.
- **Product:** ProductID; Product name; Description; Price; Stock quantity; the Staff responsible for managing the product.
- **Purchase:** PurchaseID; CustomerID; Payment method used; Purchase date.
- **Purchase Item:** PurchaseID; ProductID; Quantity purchased; Purchase price.

NOTE: credit cards do not *need* an associated `CardholderName`, but busineses may find this useful to have.
NOTE: `Purchase` and `PurchaseItem` are separated to avoid multi-valued attributes. `Purchase` primarily keeps track of a `PurchaseID` which may be referenced several times in `PurchaseItem`, each time with a different product ID, to record a single rder.

## Use Cases

### Use Case 1: Purchase Products
1. Customer browses available products.
2. Customer selects one or more products.
3. Customer selects a saved credit card.
4. DB records the purchase and associated products.

### Use Case 2: Add a New Product
1. Staff member enters product information.
2. DB stores product information and initial inventory.
3. Product becomes available for purchase.

### Use Case 3: Update Inventory
1. Staff member selects a product.
2. Staff member updates the stock quantity.
3. DB saves the updated inventory.

### Use Case 4: View Purchase History
1. Customer requests purchase history.
2. DB retrieves customer purchases.
3. DB displays purchased products and quantities.

