# from sqlalchemy import create_engine

# path = '/Users/weijiaying/Desktop/ECON481/auctions.db'
# engine = create_engine(f'sqlite:///{path}')

# from sqlalchemy import inspect

# inspector = inspect(engine)
# # print(inspector.get_table_names())

# import pandas as pd
# from sqlalchemy.orm import Session

# class DataBase:
#     def __init__(self, loc: str, db_type: str = "sqlite") -> None:
#         """Initialize the class and connect to the database"""
#         self.loc = loc
#         self.db_type = db_type
#         self.engine = create_engine(f'{self.db_type}:///{self.loc}')
#     def query(self, q: str) -> pd.DataFrame:
#         """Run a query against the database and return a DataFrame"""
#         with Session(self.engine) as session:
#             df = pd.read_sql(q, session.bind)
#         return(df)

# auctions = DataBase(path)

# q = 'select * from bids'
# print(auctions.query(q).head())


### Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/<user>/<repo>/blob/main/<filename.py>"

### Exercise 1
def std() -> str:
    """
    Return a SQL query that cauculated the standard deviation and output with two column: itemId and std.
    """

    query = """
    SELECT 
        itemId,
        CASE
            WHEN COUNT(bidAmount) > 1 THEN 
                SQRT(SUM((bidAmount - avg_bidAmount) * (bidAmount - avg_bidAmount)) / (COUNT(bidAmount) - 1))
            ELSE 
                NULL
        END as std
    FROM 
        (SELECT 
            itemId, 
            bidAmount, 
            AVG(bidAmount) OVER (PARTITION BY itemId) AS avg_bidAmount 
        FROM 
            bids) subquery
    GROUP BY 
        itemId
    HAVING 
        COUNT(bidAmount) > 1;
    """
    return query

# Get the SQL query
# query = std()

# # Execute the query and fetch the results into a DataFrame
# df = auctions.query(query)

# # Print the DataFrame
# print(df)

### Exercse 2
def bidder_spend_frac() -> str:
    """
    Returns a string containing a SQL query that can be run against the auctions.db database 
    that outputs a table that has four columns
    bidderName, total_spend, total_bids, spend_frac: total_spend/total_bids.
    """
    query = """
    WITH MaxBids AS (
        SELECT 
            bidderName, 
            itemId, 
            MAX(bidAmount) AS max_bid
        FROM 
            bids
        GROUP BY 
            bidderName, itemId
    ),
    TotalSpend AS (
        SELECT 
            bidderName, 
            SUM(max_bid) AS total_spend
        FROM 
            MaxBids
        GROUP BY 
            bidderName
    ),
    TotalBids AS (
        SELECT 
            bidderName, 
            SUM(bidAmount) AS total_bids
        FROM 
            bids
        GROUP BY 
            bidderName
    )
    SELECT 
        ts.bidderName,
        ts.total_spend,
        tb.total_bids,
        CASE
            WHEN tb.total_bids > 0 
            THEN ts.total_spend * 1.0 / tb.total_bids
            ELSE 0
        END AS spend_frac
    FROM 
        TotalSpend ts
    JOIN 
        TotalBids tb ON ts.bidderName = tb.bidderName;
    """
    return query

# #
# query = bidder_spend_frac()

# df = auctions.query(query)
# print(df)

### Exercise 3
def min_increment_freq() -> str:
    """
    Returns a string containing a SQL query that can be run against the auctions.db database 
    that outputs a table that has one column (freq) which represents the fraction of bids in 
    the database that are exactly the minimum bid increment (items.bidIncrement) above the 
    previous high bid..
    """

    query = """
    WITH PreviousBids AS (
        SELECT
            bid1.itemId,
            bid1.bidAmount,
            bid1.bidderName,
            bid1.bidTime,
            bid2.bidAmount AS prev_bidAmount,
            i.bidIncrement
        FROM
            bids bid1
        LEFT JOIN
            bids bid2 ON bid1.itemId = bid2.itemId 
                    AND bid1.bidTime > bid2.bidTime
                    AND bid1.bidAmount > bid2.bidAmount
        JOIN
            items i ON bid1.itemId = i.itemId
        WHERE
            i.isBuyNowUsed = 0
    ),
    RankedBids AS (
        SELECT
            itemId,
            bidAmount,
            prev_bidAmount,
            bidIncrement,
            ROW_NUMBER() OVER (PARTITION BY itemId, bidAmount ORDER BY prev_bidAmount DESC) AS rn
        FROM
            PreviousBids
    ),
    ValidBids AS (
        SELECT
            itemId,
            bidAmount,
            bidIncrement,
            prev_bidAmount
        FROM
            RankedBids
        WHERE
            rn = 1
    )
    SELECT
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM bids WHERE itemId IN (SELECT itemId FROM items WHERE isBuyNowUsed = 0)) AS freq
    FROM
        ValidBids
    WHERE
        bidAmount = prev_bidAmount + bidIncrement;
    """
    return query

# query = min_increment_freq()

# df = auctions.query(query)
# print(df)

### Exercise 4
def win_perc_by_timestamp() -> str:
    """
    Returns a string containing a SQL query that can be run against the auctions.db database 
    that outputs a table that has two columns: timestamp_bin & win_perc.
    """

    query = """
    WITH AuctionTimes AS (
        SELECT 
            itemId,
            MIN(bidTime) AS auctionStartTime,
            MAX(bidTime) AS auctionEndTime
        FROM 
            bids
        GROUP BY 
            itemId
    ),
    BinnedBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.bidAmount,
            b.bidTime,
            a.auctionStartTime,
            a.auctionEndTime,
            ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
            (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) AS normalized_time,
            CASE
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.1 THEN 1
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.2 THEN 2
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.3 THEN 3
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.4 THEN 4
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.5 THEN 5
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.6 THEN 6
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.7 THEN 7
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.8 THEN 8
                WHEN ((julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                     (julianday(a.auctionEndTime) - julianday(a.auctionStartTime))) <= 0.9 THEN 9
                ELSE 10
            END AS timestamp_bin
        FROM
            bids b
        JOIN
            AuctionTimes a ON b.itemId = a.itemId
    ),
    WinningBids AS (
        SELECT
            itemId,
            MAX(bidAmount) AS winningBidAmount
        FROM
            bids
        GROUP BY
            itemId
    ),
    BinnedWinningBids AS (
        SELECT
            b.itemId,
            b.bidderName,
            b.timestamp_bin
        FROM
            BinnedBids b
        JOIN
            WinningBids w ON b.itemId = w.itemId AND b.bidAmount = w.winningBidAmount
    )
    SELECT
        timestamp_bin,
        COUNT(b.itemId) * 1.0 / (SELECT COUNT(*) FROM BinnedBids WHERE BinnedBids.timestamp_bin = b.timestamp_bin) AS win_perc
    FROM
        BinnedWinningBids b
    GROUP BY
        timestamp_bin;
    """
    return query

# query = win_perc_by_timestamp()

# df = auctions.query(query)
# print(df)
