# All-in-One Converter

A comprehensive unit converter application built with Python and Tkinter.

## Features

- **Currency Converter**: Real-time exchange rates (via API) with offline fallback
- **Weight Converter**: Metric and Imperial units (mg to tonne)
- **Length Converter**: Metric and Imperial units (mm to nautical mile)
- **Area Converter**: Square meters, acres, hectares, etc.
- **Temperature Converter**: Celsius, Fahrenheit, Kelvin
- **Themes**: Toggle between Light and Dark modes
- **Modern UI**: Clean interface with tabbed navigation

## Usage

```bash
python AIOConverter.py
```

## Dependencies

- `requests` (for currency rates)
- `tkinter` (built-in)

## Notes

- Currency rates are fetched from `exchangerate.host`
- If offline, the app uses cached or hardcoded fallback rates
