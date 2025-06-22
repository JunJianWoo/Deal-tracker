# API Documentation

## Table of Contents

- [GET /item-price-today](#get-item-price-today)
- [GET /similar-item/<desc>](#get-similar-itemdesc)

# GET /item-price-today

**Summary:**  
Retrieve today’s discounted item prices filtered by company source and price range.

---

### Request Query Parameters

| Name           | Type         | Description                           |
| -------------- | ------------ | ------------------------------------- |
| company_source | List[string] | Filter by one or more company sources |
| min_price      | Float        | Minimum discounted price (inclusive)  |
| max_price      | Float        | Maximum discounted price (inclusive)  |

---

### Success Response (200)

- **Content-Type:** application/json
- **Body:** List of objects combining item and price details

```json
[
  {
    "id": "17b10018-4de9-11f0-9f72-34f39a7bfa29",
    "name": "Sample Item",
    "image_link": "https://example.com/image.jpg",
    "website_link": "https://example.com/product",
    "company_source": "Sample Company",
    "date": "2025-06-22",
    "original_price": 1234,
    "discounted_price": 678
  }
]
```

# GET /similar-item/desc

**Summary:**  
Retrieve a list of items whose names contain the given description substring.

---

### URL Parameter

| Name | Type   | Description                           |
| ---- | ------ | ------------------------------------- |
| desc | string | Substring to search for in item names |

---

### Success Response (200)

- **Content-Type:** application/json
- **Body:** List of matching items

```json
[
  {
    "id": "abc123",
    "name": "Samsung Galaxy S24",
    "company_source": "JB Hi-Fi"
    // other item fields...
  },
  {
    "id": "def456",
    "name": "Samsung Galaxy S23",
    "company_source": "Other Store"
    // other item fields...
  }
]
```
