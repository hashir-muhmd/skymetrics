# Findings - SkyMetrics

## Delay causes vs. cancellation causes differ
Late Aircraft (124.15M total delay-minutes) and Carrier issues (107.01M) drive the
most delay time across the network. Weather, by contrast, contributes relatively
little to delay-minutes (18.31M) but is the dominant cause of outright
cancellations (165K of 287K cancelled flights, ~57%). When weather is bad enough
to disrupt flights, airlines tend to cancel rather than delay.

## Carrier on-time performance
Across 15 reporting carriers, on-time performance (arrivals within 15 minutes of
schedule) ranges from 85% (Endeavor Air) down to 71% (Frontier Airlines).
Legacy/regional carriers (Endeavor, Republic, Delta) top the list; ultra-low-cost
carriers (Frontier, JetBlue, Spirit) cluster at the bottom, consistent with public
industry reputation.

## Carrier performance spread
Best-to-worst on-time performance among the 15 carriers spans 14.1 percentage
points: Endeavor Air (85.5%) to Frontier Airlines (71.4%), with network average at
79.1%. The same ordering holds for average arrival delay: Endeavor Air has the
lowest (0.23 min) and Frontier the highest (16.00 min), so the two metrics tell a
consistent story.

## Airport rankings require a minimum flight-volume filter
A naive ranking of airports by average arrival delay is dominated by small regional
airports, where one atypical month skews the average to look artificially good or
bad. Filtering to airports with 10,000+ flights over the period gives a far more
meaningful "major airport" ranking. Among major airports, mountain/resort airports
(e.g. Eagle-Vail, CO) and major Sun Belt hubs (Miami, Dallas-Fort Worth, Fort
Lauderdale) show the highest average delays, plausibly linked to weather exposure
and high traffic volume respectively.

## Seasonality
Flight volume is fairly flat across the year (1.53M in February to 1.87M in July,
summed over 2023-2025), with February the low point (shortest month) and July the
peak. On-time performance varies far more than volume does: monthly on-time %
ranges from 71.8% in July to 83.9% in November, a 12.1-point spread. June and July
are the worst months (73.8% and 71.8%), while September through November are the
best (83.2% to 83.9%). Peak summer travel coincides with the weakest punctuality,
plausibly due to high traffic and summer weather, though this dataset doesn't
isolate the cause by month.

## Day-of-week pattern
On-time performance is best on Tuesday (82.3%) and Wednesday (81.2%) and worst on
Sunday (76.6%) and Friday (77.4%), a 5.7-point spread. The worst days line up with
peak weekend travel periods.

## Year-over-year growth
Flight volume grew steadily through 2024 compared to 2023, but growth flattened
and dipped slightly negative in parts of 2025 compared to the prior year.

## NAS delay trend (2023-2025)
Average NAS (National Air System) delay rose from ~12.5 minutes in 2023 to ~16
minutes in 2025, a roughly 28% increase, the only delay cause showing a clear
worsening trend. Over the same period, average carrier delay modestly improved
(from ~25 to ~23.5 minutes), and weather/security stayed roughly flat. This
suggests the primary bottleneck shifted from airline-controlled operations toward
air traffic system capacity.