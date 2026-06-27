# Smart-me for Home Assistant

![Smart-me logo](https://web.smart-me.com/wp-content/uploads/2023/07/smart-me_186×86.png)

A custom integration that connects [Smart-me](https://smart-me.com) energy meters to Home Assistant. It automatically discovers all devices linked to your Smart-me account and exposes their real-time measurements as sensors, updated every 60 seconds.

## Features

- Auto-discovers all Smart-me devices on your account
- Creates sensors for every available measurement per device: energy (total, tariffs, import/export), active power, voltage, current, power factor, temperature, and flow rate
- Energy sensors use `state_class: total_increasing` and are compatible with the Home Assistant Energy Dashboard
- Configured via the UI — no YAML required

## Installation

1. Copy the `custom_components/smart_me/` folder into your Home Assistant config directory under `custom_components/`.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **Smart-me**.
4. Enter your Smart-me account email and password.