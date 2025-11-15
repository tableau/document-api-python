import argparse
import sys
from tableaudocumentapi.query import Query

def main():
    parser = argparse.ArgumentParser(
        description="Compare two Tableau workbooks (.twb or .twbx) and output their differences."
    )
    parser.add_argument("--wb1", help="Path to first workbook file")
    parser.add_argument("--wb2", help="Path to second workbook file")
    parser.add_argument("--out", default="df_diff.csv", help="Output CSV file (default: df_diff.csv)")
    parser.add_argument("--wb1-str", help="Raw XML string for first workbook")
    parser.add_argument("--wb2-str", help="Raw XML string for second workbook")

    args = parser.parse_args()

    # Determine which mode to use
    if args.wb1 and args.wb2:
        df = Query.compare_diffs(args.wb1, args.wb2)
    elif args.wb1_str and args.wb2_str:
        df = Query.compare_diffs(
            wb1_filename=None, wb2_filename=None,
            wb1_twb_string=args.wb1_str, wb2_twb_string=args.wb2_str
        )
    else:
        sys.exit("❌ You must provide either both --wb1/--wb2 or both --wb1-str/--wb2-str.")

    df.to_csv(args.out, index=False)
    print(f"✅ Diff written to {args.out}")
