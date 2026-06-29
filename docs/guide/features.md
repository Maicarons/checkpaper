# Features

CheckPaper provides **6 core validation capabilities** for academic paper verification. Each can be run independently or combined for comprehensive analysis.

## 1. Format Checking

**Type:** `format`

Validates the structural and formatting compliance of your paper.

### What It Checks

| Check | Description |
|-------|-------------|
| Heading Hierarchy | Verifies heading levels are consistent and properly nested (H1 → H2 → H3) |
| Numbering | Checks section, figure, table, and equation numbering is sequential and gap-free |
| Font Consistency | Validates font families and sizes are uniform across similar elements |
| Page Layout | Checks margins, headers, footers, and page size compliance |
| TOC Accuracy | Verifies the table of contents matches actual section titles and page numbers |
| Paragraph Format | Validates indentation, line spacing, and paragraph spacing consistency |

### Severity Levels

- **Critical:** Heading levels skipped (e.g., H1 → H3 without H2)
- **Warning:** Numbering gaps or inconsistent formatting
- **Info:** Minor style deviations that don't affect readability

## 2. Figure & Table Reference Check

**Type:** `figure_table`

Ensures all figures and tables are properly referenced in the text.

### What It Checks

| Check | Description |
|-------|-------------|
| Citation Completeness | Every defined figure/table has at least one in-text reference |
| Number Matching | Citation numbers match the actual definition numbers |
| Orphan Detection | Finds references to figures/tables that don't exist |
| Unused Detection | Finds defined figures/tables never referenced in the text |

### Example Issues Found

```
🔴 Critical: "Figure 5" is referenced on page 8 but only Figures 1-4 are defined
🟡 Warning: "Table 2" is defined on page 5 but never referenced in the text
🔵 Info: Consider using "as shown in" format for more formal references
```

## 3. Citation Integrity Check

**Type:** `citation`

Validates the consistency between in-text citations and the reference list.

### What It Checks

| Check | Description |
|-------|-------------|
| Citation-Reference Matching | Every `[1]` or `(Author, Year)` citation has a matching reference entry |
| Duplicate Detection | Identifies duplicate entries in the reference list |
| Missing References | Finds citations that reference non-existent entries |
| Format Consistency | Checks citation format is uniform (e.g., all numeric or all author-year) |
| Ordering | Verifies references are ordered according to citation style rules |

## 4. Data Source Verification

**Type:** `data_source`

Verifies the authenticity and accessibility of data sources cited in the paper.

### What It Checks

| Check | Description |
|-------|-------------|
| Source Annotation | Data sources are explicitly cited with URLs or DOIs |
| URL Accessibility | Referenced dataset URLs are live and accessible |
| Content Match | Data descriptions match the actual dataset content |
| Fraud Detection | Identifies suspicious or fabricated data source claims |

## 5. Data Processing Verification

**Type:** `data_processing`

Validates the statistical methods and data processing claims in the paper.

### What It Checks

| Check | Description |
|-------|-------------|
| Statistical Methods | Validates that claimed statistical methods are appropriate for the data |
| Sample Size | Checks whether the sample size is sufficient for the reported analyses |
| p-value Reasonability | Verifies reported p-values and confidence intervals are mathematically plausible |
| GRIM/SPRITE Tests | Runs GRIM (Granularity-Related Inconsistency of Means) and SPRITE tests to detect impossible statistics |
| Figure-Text Consistency | Checks that numerical values in figures match those reported in the text |

### Statistical Tests

| Test | Purpose |
|------|---------|
| **GRIM** | Tests whether a reported mean is possible given the sample size and scale granularity |
| **SPRITE** | Tests whether reported statistics are mutually consistent |

## 6. Reference Verification

**Type:** `reference`

Verifies the authenticity of references against external academic databases.

### What It Checks

| Check | Description |
|-------|-------------|
| DOI Validation | Verifies DOI exists and resolves correctly |
| Metadata Matching | Compares title, authors, journal, year against Crossref/Semantic Scholar data |
| Journal Credibility | Detects potentially predatory or non-existent journals |
| Online Search | Uses web search to verify reference existence when API data is insufficient |

### APIs Used

| API | Purpose |
|-----|---------|
| **Crossref** | DOI metadata, citation counts, journal information |
| **Semantic Scholar** | Paper metadata, citation graphs, influence metrics |

## Combining Validation Types

You can run any combination of validation types for a single paper:

```bash
# Run all validations
curl -X POST http://localhost:9031/api/v1/validation/start \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "your-doc-id",
    "validation_types": ["format", "figure_table", "citation", "data_source", "data_processing", "reference"]
  }'

# Run only format and citation checks (faster)
curl -X POST http://localhost:9031/api/v1/validation/start \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "your-doc-id",
    "validation_types": ["format", "citation"]
  }'
```

## Severity System

All issues are categorized by severity:

| Level | Icon | Description | Examples |
|-------|------|-------------|----------|
| **Critical** | 🔴 | Serious issues that may indicate fraud or fundamental errors | Fabricated data, missing references, impossible statistics |
| **Warning** | 🟡 | Issues that should be addressed before submission | Formatting inconsistencies, incomplete citations |
| **Info** | 🔵 | Suggestions for improvement | Style recommendations, optimization tips |

## Next Steps

- [API Reference](/api/) — Complete API documentation
- [Deployment](/guide/deployment) — Production deployment guide
