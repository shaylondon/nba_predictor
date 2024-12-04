# nba_predictive_model
This model accesses [NBA.com](https://www.nba.com/stats) official stats and uses them to leverage stat predictions.

# Getting Started
`nba_api`, `pandas`, `requests`, `tabulate` required.

```bash
pip install nba_api pandas requests tabulate
```
To run:
```bash
python predictors/driver.py
```
## NBA API
This model uses Swar Patel's [`nba_api`](https://github.com/swar/nba_api) API Client.

This package is Open Source with an [MIT License](https://github.com/swar/nba_api/blob/master/LICENSE).

### NBA.com

NBA.com has a [Terms of Use](https://www.nba.com/termsofuse) regarding the use of the NBA’s digital platforms.

### Justification of Models
Four Factors weights determined [here](https://squared2020.com/2017/09/05/introduction-to-olivers-four-factors/)

## LICENSE
[MIT License](https://github.com/shaylondon/nba_predictive_model/blob/main/LICENSE)