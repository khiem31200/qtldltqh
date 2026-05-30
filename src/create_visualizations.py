"""
Script to generate multi‑dimensional data visualizations for the
CMP_SC‑8630 data visualization assignment.  The script loads three
real‑world datasets related to climate and hydrology and produces
visualizations that explore patterns across multiple variables and
dimensions.  The resulting figures are saved to the ``output``
directory.  The datasets used here include:

* ``weather_data.csv`` – daily weather observations for multiple
  cities in New Zealand (2016–2017) containing temperature,
  humidity, wind, pressure and precipitation variables.  Source:
  mosaicData package within the Rdatasets collection.
* ``global_temp.csv`` – NASA Goddard Institute for Space Studies
  (GISTEMP) global land–ocean temperature anomalies from 1880 to
  2025.  Monthly anomalies relative to the 1951–1980 baseline are
  provided.  Source: NASA GISS via data.giss.nasa.gov.
* ``minnesota_weather.csv`` – monthly weather summary for six
  Minnesota agricultural sites (1927–1936) including cooling and
  heating degree days, precipitation and temperature extremes.
  Source: agridat package within Rdatasets.

The visualizations include heatmaps, scatter plots and line charts
to illustrate how variables such as temperature, humidity and
precipitation vary over time and across different locations.
"""

import os
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def ensure_output_dir(path: str) -> None:
    """Ensure that the output directory exists."""
    os.makedirs(path, exist_ok=True)


def plot_weather_heatmap(df: pd.DataFrame, outdir: str) -> str:
    """Create a heatmap of average temperature by city and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Weather data with columns ``city``, ``month`` and ``avg_temp``.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # TODO: Students implement this function to generate "weather_heatmap.png"
    #
    # Instructions:
    # 1. Compute the average monthly temperature for each city (group by 'city' and 'month', calculate mean of 'avg_temp').
    # 2. Pivot the result to create a matrix with 'city' as index, 'month' as columns, and average temperature as values.
    # 3. Ensure the columns (months) are sorted in calendar order.
    # 4. Create a heatmap using seaborn.heatmap():
    #    - Set figsize to (10, 4)
    #    - Use 'coolwarm' colormap
    #    - Add a colorbar with label "Average temperature"
    #    - Enable annotations (annot=True) with float format '.1f'
    # 5. Set title "Average monthly temperature by city", xlabel "Month", and ylabel "City".
    # 6. Save the figure as "weather_heatmap.png" in outdir (using 300 dpi and tight layout) and return the saved file path.

    monthly = df.groupby(["city", "month"])["avg_temp"].mean().reset_index()
    pivot = monthly.pivot(index="city", columns="month", values="avg_temp")
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(
        pivot,
        cmap="coolwarm",
        annot=True,
        fmt=".1f",
        cbar_kws={"label": "Average temperature"},
        ax=ax,
    )
    ax.set_title("Average monthly temperature by city")
    ax.set_xlabel("Month")
    ax.set_ylabel("City")

    out_path = os.path.join(outdir, "weather_heatmap.png")
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


def plot_weather_scatter(df: pd.DataFrame, outdir: str) -> str:
    """Create a scatter plot exploring relationships between humidity,
    temperature and precipitation.

    Each point represents a daily observation.  The x‑axis shows
    average humidity, the y‑axis shows average temperature in Fahrenheit,
    the marker size encodes precipitation and colour encodes the city.
    Separate legends are provided for city and precipitation to avoid
    overlap.

    Parameters
    ----------
    df : pandas.DataFrame
        Weather data with columns ``avg_humidity``, ``avg_temp``,
        ``precip`` and ``city``.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # TODO: Students implement this function to generate "weather_scatter.png"
    #
    # Instructions:
    # 1. Clean the 'precip' column by converting it to numeric (coercing errors to NaN) and filling missing values with 0.0.
    # 2. Set up the figure with figsize=(9, 6).
    # 3. Set a marker size range, e.g., size_range = (20, 300).
    # 4. Generate a scatter plot using seaborn.scatterplot():
    #    - x-axis: "avg_humidity" (Label: "Average relative humidity (%)")
    #    - y-axis: "avg_temp" (Label: "Average temperature (°F)")
    #    - hue: "city"
    #    - size: "precip" with sizes=size_range
    #    - Use alpha=0.65 for transparency
    #    - Hide the default legend to draw custom separate legends (legend=False)
    # 5. Create a custom legend for the cities (hue):
    #    - Draw circles with corresponding colors using matplotlib.lines.Line2D.
    #    - Place it at loc="upper left", bbox_to_anchor=(1.02, 1.0) with title "City".
    # 6. Create a custom legend for precipitation sizes (size):
    #    - Choose representative quantiles/values of precip (e.g. 4 values from 0 to max).
    #    - Use plt.scatter() with proportional sizes mapped using np.interp to size_range.
    #    - Place it at loc="lower left", bbox_to_anchor=(1.02, 0.0) with title "Precipitation".
    # 7. Add title "Daily weather: temperature vs humidity with precipitation (size)".
    # 8. Save the figure as "weather_scatter.png" in outdir (using 300 dpi and tight layout) and return the saved file path.

    from matplotlib.lines import Line2D

    data = df.copy()
    data["precip"] = pd.to_numeric(data["precip"], errors="coerce").fillna(0.0)

    fig, ax = plt.subplots(figsize=(9, 6))
    size_range = (20, 300)

    sns.scatterplot(
        data=data,
        x="avg_humidity",
        y="avg_temp",
        hue="city",
        size="precip",
        sizes=size_range,
        alpha=0.65,
        legend=False,
        ax=ax,
    )
    ax.set_xlabel("Average relative humidity (%)")
    ax.set_ylabel("Average temperature (°F)")
    ax.set_title("Daily weather: temperature vs humidity with precipitation (size)")

    cities = sorted(data["city"].dropna().unique())
    palette = sns.color_palette(n_colors=len(cities))
    city_handles = [
        Line2D(
            [0], [0],
            marker="o",
            color="w",
            markerfacecolor=palette[i],
            markersize=9,
            label=city,
        )
        for i, city in enumerate(cities)
    ]
    city_legend = ax.legend(
        handles=city_handles,
        title="City",
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
    )
    ax.add_artist(city_legend)

    precip_min = float(data["precip"].min())
    precip_max = float(data["precip"].max())
    if precip_max <= precip_min:
        precip_max = precip_min + 1.0
    sample_values = np.linspace(precip_min, precip_max, 4)
    sample_sizes = np.interp(
        sample_values,
        [precip_min, precip_max],
        size_range,
    )
    precip_handles = [
        plt.scatter([], [], s=size, color="gray", alpha=0.65, label=f"{val:.2f}")
        for val, size in zip(sample_values, sample_sizes)
    ]
    ax.legend(
        handles=precip_handles,
        title="Precipitation",
        loc="lower left",
        bbox_to_anchor=(1.02, 0.0),
    )

    out_path = os.path.join(outdir, "weather_scatter.png")
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


def plot_global_temp_heatmap(df: pd.DataFrame, outdir: str) -> str:
    """Create a heatmap of global temperature anomalies by year and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Global temperature anomalies where rows correspond to years and
        columns to months (Jan–Dec).  The DataFrame should include
        numeric values for anomalies.  Missing values are allowed and
        will appear as blank cells.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # TODO: Students implement this function to generate "global_temp_heatmap.png"
    #
    # Instructions:
    # 1. Reshape the dataframe from wide to long format using pandas.melt():
    #    - Keep 'Year' as id_vars, and months 'Jan' to 'Dec' as value_vars.
    #    - Name the variable column "Month" and value column "Anomaly".
    # 2. Map Month abbreviations to month numbers (1 to 12) so they are sorted chronologically.
    # 3. Pivot the long dataframe back to a matrix with 'Year' as index, 'MonthNum' as columns, and 'Anomaly' as values.
    # 4. Ensure the matrix is sorted by year index in ascending order.
    # 5. Set up the figure with figsize=(10, 8).
    # 6. Draw a heatmap using seaborn.heatmap():
    #    - Use colormap 'coolwarm'
    #    - Set colormap limits to vmin=-1.5 and vmax=1.5
    #    - Set cbar_kws with label "Temperature anomaly (°C relative to 1951–1980)"
    #    - Set linewidths=0 and linecolor="white"
    # 7. Customize x-ticks to display month abbreviations ('Jan' to 'Dec') rotated by 45 degrees.
    # 8. Set title "Global land–ocean temperature anomalies (1880–2025)", xlabel "Month", and ylabel "Year".
    # 9. Save the figure as "global_temp_heatmap.png" in outdir (using 300 dpi and tight layout) and return the saved file path.

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    long_df = df.melt(
        id_vars="Year",
        value_vars=months,
        var_name="Month",
        value_name="Anomaly",
    )
    month_map = {name: i + 1 for i, name in enumerate(months)}
    long_df["MonthNum"] = long_df["Month"].map(month_map)
    long_df["Anomaly"] = pd.to_numeric(long_df["Anomaly"], errors="coerce")

    matrix = long_df.pivot(index="Year", columns="MonthNum", values="Anomaly")
    matrix = matrix.sort_index(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        matrix,
        cmap="coolwarm",
        vmin=-1.5,
        vmax=1.5,
        cbar_kws={"label": "Temperature anomaly (°C relative to 1951–1980)"},
        linewidths=0,
        linecolor="white",
        ax=ax,
    )
    ax.set_xticks(np.arange(len(months)) + 0.5)
    ax.set_xticklabels(months, rotation=45)
    ax.set_title("Global land–ocean temperature anomalies (1880–2025)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")

    out_path = os.path.join(outdir, "global_temp_heatmap.png")
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


def plot_minnesota_precip_line(df: pd.DataFrame, outdir: str) -> str:
    """Create a line chart of monthly precipitation by site over time.

    This figure shows how precipitation varies across the six Minnesota
    sites from 1927 to 1936.  Each line corresponds to a site and
    month; values are aggregated by year and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Minnesota weather data with columns ``site``, ``year``, ``mo`` (month) and
        ``precip``.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # TODO: Students implement this function to generate "minnesota_precip_line.png"
    #
    # Instructions:
    # 1. Create a datetime column named 'date' combining 'year' and 'mo' (month) with day set to 1.
    # 2. Set up the figure with figsize=(10, 6).
    # 3. Create a line plot using seaborn.lineplot():
    #    - x-axis: "date" (Label: "Year")
    #    - y-axis: "precip" (Label: "Precipitation (inches)")
    #    - hue: "site"
    # 4. Set title "Monthly precipitation by Minnesota site (1927–1936)".
    # 5. Place the legend outside the plot box on the upper right: bbox_to_anchor=(1.05, 1), loc="upper left", title="Site".
    # 6. Save the figure as "minnesota_precip_line.png" in outdir (using 300 dpi and tight layout) and return the saved file path.

    data = df.copy()
    data["date"] = pd.to_datetime(
        dict(year=data["year"], month=data["mo"], day=1)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=data,
        x="date",
        y="precip",
        hue="site",
        ax=ax,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Precipitation (inches)")
    ax.set_title("Monthly precipitation by Minnesota site (1927–1936)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Site")

    out_path = os.path.join(outdir, "minnesota_precip_line.png")
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


def main() -> List[str]:
    """Run all visualizations and return a list of generated file paths."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    out_dir = os.path.join(base_dir, "output")
    ensure_output_dir(out_dir)
    figures: List[str] = []

    # Load and plot weather data
    weather_path = os.path.join(data_dir, "weather_data.csv")
    weather_df = pd.read_csv(weather_path)
    # Plot heatmap and scatter
    figures.append(plot_weather_heatmap(weather_df, out_dir))
    figures.append(plot_weather_scatter(weather_df, out_dir))

    # Load and plot global temperature anomalies
    global_path = os.path.join(data_dir, "global_temp.csv")
    global_df = pd.read_csv(global_path, skiprows=1)
    # Replace *** with NA and convert to numeric
    global_df = global_df.replace("***", pd.NA)
    for col in global_df.columns[1:]:
        global_df[col] = pd.to_numeric(global_df[col], errors="coerce")
    figures.append(plot_global_temp_heatmap(global_df, out_dir))

    # Load and plot Minnesota weather data
    minn_path = os.path.join(data_dir, "minnesota_weather.csv")
    minn_df = pd.read_csv(minn_path)
    figures.append(plot_minnesota_precip_line(minn_df, out_dir))
    return figures


if __name__ == "__main__":
    generated = main()
    print("Generated figures:")
    for path in generated:
        print(path)