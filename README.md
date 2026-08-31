# Beach Day API for Home Assistant

A Home Assistant custom integration for [Beach Day API](https://beachdayapi.com/).

## Features

Configure a Beach Day API key and beach ID to create sensors for the latest beach score, water temperature, and air temperature. The integration polls the cloud API hourly and includes beach location details as entity attributes.

## Installation through HACS

1. Install [HACS](https://www.hacs.xyz/docs/use/).
2. In HACS, open **Integrations**, select the three-dot menu, and choose **Custom repositories**.
3. Add `https://github.com/rv888/home-assistant-beachday` with category **Integration**.
4. Install **Beach Day API** and restart Home Assistant.
5. Add the integration from **Settings → Devices & services → Add integration**.
6. Enter your Beach Day API key and numeric beach ID.

An API key is required. Usage is subject to the [Beach Day API terms](https://beachdayapi.com/terms/).

## Development

The integration lives in `custom_components/beachday`. Run the Python tests with `pytest` and validate the repository with HACS and Home Assistant `hassfest` checks in GitHub Actions.

## Support

Open an issue at https://github.com/rv888/home-assistant-beachday/issues.
