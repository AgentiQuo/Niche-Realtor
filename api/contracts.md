# Niche Realtor API Contracts

## POST `/niche/create`
**Purpose**: Create a new niche.
**Body**:
```json
{
  "name": "string",
  "description": "string",
  "sources": ["string"],
  "tags": ["Tag"]
}
```
**Returns**: `niche_id`

## POST `/property/ingest`
**Purpose**: Ingest a new property listing.
**Body**:
```json
{
  "url": "string",
  "images": ["string"],
  "metadata": {}
}
```
**Returns**: `property_id`

## POST `/property/analyze`
**Purpose**: Run Property Analysis Agent.
**Body**:
```json
{
  "property_id": "string"
}
```
**Returns**:
```json
{
  "tags": ["Tag"],
  "embedding": [0.0]
}
```

## POST `/neighborhood/analyze`
**Purpose**: Run Neighborhood Scout Agent.
**Body**:
```json
{
  "neighborhood_name": "string",
  "region": "string"
}
```
**Returns**:
```json
{
  "tags": ["Tag"],
  "embedding": [0.0],
  "vibe_summary": "string"
}
```

## POST `/client/create`
**Purpose**: Create a new client profile.
**Body**:
```json
{
  "preferences": {}
}
```
**Returns**: `client_id`

## POST `/client/update`
**Purpose**: Update client preferences + embedding.
**Body**:
```json
{
  "client_id": "string",
  "feedback": {}
}
```
**Returns**: `updated client_embedding`

## POST `/match`
**Purpose**: Match client ↔ niches ↔ properties ↔ neighborhoods.
**Body**:
```json
{
  "client_id": "string",
  "niche_id": "string"
}
```
**Returns**:
```json
{
  "ranked_results": [],
  "explanations": []
}
```
