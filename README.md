# TradeAnalyzer PyQt

## Description

This desktop application use to analyzing text file which output from XQ trading platform.

- Supports multi-report analysis.
- Supports compare with benchmark performance.

**This project is no longer maintained and may contain some bugs.**

## Development

### Install PDM Package Manager

```powershell
# Windows
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -

# Ubuntu
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```

### Install Project Dependencies

```powershell
pdm install
```

## Run App

```powershell
pdm run start
```

## License

This project is licensed under the [GNU General Public License (GPL) version 3.0 or later](LICENSE), see the [LICENSE](LICENSE) file for details.
