# Excel SQL Runner

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DougTrajano_excel-sql-runner&metric=alert_status)](https://sonarcloud.io/dashboard?id=DougTrajano_excel-sql-runner)
![GitHub](https://img.shields.io/github/license/DougTrajano/excel-sql-runner)

A data app that allows you to run SQL in excel files. :)

You can create tables in a temporary database to aggregate, joins and all transformation available in SQL.

## Data Privacy

No data will be transferred outside the application when executed locally.

If you use the instantiated application, the data will be transferred and temporarily stored on the server.

This [application](https://share.streamlit.io/dougtrajano/excel-sql-runner/main/main.py) and the source code is a hobby project and have no warranties in this use.

## Installation

### Docker

To run **Excel SQL Runner** via Docker, just type:

```
docker run -d -p 8501:8501 --name excel-sql-runner dougtrajano/excel-sql-runner
```

### Locally

To run **Excel SQL Runner** locally.

1. Clone this repository.

```
git clone https://github.com/DougTrajano/excel-sql-runner.git
```

2. Open project folder:

```
cd excel-sql-runner
```

3. Install requirements:

```
pip install -r requirements.txt
```

4. Launch application:

```
streamlit run main.py
```

## Can I see a demo?

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dougtrajano/excel-sql-runner/main/main.py)

## Changelogs

See the [changelog](CHANGELOG.md) for a history of notable changes to this project.

## License

See [LICENSE](LICENSE) for details.

## Do you like this project?

<a href="https://www.buymeacoffee.com/dougtrajano" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="180" height="50" ></a>
