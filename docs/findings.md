# Findings — SkyMetrics

## Delay causes vs. cancellation causes differ
Late Aircraft (124.15M total delay-minutes) and Carrier issues (107.01M) drive the
most delay time across the network. Weather, by contrast, contributes relatively
little to delay-minutes (18.31M) — but is the dominant cause of outright
cancellations (165K of 287K cancelled flights, ~57%). When weather is bad enough
to disrupt flights, airlines tend to cancel rather than delay.

## Carrier on-time performance
Across 15 reporting carriers, on-time performance (arrivals within 15 minutes of
schedule) ranges from 85% (Endeavor Air) down to 71% (Frontier Airlines).
Legacy/regional carriers (Endeavor, Republic, Delta) top the list; ultra-low-cost
carriers (Frontier, JetBlue, Spirit) cluster at the bottom — consistent with public
industry reputation.

## Airport rankings require a minimum flight-volume filter
A naive ranking of airports by average arrival delay is dominated by small regional
airports (e.g. single-digit-thousands of flights over 3 years), where one atypical
month skews the average delay to look artificially good or bad. Filtering to
airports with 10,000+ flights over the period gives a far more meaningful "major
airport" ranking. Among major airports, mountain/resort airports (e.g. Eagle-Vail,
CO) and major Sun Belt hubs (Miami, Dallas-Fort Worth, Fort Lauderdale) show the
highest average delays — plausibly linked to weather exposure and high traffic
volume respectively.

## Seasonality
Flight volume shows a clear, repeating seasonal pattern across all three years:
dips in February (fewest days in the month) and peaks around July-August (summer
travel season).

## Year-over-year growth
Flight volume grew steadily through 2024 compared to 2023, but growth flattened
and dipped slightly negative in parts of 2025 compared to the prior year.