SRH Inventory:

SRH Inventory is a very easy to use inventory management app developed by students at SRH University.  
It is maintained by Chris Glettenberg, Joseph, Rafi, Faisal and Leo.  
The program is coded using Python and runs on the Streamlit interface with additionally Streamlit plugins, namnely Panda and altair.  
Using Streamlit and these plugins we are able to easily visualize and edit transaction and inventory data for a small company.

Installation: 

Option 1: Run online in virtual simulator like github
1. Open virtual cloud based environment like github
2. Install dependencies:
   - !pip install streamlit pandas numpy altair
3. Save app as any name
4. Run app: streamlit run yourAppName.py
(Commands may be different depending on your environment/OS)

Option 2: Run Locally:
1. Clone the repository: git clone https://github.com/yourusername/srh-inventory.gitcd srh-inventory
2. Install dependencies: pip install -r requirements.txt
3. Save app as any name
4. Run application: streamlit run yourAppName.py
(Commands may be different depending on your environment/OS)

File Structure:
inventory.py/
│── Inventory.py 
│── requirements.txt
│── README.md 

Potential Future Changes:
We would love to eventually broaden our App to handle larger inventory amounts, potentially by added auto assignment to SKUS.
Also we would love to ntroduct a Mobile version by attempting to transition from streamlit to another platform (Flutter?)
Lasttly we think we have room to improve data visualization and download features of this app.
