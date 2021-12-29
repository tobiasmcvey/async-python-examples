import asyncio
import time
import pandas as pd

def extract(file):
    dtype_dict = {"Nr": "int",
                  "Kommunenavn": "string",
                  "Adm. senter": "string",
                  "Fylke": "category",
                  "Målform": "category",
                  "Domene": "string"
                  }
    df = pd.read_csv(file, dtype=dtype_dict,low_memory=False)
    return df

async def transform(df):
    df["Lenke"] = "https://" + df["Domene"]
    await load(df)

async def load(tdf):
    tdf.to_csv("kommuner_lenker.csv", index=False)
    await asyncio.sleep(0)

async def main():
    pd.set_option("mode.chained_assignment", None)
    file = "https://raw.githubusercontent.com/tobiasmcvey/kommunale-nettsider/main/kommuner.csv"
    df = extract(file)
    chunk_size = int(df.shape[0] / 4)
    for start in range(0, df.shape[0], chunk_size):
        df_subset = df.iloc[start:start + chunk_size]
        x = asyncio.create_task(transform(df_subset))
        await x

start = time.time()
asyncio.run(main())
end=time.time()-start
print("execution time {} sec".format(end))
