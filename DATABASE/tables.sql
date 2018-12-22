
DROP TABLE IF EXISTS tbl_categories;
CREATE TABLE tbl_categories (Type VARCHAR(5), Level1 VARCHAR(50), Level2 VARCHAR(50));
CREATE INDEX tbl_categories_idx_1 ON tbl_categories(Type);
CREATE INDEX tbl_categories_idx_2 ON tbl_categories(Level1);

DROP TABLE IF EXISTS tbl_account;
CREATE TABLE tbl_account (AcctID INTEGER PRIMARY KEY,Type INTEGER,Name VARCHAR(100), Bank VARCHAR(50), AccountNo VARCHAR(20), Currency VARCHAR(3),StartingBalance NUMERIC,Notes TEXT);
CREATE INDEX tbl_account_idx_1 ON tbl_account(AcctID);
CREATE INDEX tbl_account_idx_2 ON tbl_account(Type);

DROP TABLE IF EXISTS tbl_account_creditcard;
CREATE TABLE tbl_account_creditcard (AcctID INTEGER PRIMARY KEY,CreditLimit);
CREATE INDEX tbl_account_creditcard_idx_1 ON tbl_account_creditcard(AcctID);

DROP TABLE IF EXISTS tbl_account_loan;
CREATE TABLE tbl_account_loan (AcctID INTEGER PRIMARY KEY, Term INTEGER, Rate NUMERIC, Frequency INTEGER, 
	DeductFrom INTEGER, TotalOutstanding NUMERIC);
CREATE INDEX tbl_account_loan_idx_1 ON tbl_account_loan(AcctID);

DROP TABLE IF EXISTS tbl_transaction;
CREATE TABLE tbl_transaction (TransactionID INTEGER PRIMARY KEY,SubID INTEGER,Type VARCHAR(5), Level1 VARCHAR(50), Level2 VARCHAR(50), AcctID INTEGER, 
	Currency VARCHAR(3), Amount NUMERIC, TransactionDate TEXT, Payee VARCHAR(100), Notes TEXT);
CREATE INDEX tbl_transaction_idx_1 ON tbl_transaction(TransactionID);
CREATE INDEX tbl_transaction_idx_2 ON tbl_transaction(Level1, Level2, TransactionDate);
CREATE INDEX tbl_transaction_idx_3 ON tbl_transaction(AcctID, TransactionDate);
CREATE INDEX tbl_transaction_idx_4 ON tbl_transaction(AcctID, Payee);

DROP TABLE IF EXISTS tbl_transaction_tag;
CREATE TABLE tbl_transaction_tag (TransactionID INTEGER,TagID INTEGER);

DROP TABLE IF EXISTS tbl_tag;
CREATE TABLE tbl_tag (TagID INTEGER PRIMARY KEY,Description VARCHAR(200));

DROP TABLE IF EXISTS tbl_transaction_portfolio;
CREATE TABLE tbl_transaction_portfolio (TransactionID INTEGER PRIMARY KEY, SecurityCode VARCHAR(20), 
	Units NUMERIC, PricePerUnit NUMERIC, Fees NUMERIC);
CREATE INDEX tbl_transaction_portfolio_idx_1 ON tbl_transaction_portfolio(SecurityCode);

DROP TABLE IF EXISTS tbl_security;
CREATE TABLE tbl_security (SecurityCode VARCHAR(20) PRIMARY KEY, SecurityName VARCHAR(100));

DROP TABLE IF EXISTS tbl_security_quote;
CREATE TABLE tbl_security_quote (SecurityCode VARCHAR(20) PRIMARY KEY, QuoteDate TEXT, Price NUMERIC);

