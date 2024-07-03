Hi Taavo,

I have loaded the data into the `cbi_dev` database under the name `dlbiadvdanltcs.weekly_ds_us`.

Jason provided the join keys to `SRM_MODEL_DATA`:
- `summarydate` and `intalias` from the blended utilization data
- `caldt_k` and `fibenode` from the SRM model data

Initially, I noticed some duplicates, as shown below.

Additionally, the join keys provided appear to be different. The node codes from the utilization data vary: some records have multiple nodes either concatenated, separated by commas, or by slashes.

Here are the details provided about the data:
- The data represents node utilization for the prior week. For example, the record dated `'2024-01-07'` reflects the node utilization from `'2023-12-31'` to `'2024-01-07'`

At this point, I'm unsure how to join the data correctly. Could you provide some guidance on this?
