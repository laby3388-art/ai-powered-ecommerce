# Entity relationship diagram

```mermaid
erDiagram
    USER ||--o{ CART_ITEM : owns
    USER ||--o{ ORDER : places
    CATEGORY ||--o{ PRODUCT : groups
    PRODUCT ||--o{ CART_ITEM : appears_in
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : snapshots

    USER {
      int id PK
      string username
      string password_hash
    }
    CATEGORY {
      int id PK
      string name UK
      string slug UK
    }
    PRODUCT {
      int id PK
      int category_id FK
      string name
      decimal price
      int stock
      boolean is_active
    }
    CART_ITEM {
      int id PK
      int user_id FK
      int product_id FK
      int quantity
      string unique_user_product
    }
    ORDER {
      int id PK
      int user_id FK
      string status
      decimal total
      datetime created_at
    }
    ORDER_ITEM {
      int id PK
      int order_id FK
      int product_id FK
      string product_name_snapshot
      decimal unit_price_snapshot
      int quantity
    }
```

Django's built-in `User` table is used for customers and administrator accounts. Order items retain the product name and unit price from checkout so the receipt remains meaningful if catalog details later change.
