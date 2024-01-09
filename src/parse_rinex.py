from pathlib import Path
import georinex as gr


file = Path('data/DGLS00NOR_S_20240081100_01H_GN.rnx.gz')
file2 = Path('data/BERC00NOR_S_20240081100_01H_GN.rnx.gz')
# file2 = Path('data/test.rnx')
# data = file.read_text()
# file2.write_text('\n'.join(data.split('\n')[:200]))

dat = gr.load(file)
df = dat.to_dataframe()
pos = gr.keplerian2ecef(dat)
dat2 = gr.load(file2)
df2 = dat2.to_dataframe()
print(df)
print(df2)
print(df == df2)
here=True
