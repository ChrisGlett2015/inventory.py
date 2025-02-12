import streamlit as st
import pandas as pd
import numpy as np
import csv
import os
import asyncio
import altair as alt

INVENTORY_FILE = "inventory.csv"
TRANSACTIONS_FILE = "transactions.csv"

class Item:
    def __init__(self, name, price, expense, SKU, quantity, category):
        self.name = name
        self.price = price
        self.expense = expense
        self.SKU = SKU
        self.quantity = quantity
        self.category = category

    def update_quantity(self, bought, sold):
        self.quantity += int(bought)
        if sold > self.quantity:
            return False 
        self.quantity -= int(sold)
        return True
    
    def stock_level(self):
        if self.quantity < 15:
            return "low"
        else:
            return "okay"

class Transaction:
    def __init__(self, name, bought, sold, price, expense):
        self.name = name
        self.bought = bought
        self.sold = sold
        self.price = price
        self.expense = expense

items = []

if "items" not in st.session_state:
    st.session_state["items"] = [
        Item("Milk", 2.00, 1.00, 10000001, 10, "Dairy"),
        Item("Yogurt", 3.00, 1.00, 10000002, 15, "Dairy"),
        Item("Cheese", 2.75, 1.25, 10000003, 20, "Dairy"),
        Item("Bread", 3.00, 0.75, 10000004, 30, "Bakery"),
        Item("Cake", 8.00, 2.50, 10000005, 5, "Bakery"),
        Item("Orange", 0.30, 0.10, 10000006, 50, "Produce"),
        Item("Apple", 0.50, 0.20, 10000007, 100, "Produce"),
        Item("Beef", 13.00, 7.00, 10000008, 10, "Meat"),
        Item("Chicken", 9.00, 4.00, 100000019, 20, "Meat"),
        Item("Broccoli", 0.75, 0.30, 10000010, 10, "Produce"),
    ]

st.title("SRH Inventory")
st.caption("Inventory made simple." ,unsafe_allow_html=False)

if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

if "Manage Products" not in st.session_state:
    st.session_state["Manage Products"] = False

if "Search" not in st.session_state:
    st.session_state["Search"] = False

if "New Item" not in st.session_state:
    st.session_state["New Item"] = False

if "Delete Item" not in st.session_state:
    st.session_state["Delete Item"] = False

if "Enter" not in st.session_state:
    st.session_state["Enter"] = False

if "Inventory" not in st.session_state:
    st.session_state["Inventory"] = False

if "Transactions" not in st.session_state:
    st.session_state["Transactions"] = False   

if "Reports" not in st.session_state:
    st.session_state["Reports"] = False            

if st.button("Inventory"):
    st.session_state["Inventory"] = not st.session_state["Inventory"]
    st.session_state["Manage Transactions"] = False
    st.session_state["Transactions"] = False  
    st.session_state["Reports"] = False

if st.session_state["Inventory"]:
    if st.session_state["Manage Products"] or st.session_state["Transactions"]:
        st.session_state["Manage Products"] = False
        st.session_state["Transactions"] = False   
    item_chart = [
    {
        "Name": item.name,
        "Price": item.price,
        "Expense": item.expense,
        "SKU": item.SKU,
        "Quantity": item.quantity,
        "Category": item.category,
        "Stock Level": item.stock_level()
        }
        for item in st.session_state["items"]
    ]
    df = pd.DataFrame(item_chart)

    st.table(pd.DataFrame(item_chart))
    cola, colb, colc, cold = st.columns(4)
    with cold:
        if st.button("Download Inventory"):
            df.to_csv('inventory.csv', index=False)

if st.button("Manage Products"):
    st.session_state["Manage Products"] = not st.session_state["Manage Products"]
    st.session_state["Inventory"] = False
    st.session_state["Transactions"] = False  
    st.session_state["Reports"] = False

if st.session_state["Manage Products"]:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Search"):
            st.session_state["Search"] = not st.session_state["Search"]
            st.session_state["New Item"] = False
            st.session_state["Delete Item"] = False
    with col2:
        if st.button("New Item"):
            st.session_state["New Item"] = not st.session_state["New Item"]
            st.session_state["Search"] = False
            st.session_state["Delete Item"] = False            
    with col3:
        if st.button("Delete Item"):
            st.session_state["Delete Item"] = not st.session_state["Delete Item"]
            st.session_state["New Item"] = False
            st.session_state["Search"] = False
if st.session_state["Manage Products"] and st.session_state["Search"]:
    search_key = st.text_input("Please Enter Product Name, SKU, or Category: ")
    for item in st.session_state["items"]:
        if search_key == item.name or search_key == item.SKU or search_key == item.category:
            item_chart = [       {
                "Name": item.name,
                "Price": item.price,
                "Expense": item.expense,
                "SKU": item.SKU,
                "Quantity": item.quantity,
                "Category": item.category,
            } ]
            st.table(pd.DataFrame(item_chart))

if st.session_state["Manage Products"] and st.session_state["New Item"]:
    st.write("Please enter the following information about your item: ")
    name_temp = st.text_input("Name: ")
    price_temp = st.number_input("Price:")
    expense_temp = st.number_input("Cost to produce: ")
    SKU_temp = st.number_input("SKU: ")
    quantity_temp = st.number_input("Number in stock: ")
    category_temp = st.text_input("Category: ")
    new_item = Item(name_temp, price_temp, expense_temp, SKU_temp, quantity_temp, category_temp)
    if st.button("Enter"):
        for item in st.session_state["items"]:
            if new_item.SKU == item.SKU:
                st.write("Item with SKU already exists!")
                exit()
        st.session_state["items"].append(new_item)
        st.session_state["New Item"] = not st.session_state["New Item"]
        st.write("Item successfully added!")


if st.session_state["Manage Products"] and st.session_state["Delete Item"]:
        search_key = st.text_input("Please Enter Product Name or SKU you would like to Delete: ")
        if st.button("Delete"):
            temp = None
            for item in st.session_state["items"]:
                if search_key == item.name or search_key == str(item.SKU) or search_key == item.category:
                    temp = item
                    break
            if temp:
                st.session_state["items"].remove(temp)
                st.write("Item successfully deleted!")
            else:
                st.write("Item does not exist!")

if st.button("Transactions"):
    st.session_state["Transactions"] = not st.session_state["Transactions"]
    st.session_state["Inventory"] = False
    st.session_state["Manage Products"] = False  
    st.session_state["Reports"] = False

if st.session_state["Transactions"]: 
    for idx, item in enumerate(st.session_state["items"]):
        col4, col5 = st.columns(2)
        with col4:
            bought = st.number_input(f"Bought ({item.name}):", key=f"bought_{idx}")
            sold = st.number_input(f"Sold ({item.name}):", key=f"sold_{idx}")
        with col5:
            new_price = st.number_input(f"New Price ({item.name}):", key=f"new_price_{idx}")
            new_expense = st.number_input(f"New Expense ({item.name}):", key=f"new_expense_{idx}")
        if st.button(f"Update", key=f"update_{idx}"):
            if new_price:
                item.price = new_price
            if new_expense:
                item.expense = new_expense
            if bought > 0 or sold > 0:
                success = item.update_quantity(bought, sold)
                if not success:
                    st.warning(f"Not enough stock for {item.name}! Transaction canceled.")
                    exit()
                temp_Transaction = Transaction(item.name, bought, sold, item.price, item.expense)
                st.session_state["transactions"].append(temp_Transaction)
            st.success(f"Updated")

if st.button("Reports"):
    st.session_state["Reports"] = not st.session_state["Reports"]
    st.session_state["Inventory"] = False
    st.session_state["Transactions"] = False 
    st.session_state["Manage Products"] = False

if st.session_state["Reports"]: 
    transaction_chart = [
        {
            "Name": transaction.name,
            "Sold": transaction.sold,
            "Bought": transaction.bought
        }
        for transaction in st.session_state["transactions"] 
    ]
    if transaction_chart:
        df = pd.DataFrame(transaction_chart)
        
        chart_data = df.melt(id_vars=["Name"], value_vars=["Sold", "Bought"], 
                        var_name="Type", value_name="Value")

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Name:N", title="Items"),
            y=alt.Y("Value:Q", title="Value"),
            color=alt.Color("Type:N", title="Type"),
            column=alt.Column("Type:N", title=None)
        ).properties(
        width=100,
        height=300
        )

        chart
    else:
        st.write("Transaction list is empty!")
        
    colw, colx, coly, colz = st.columns(4)
    with colz:
        if st.button("Download Transactions"):
            df.to_csv('transactions.csv', index=False)
