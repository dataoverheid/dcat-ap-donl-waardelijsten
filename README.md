# waardelijsten.dcat-ap-donl.nl

Source: [github.com/dataoverheid/dcat-ap-donl-waardelijsten](https://github.com/dataoverheid/dcat-ap-donl-waardelijsten)

## requirements

- Python 3.x
- Python-PIP
- Virtualenv

See the `requirements.txt` file for specific `pip` dependencies.

## installation

Execute the following commands in a terminal of choice.

```shell script
git clone --single-branch --branch master 'git@github.com:dataoverheid/dcat-ap-donl-waardelijsten.git'
virtualenv dcat-ap-donl-waardelijsten/venv
source dcat-ap-donl-waardelijsten/venv/bin/activate
python -m pip install -r dcat-ap-donl-waardelijsten/requirements.txt --no-cache-dir
```

Now configure the following scheduled task, the example below uses crontab. The goal is to execute the command daily at 23:00 (CET).

```shell script
0 23 * * * * (cd /path/to/dcat-ap-donl-waardelijsten && ./venv/bin/python src/waardelijsten_updater.py /var/www/waardelijsten.dcat-ap-donl.nl)
```

Now configure your webserver to serve the `public/` directory.
