Hi Taavo,

I have loaded the data into the `cbi_dev` database under the name `dlbiadvdanltcs.weekly_ds_us`.

Jason provided the join keys to `SRM_MODEL_DATA`:
- `summarydate` and `intalias` from the blended utilization data
- `caldt_k` and `fibenode` from the SRM model data

Initially, I noticed some duplicates, as shown below.

Additionally, the join keys provided appear to be different. The node codes from the utilization data vary: some records have multiple nodes either concatenated, separated by commas, or by slashes.

