import pandas as pd


def main():
    df = pd.read_csv(
        r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\_v23\v23\Q_triangles_with_centers_Z2_S3_fiber6.csv"
    )
    print("Unique values in 's3_type_startsheet0':")
    print(df["s3_type_startsheet0"].value_counts())
    print()
    print("Sample values:")
    for val in df["s3_type_startsheet0"].unique()[:20]:
        print(f"  {repr(val)}")


if __name__ == "__main__":
    main()
