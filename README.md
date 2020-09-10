# covid-demographic-data

## Installation

If using `conda`:

```
conda env create -f environment.yml
conda activate covid
```

If using `venv` and `pip`:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

If using neither, make sure you have the packages listed in `requirements.txt` installed in your Python environment.

## State Data Formatters

For all states in our dataset, we need a formatter that reads the raw data from [obastani/covid19demographics](https://github.com/obastani/covid19demographics) and extracts the age-group panel data. When a formatter has been written, add it to the `code/formatters.py` file and the `state_functions` dictionary therein. See the current file for formatters that have already been complete.

To get a sense of what a formatting function should do, refer to `notebooks/SampleCode.ipynb`. In brief, formatters take the raw json (e.g., `raw_json["USA"]["AL"]`) for a given state and 
return a timeseries of either cases/deaths, with any duplicate or missing dates removed. 

Columns should be formatted as "{low}-{high}", for each age bucket reported. Because states have changed their reporting buckets over time, dates with a missing entry for that particular bucket should be filled with `NaN`. The index of the returned dataframe should be the date in `datetime.date` format (not `datetime.datetime`).

Example data below:

```python
AL_formatter(raw_json["USA"]["AL"]).head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0-4</th>
      <th>18-24</th>
      <th>25-49</th>
      <th>5-17</th>
      <th>50-64</th>
      <th>65-100</th>
      <th>unknown</th>
      <th>5-24</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-06-29</th>
      <td>617.0</td>
      <td>NaN</td>
      <td>15123.0</td>
      <td>NaN</td>
      <td>7624.0</td>
      <td>6510.0</td>
      <td>272.0</td>
      <td>6536.0</td>
    </tr>
    <tr>
      <th>2020-06-30</th>
      <td>639.0</td>
      <td>NaN</td>
      <td>15606.0</td>
      <td>NaN</td>
      <td>7817.0</td>
      <td>6638.0</td>
      <td>31.0</td>
      <td>6805.0</td>
    </tr>
    <tr>
      <th>2020-07-01</th>
      <td>653.0</td>
      <td>NaN</td>
      <td>15984.0</td>
      <td>NaN</td>
      <td>7986.0</td>
      <td>6787.0</td>
      <td>29.0</td>
      <td>7003.0</td>
    </tr>
    <tr>
      <th>2020-07-02</th>
      <td>677.0</td>
      <td>NaN</td>
      <td>16457.0</td>
      <td>NaN</td>
      <td>8208.0</td>
      <td>6957.0</td>
      <td>28.0</td>
      <td>7277.0</td>
    </tr>
    <tr>
      <th>2020-07-03</th>
      <td>712.0</td>
      <td>NaN</td>
      <td>17178.0</td>
      <td>NaN</td>
      <td>8497.0</td>
      <td>7196.0</td>
      <td>65.0</td>
      <td>7714.0</td>
    </tr>
  </tbody>
</table>