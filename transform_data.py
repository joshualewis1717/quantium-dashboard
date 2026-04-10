import os, pandas as pd

def load_and_transform_data(data_dir: str) -> pd.DataFrame:
    frames = []

    for file_name in sorted(os.listdir(data_dir)):
        if not file_name.endswith(".csv"):
            continue

        df = pd.read_csv(f"{data_dir}/{file_name}")

        pink_morsel_rows = df[df["product"].str.lower() == "pink morsel"].copy()
        pink_morsel_rows["price"] = pink_morsel_rows["price"].replace(r"[$,]", "", regex=True).astype(float)
        pink_morsel_rows["Sales"] = pink_morsel_rows["price"] * pink_morsel_rows["quantity"]

        frames.append(pink_morsel_rows[["Sales", "date", "region"]])

    combined = pd.concat(frames, ignore_index=True)
    return combined.rename(columns={"date": "Date", "region": "Region"})


def main() -> None:
    combined_data = load_and_transform_data("data")
    combined_data.to_csv("output.csv", index=False)

    print(f"Wrote {len(combined_data)} rows to output.csv")


if __name__ == "__main__":
    main()