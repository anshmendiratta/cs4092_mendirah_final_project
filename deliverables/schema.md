```
Customer(
    CustomerID PK,

    FirstName,
    LastName,
    Email,
    Phone
)

Staff(
    StaffID PK,

    FirstName,
    LastName,
    Position
)

Product(
    ProductID PK,
    StaffID FK

    Name,
    Description,
    Price,
    Stock,
)

CreditCard(
    CardID PK,
    CustomerID FK,

    CardNumber,
    ExpirationMonth,
    ExpirationYear,
    CardholderName
)

Purchase(
    PurchaseID PK,
    CustomerID FK,
    CardID FK,

    PurchaseDate
)

PurchaseItem(
    PurchaseID FK,
    ProductID FK,

    Quantity,
    UnitPrice,

    PK(PurchaseID, ProductID)
)
```
