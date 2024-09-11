# FirstStreet Integration for Home Assistant 🌍💧🔥

Welcome to the **FirstStreet Integration for Home Assistant**! This project allows users to monitor risk factors associated with environmental conditions, such as flooding, fires, heatwaves, winds, and air quality, based on property location. All data is sourced from the FirstStreet API.

## Summary of Project 📜

This integration connects Home Assistant with the FirstStreet API, providing five distinct sensors:
- **Flood** 🌊
- **Fire** 🔥
- **Heat** 🌞
- **Wind** 🍃
- **Air Quality** 🌫️

With these sensors, users can access real-time risk assessments for their properties, enabling better decision-making when it comes to asset protection and personal safety.

## How to Use ⚙️

### Installation Steps

1. **HACS (Highly Recommended):**
   - Ensure you have [HACS](https://hacs.xyz) installed in your Home Assistant.
   - Go to **HACS > Integrations > 3 dots > Custom repositories**.
   - Add this repository URL: `https://github.com/harperreed/hass-firststreet` and select **Integration** for the category.
   - Click **Install**.
   - Restart Home Assistant for the changes to take effect.

2. **Manual Installation:**
   - Download the `firststreet` folder from this repository.
   - Place it in your `custom_components` directory in Home Assistant.
   - Restart Home Assistant.

### Configuration Steps 🔧

1. In the Home Assistant user interface, navigate to **Configuration > Integrations**.
2. Click on the **+** button to add a new integration.
3. Search for **FirstStreet** and select it.
4. Follow the on-screen instructions to complete the setup.

### Usage 📊

Upon successful setup, you will have access to the following sensors:
- **FirstStreet Flood:** Displays flood risk factors.
- **FirstStreet Fire:** Displays fire risk factors.
- **FirstStreet Heat:** Displays heat-related risk factors.
- **FirstStreet Wind:** Displays wind risk factors.
- **FirstStreet Air:** Displays air quality risk factors.

The risk factors provided by each sensor will help you evaluate the environmental risks related to your property. 

## Tech Info 🛠️

- **Languages & Frameworks:** 
  - Python
  - Home Assistant Framework
- **Key Dependencies:** 
  - `requests`
- **Core Functionality:**
  - Integrates with the FirstStreet API to pull risk factor data.
  - Utilizes Home Assistant’s custom component structure for seamless integration.
  - Supports data retrieval and JSON parsing for various environmental risks.

### Repository Structure 📁
```plaintext
hacs/
├── README.md
├── __init__.py
├── config_flow.py
├── const.py
├── firststreet_api.py
├── hacs.json
├── manifest.json
├── property_queries.py
└── sensor.py
```

### Support & Contributions 🤝

For issues, suggestions, or feature requests, please use the [GitHub issue tracker](https://github.com/harperreed/home-assistant-firststreet/issues). Your contributions are welcome! Feel free to open pull requests for enhancements or fixes.

Thank you for using the FirstStreet Integration! Let's help make our homes safer one sensor at a time! 🏡✨
