from pathlib import Path
import georinex as gr


file = Path(
    "/workspaces/pose_est/data/cache/rnx3/1hour/1sec/2024/008/BATC/BATC00NOR_S_20240081100_01H_GN.rnx.gz"
)


dat = gr.load(file)
df = dat.to_dataframe()
pos = gr.keplerian2ecef(dat)
print(df)
