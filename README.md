# Gapminder Streamlit App in a Docker Environment

This project is a Dockerized version of a Streamlit application that visualizes Gapminder data, exploring relationships between life expectancy, GNI per capita, and population size.

## Features

- Interactive bubble chart:
  - x-axis: Logarithmic Gross National Income (GNI) per capita (PPP, inflation-adjusted).
  - y-axis: Life expectancy.
  - Bubble size: Population.
  - Color: Country.
- Year slider for selecting a specific year.
- Multiselect widget for choosing countries to display.

## Prerequisites

- Docker installed on your system
- CapRover installed and set up on a server
- Streamlit Account
- Github Account

## Data

- Source: [Gapminder Data](https://www.gapminder.org/data/)
- Indicators: Population, Life expectancy, GNI per capita (PPP, current international $)
