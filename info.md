# FirstStreet Integration for Home Assistant 🌍💧🔥

## Overview

The **FirstStreet Integration** allows users to get real-time environmental risk assessments based on property locations. This integration provides five sensors monitoring the risks associated with flooding, fires, heatwaves, winds, and air quality using data sourced from the FirstStreet API.

## Features

-   **Flood Sensor** 🌊: Monitors flood risk factors.
-   **Fire Sensor** 🔥: Assesses fire risk levels.
-   **Heat Sensor** 🌞: Evaluates heat-related risks.
-   **Wind Sensor** 🍃: Analyzes wind risk factors.
-   **Air Quality Sensor** 🌫️: Provides insights into local air quality risks.

## Installation

### HACS (Highly Recommended)

1. Ensure that [HACS](https://hacs.xyz) is installed in your Home Assistant.
2. In HACS, go to **Integrations** and click on the three dots (**...**) in the top right corner.
3. Select **Custom repositories**.
4. Add the repository URL: `https://github.com/harperreed/hass-firststreet` and select **Integration** as the category.
5. Click **Install**.
6. Restart Home Assistant.

### Manual Installation

1. Download the `firststreet` folder from this repository.
2. Place it in your `custom_components` directory in Home Assistant.
3. Restart Home Assistant.

## Configuration

1. In the Home Assistant UI, navigate to **Configuration > Integrations**.
2. Click the **+** button to add a new integration.
3. Search for **FirstStreet** and select it.
4. Follow the on-screen instructions to complete the setup.

## Usage

After successful installation and configuration, you'll see the following sensors in your Home Assistant dashboard:

-   FirstStreet Flood
-   FirstStreet Fire
-   FirstStreet Heat
-   FirstStreet Wind
-   FirstStreet Air

These sensors will provide essential data to make informed decisions about environmental risks to your property.

## Support

For issues or feature requests, please use the [GitHub issue tracker](https://github.com/harperreed/hass-firststreet/issues). Contributions are welcome; feel free to submit pull requests for enhancements or fixes.

Thank you for choosing the FirstStreet Integration! Together, let's create safer living environments. 🏡✨

```

### Instructions to save the file:
- Save the above content in a file named `info.md` and place it in the root of your repository alongside the `README.md` file.
- Ensure that all markdown formatting is preserved in order to provide a clean and readable output in HACS.
```
