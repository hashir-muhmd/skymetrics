# Data Cleaning Log — SkyMetrics

Documenting cleaning decisions as they're made, with reasoning — not just what was
changed, but why. Same honesty-first approach as SkyPulse: inconvenient or boring
findings get noted plainly, not glossed over.

---

## 2026-09-12 — Data acquisition and initial verification

**Source**: US BTS Reporting Carrier On-Time Performance (1987-present)
**Range**: 2023-2025, full calendar years only (36 monthly files)
**Scope decision**: Excluded 2020-2021 (COVID-era) to avoid an external shock
distorting delay/cancellation metrics. Excluded partial 2026 data (only Jan-Jun
available) to keep all three years directly comparable.
**Scope decision**: US domestic data only — Qatar Airways, Emirates, and Singapore
Airlines are not covered by this dataset (BTS only reports domestic US carriers).

**Verification performed**:
- Confirmed all 36 files have matching `YEAR`/`MONTH` values against their filenames
  (no mislabeled or wrong-month downloads)
- Confirmed all 36 files have **identical column structure** — safe to combine via
  Power Query's Combine & Transform
- Total combined row count: **20,928,599 rows**

**Column naming note**: BTS's actual CSV export uses `SCREAMING_SNAKE_CASE` column
names (e.g. `DEP_DELAY`, `ARR_DELAY`) rather than the friendly CamelCase labels shown
on the BTS field-selection webpage (`DepDelay`, `ArrDelay`). This is consistent across
all 36 files and is just how BTS structures its data dictionary — not an error.

**Missing field note**: `DAY_OF_WEEK` is not present in the exported columns, despite
being selectable on the BTS site. Not a blocker — it can be derived directly from
`FL_DATE` (a full date field) using Power Query's `Date.DayOfWeek()` function.

**Unexpected field note**: `DEST_AIRPORT_SEQ_ID` appeared in the export despite not
being part of the original field selection. Harmless — will be dropped during Power
Query cleanup since it's not used in the model.

**Null pattern finding** (key finding — explains a common analysis mistake):
| Column | Null count | Null % |
|---|---|---|
| DEP_DELAY | 276,090 | 1.3% |
| ARR_DELAY | 340,445 | 1.6% |
| CARRIER_DELAY | 16,557,293 | 79.1% |
| WEATHER_DELAY | 16,557,293 | 79.1% |
| NAS_DELAY | 16,557,293 | 79.1% |
| SECURITY_DELAY | 16,557,293 | 79.1% |
| LATE_AIRCRAFT_DELAY | 16,557,293 | 79.1% |
| CANCELLED | 0 | 0.0% |
| CANCELLATION_CODE | 20,641,465 | 98.6% |

The five delay-cause columns are null for ~79% of rows — this is **not missing data**.
Per BTS documentation, these columns are only populated when a flight was delayed
15+ minutes (`ARR_DEL15 = 1`). Null here means "cause not applicable" (the flight
wasn't delayed enough to have a cause recorded), not "unknown cause." This distinction
matters: blindly filling these nulls with 0 without this context would be technically
correct for aggregation purposes, but doing so without documenting *why* would hide
an important interpretive detail from anyone reviewing the analysis.

`DEP_DELAY`/`ARR_DELAY` nulls (~1.3-1.6%) are most likely cancelled/diverted flights
that never had a real departure/arrival to measure — to be confirmed once cancellation
logic is investigated in Power Query.

`CANCELLATION_CODE` is null for 98.6% of rows, consistent with only a small fraction
of flights being cancelled.

**Status**: Data acquisition phase complete. Moving into Power Query import and
cleaning phase next.


## 2026-09-14 — Power Query cleanup and star schema modeling

**Power Query cleaning completed**:
- Combined all 36 monthly CSVs into a single `Flights` fact table
- Renamed all columns from BTS's raw SCREAMING_SNAKE_CASE to clean, readable names
  (e.g. `DEP_DELAY` → `DepDelay`, `OP_UNIQUE_CARRIER` → `CarrierCode`)
- Fixed data types: `FlightDate` set to Date type, delay columns to Decimal Number,
  IDs/flags to Whole Number, text fields confirmed as Text
- Dropped unused columns: `DEST_AIRPORT_SEQ_ID`, `Source.Name`
- Derived `DayOfWeek` from `FlightDate` (not present in BTS's raw export) using
  `Date.DayOfWeekName()`
- Loaded full dataset into the model: confirmed 20,928,599 rows via card visual,
  matching the row count from independent Python verification

**Star schema built**:
- `Flights` (fact table) at the center
- `DimDate` — calendar table (2023-01-01 to 2025-12-31) with Year, Quarter, Month,
  DayOfWeek, IsWeekend, YearMonth; marked as the official Power BI date table
- `DimCarrier` — distinct carrier codes mapped to full airline names via SWITCH
- `DimAirport` — origin and destination airports combined and deduplicated into one
  dimension, since both columns represent the same real-world entity (an airport)

**Modeling decision — dual airport relationship**: `DimAirport` relates to `Flights`
twice (via `OriginAirport` and `DestAirport`), but Power BI only allows one active
relationship between two tables at a time. Set the Origin relationship as active
(default for most measures) and the Destination relationship as inactive, to be
activated explicitly per-measure using `USERELATIONSHIP()` for destination-side
analysis (e.g. "average arrival delay by destination airport").

**Status**: Data model complete. Moving into DAX measure-building next.