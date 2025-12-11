Underfloor Heating Output Quadratic Equation
============================================

This project provides tools for analyzing and predicting the heat output of underfloor heating (UFH) systems using quadratic curve fitting. It is based on data from the MCS heat pump calculator and supports flexible queries for different floor coverings, pipe spacings, and temperatures.


Files
-----

* `mcs-solid-16mm-table.csv`: This CSV contains values from the MCS Calculator (Excel 1.10) for a 16mm pipe in a solid floor
* `ufh_quadratic_calc.py`: This python script works out a quadratic equation that fits the MCS data
* `test_calc_output.py`: Tests the quadratic equation results against tests case values from MCS


Setup
-----

It is recommended to use venv to install the python dependencies:

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


Floor Coverings
---------------

| R (m²·K/W) | Rough tog | Example floor coverings                                         |
|-----------:|-----------|-----------------------------------------------------------------|
| 0.00       | 0.0 tog   | Bare screed; thin ceramic/stone tiles                           |
| 0.05       | 0.5 tog   | Thin vinyl / LVT; laminate                                      |
| 0.10       | 1.0 tog   | ~10–12 mm engineered wood glued down; low-tog carpet + underlay |
| 0.15       | 1.5 tog   | Thicker engineered wood or parquet; typical carpet + underlay   |

