#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/<Vicky-gqc>/<ECON-481>/blob/main/<assignment-6.py>"


# In[4]:


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

path = 'auctions.db'

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    def query(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return(df)

auctions = DataBase(path)


# In[5]:


#Exercise 1
def std() -> str:
    """
    SELECT itemid and std, whereby std is given by the formula in which we need to calculate the mean bidamount.
    FROM (subquery: in which we have itemid, bidamount, and mean aligned by itemid)
    align by itemid
    """
    q = '''
    SELECT 
        itemID,
        CASE 
            WHEN COUNT(bidAmount) > 1 THEN
                ROUND(
                    SQRT(
                        SUM(
                            (bidAmount - avg_bid) * (bidAmount - avg_bid) 
                        ) / (COUNT(bidAmount) - 1)
                    ), 2)
            ELSE 
                NULL
        END AS std
    FROM 
    (
        SELECT 
            itemID,
            bidAmount,
            (SELECT AVG(bidAmount) FROM bids AS b2 WHERE b2.itemID = b.itemID) AS avg_bid
        FROM 
            bids AS b
    ) AS sub
    GROUP BY 
        itemID
    HAVING 
        COUNT(*) > 1'''
    return None


# In[6]:


#Exercise 2

def bidder_spend_frac() -> str:
    """
    Create table TotalBids; create table TotalSpend
    Extract column max_bids from TotalBids; extract column sum_paid from TotalSpend
    Put biddername, total_spend, total_bids and spend_frac together 
    """
    q = '''
    WITH TotalBids as (SELECT itemid, biddername, max(bidamount) AS max_bids
    FROM bids
    GROUP BY itemid, biddername),
    
    TotalSpend as(
    SELECT b.itemid, b.highbiddername as biddername, sum(b.bidamount) as sum_paid
    FROM bids as b
    LEFT JOIN items AS i ON b.itemid=i.itemid
    WHERE i.currentprice = b.bidamount
    GROUP BY b.highbiddername, b.itemid)
    
    SELECT b.biddername, ts.sum_paid AS total_spend, tb.max_bids AS total_bids, (ts.sum_paid / tb.max_bids) AS spend_frac
    FROM bids as b
    RIGHT JOIN TotalSpend AS ts ON ts.biddername = b.biddername
    LEFT JOIN TotalBids AS tb ON tb.biddername = b.biddername
        '''
    return None


# In[7]:


#Exercise 3

def min_increment_freq() -> str:
    """
    Create difference for consecutive bids,
    Check for min_increments,
    Ensure that difference = min_increments (= 1),
    Count total number of bids,
    Calculate freq fraction
    """
    q = '''
    WITH bid_differences AS (
        SELECT b.itemid, b.bidamount - LAG(b.bidamount) OVER (PARTITION BY b.itemid ORDER BY b.bidtime) AS diff
        FROM bids AS b
        JOIN items AS i ON b.itemid = i.itemid
        WHERE i.isBuyNowUsed != 1
    ),
    min_increments AS (
        SELECT itemid, MIN(bidIncrement) AS min_inc
        FROM items
        WHERE isBuyNowUsed != 1
        GROUP BY itemid
    ),
    valid_bids AS (
        SELECT bd.itemid, bd.diff, mi.min_inc, count(bd.diff) AS numer
        FROM bid_differences AS bd
        JOIN min_increments AS mi ON bd.itemid = mi.itemid
        WHERE bd.diff = mi.min_inc
    ),
    num_bids AS (
        SELECT b.itemid, COUNT(*) AS total_num
        FROM bids AS b
        JOIN items AS i ON b.itemid = i.itemid
        WHERE i.isBuyNowUsed != 1
        GROUP BY b.itemid
    )
    SELECT ROUND(CAST(COUNT(vb.diff) AS FLOAT) / SUM(nb.total_num), 2) AS freq
    FROM valid_bids AS vb
    JOIN num_bids AS nb ON vb.itemid = nb.itemid
    '''
    return None


# In[12]:


q = 'select * from bids'
print(auctions.query(q).tail())


# In[16]:


#Exercise 4
def win_perc_by_timestamp() -> str:
    """
    Calculate the denominator (range of data) for the normalized data.
    Calculate the normalized data.
    Create bins.
    Calculate the number of winnings. Select them into timestamp bins.
    Create timestamp_bin and win_perc columns.  
    """
    
    q = '''
        WITH a AS (
            SELECT itemid, starttime, endtime, (julianday(endtime) - julianday(starttime)) AS length
            FROM items
        ),
        b_normalized AS (
            SELECT b.itemid, b.bidtime, b.biddername, a.starttime, a.endtime, ((julianday(a.endtime) - julianday(b.bidtime)) / a.length) AS time_norm
            FROM bids AS b
            INNER JOIN a ON b.itemid = a.itemid
        ),
        binned_bids AS (
            SELECT itemid, biddername, CASE 
                WHEN time_norm BETWEEN 0.9 AND 1.0 THEN 10
                WHEN time_norm BETWEEN 0.8 AND 0.9 THEN 9
                WHEN time_norm BETWEEN 0.7 AND 0.8 THEN 8
                WHEN time_norm BETWEEN 0.6 AND 0.7 THEN 7
                WHEN time_norm BETWEEN 0.5 AND 0.6 THEN 6
                WHEN time_norm BETWEEN 0.4 AND 0.5 THEN 5
                WHEN time_norm BETWEEN 0.3 AND 0.4 THEN 4
                WHEN time_norm BETWEEN 0.2 AND 0.3 THEN 3
                WHEN time_norm BETWEEN 0.1 AND 0.2 THEN 2
                WHEN time_norm BETWEEN 0.0 AND 0.1 THEN 1
                ELSE NULL
                END AS timestamp_bin
            FROM b_normalized
        ),
        winning_bids AS (
            SELECT b.itemid, b.biddername AS winner
            FROM bids AS b
            INNER JOIN items AS i ON b.itemid = i.itemid
            WHERE b.bidamount = i.currentprice
            GROUP BY b.itemid, b.biddername
        ),
        bin_wins AS (
            SELECT bb.timestamp_bin, COUNT(*) AS total_bids, SUM(CASE WHEN bb.biddername = wb.winner THEN 1 ELSE 0 END) AS win_count
            FROM binned_bids AS bb
            LEFT JOIN winning_bids AS wb ON bb.itemid = wb.itemid
            GROUP BY bb.timestamp_bin
        )
        SELECT timestamp_bin, ROUND(CAST(win_count AS FLOAT) / total_bids, 2) AS win_perc
        FROM bin_wins
        WHERE timestamp_bin IS NOT NULL
        ORDER BY timestamp_bin
    '''
    return None


# In[ ]:




