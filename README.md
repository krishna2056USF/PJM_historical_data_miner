PJM Historical Data Miner
The PJM Historical Data Miner is used to retrieve PJM's historical data.

Example Usage
To fetch various types of historical data from PJM, use the following commands:

Example Usage
python fetch_pjm.py -u gen_by_fuel -o dataset/gen_by_fuel.csv\n
python fetch_pjm.py -u hrl_load_metered -o dataset/hrl_load_metered.csv
python fetch_pjm.py -u rt_hrl_lmps -o dataset/rt_hrl_lmps.csv
Replace the -u argument with the desired data URL key and the -o argument with the output file path to store the retrieved data.
