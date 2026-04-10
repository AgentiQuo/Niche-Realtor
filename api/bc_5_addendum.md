# BC-5 Addendum: GET /niche/list

**Purpose**: Retrieve a list of all defined niches in the system.

## Route specifications
- **Path**: `GET /niche/list`

## Request Shape
- **Body**: None
- **Query Parameters**:
  - `page` (optional integer): Placeholder for pagination (default: 1)
  - `limit` (optional integer): Placeholder for results per page (default: 50)

## Response Shape
Returns an array of `Niche` objects.

```json
[
  {
    "niche_id": "string",
    "name": "string",
    "description": "string",
    "tags": ["Tag"],
    "neighborhoods": ["Neighborhood"],
    "embedding": [0.0],
    "sources": ["string"]
  }
]
```

## Error Cases
- **500 Internal Server Error**: If the underlying relational db or service layer experiences a critical failure querying collections.
