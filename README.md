\# AIS Vessel Analysis



A Python project for processing and analyzing AIS (Automatic Identification System) vessel data.



The project focuses on privacy-aware preprocessing, vessel trajectory analysis, travelled-distance calculations, fleet-level statistics, visualization, automated testing, and continuous integration with GitHub Actions.



\## Features



\- AIS data loading from Parquet files

\- Privacy-aware vessel anonymization

\- AIS data cleaning and validation

\- Vessel trajectory extraction

\- Time-gap detection

\- Vessel trajectory visualization

\- Haversine distance calculation in nautical miles

\- Handling of simultaneous AIS observations from multiple data sources

\- Fleet-level vessel statistics

\- Automated tests with pytest

\- GitHub Actions continuous integration

\- Reusable command-line analysis example



\## Project Structure



```text

ais-vessel-analysis/

│

├── .github/

│   └── workflows/

│       └── tests.yml

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── anonymize.py

│   ├── clean\_data.py

│   ├── trajectory.py

│   ├── vessel\_summary.py

│   └── visualize.py

│

├── tests/

│   ├── conftest.py

│   ├── test\_anonymize.py

│   ├── test\_clean\_data.py

│   ├── test\_trajectory.py

│   └── test\_vessel\_summary.py

│

├── example\_analysis.py

├── requirements.txt

├── .gitignore

└── README.md
## Example Output

Running:

```bash
python example_analysis.py "path/to/ais_data.parquet"
Summary for vessel_059
messages: 17711
start_time: 2023-01-01 00:01:55
end_time: 2023-01-01 23:59:29
avg_speed: 19.150251256281404
max_speed: 35.9

Total distance travelled: 216.73 nautical miles
### Top vessels by distance

The fleet summary also ranks anonymized vessels by total distance travelled:

| vessel_id | messages | mean_reported_sog | total_distance_nm | distance_avg_speed |
|---|---:|---:|---:|---:|
| vessel_059 | 17711 | 19.150251 | 216.734909 | 9.045907 |
| vessel_047 | 8788 | 7.757283 | 157.990518 | 6.596452 |
| vessel_034 | 11021 | 4.569322 | 106.799565 | 4.450548 |
| vessel_026 | 15251 | 8.914215 | 96.794397 | 4.033333 |
| vessel_035 | 4218 | 3.319132 | 87.399820 | 3.643304 |

## Publications

Relevant publications on AIS-based maritime data analysis:

1. **Exploring Recent Maritime Research on AIS-Based Ship Behavior Analysis and Modeling**  
   Duka, A., Zhang, H., Vidan, P., & Li, G. (2026).  
   *Journal of Marine Science and Engineering*, 14(8), 712.  
   [DOI](https://doi.org/10.3390/jmse14080712) | [Publisher](https://www.mdpi.com/2077-1312/14/8/712)

2. **Fishing Ground Identification and Activity Analysis Based on AIS Data**  
   Duka, A., Tian, W., Zhang, H., Vidan, P., & Li, G. (2026).  
   *Future Transportation*, 6(1), 34.  
   [DOI](https://doi.org/10.3390/futuretransp6010034) | [Publisher](https://www.mdpi.com/2673-7590/6/1/34)

3. **AIS-Based Analysis of Passenger Vessel Traffic and Emissions in Coastal Norway**  
   Duka, A., Zhang, H., Vidan, P., & Li, G. (2026).  
   *Logistics*, 10(9), 209.  
   [DOI](https://doi.org/10.3390/logistics10090209) | [Publisher](https://www.mdpi.com/2305-6290/10/9/209)