-- List all products.
SELECT Name, Price, Stock FROM Product;

-- Find all customer who have more than one credit card.
SELECT
    Customer.FirstName,
    Customer.LastName,
    COUNT(CreditCard.CardID) AS NumberOfCards
FROM Customer
JOIN CreditCard
    ON Customer.CustomerID = CreditCard.CustomerID
GROUP BY Customer.CustomerID
HAVING COUNT(CreditCard.CardID) > 1;

-- List products in descending order of units sold.
SELECT
    Product.Name,
    SUM(PurchaseItem.Quantity) AS UnitsSold
FROM Product
JOIN PurchaseItem
    ON Product.ProductID = PurchaseItem.ProductID
GROUP BY Product.ProductID
ORDER BY UnitsSold DESC

