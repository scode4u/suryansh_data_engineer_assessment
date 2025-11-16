# import json
# import logging
# from typing import List, Dict, Any

# from pydantic import ValidationError

# from models import Property
# from utils import get_connection, init_db


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )

# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_PATH = os.path.join(BASE_DIR, "..", "data", "fake_property_data_new.json")


# def load_raw(path: str = DATA_PATH) -> List[Dict[str, Any]]:
#     """
#     Load raw JSON records from file.
#     Handles both normal JSON (list/dict) and line-delimited JSON.
#     """
#     try:
#         with open(path, "r") as f:
#             data = json.load(f)
#     except json.JSONDecodeError:
#         # Fall back to line-delimited JSON (one JSON object per line)
#         records: List[Dict[str, Any]] = []
#         with open(path, "r") as f:
#             for line in f:
#                 line = line.strip()
#                 if not line:
#                     continue
#                 records.append(json.loads(line))
#         return records

#     if isinstance(data, list):
#         return data
#     elif isinstance(data, dict):
#         # If it's a dict, just wrap in a list so we don't crash
#         return [data]
#     else:
#         raise ValueError("Unsupported JSON structure")


# def transform(records: List[Dict[str, Any]]):
#     """
#     Validate and normalize raw JSON into 4 logical tables.
#     Returns lists of dicts for each table.
#     """
#     property_rows: Dict[int, Dict[str, Any]] = {}
#     hoa_rows: List[Dict[str, Any]] = []
#     valuation_rows: List[Dict[str, Any]] = []
#     rehab_rows: List[Dict[str, Any]] = []

#     for raw in records:
#         try:
#             p = Property(**raw)
#         except ValidationError as e:
#             logging.warning("Skipping record due to validation error: %s", e)
#             continue

#         pid = p.property_id

#         # Base property row (dedup on property_id)
#         property_rows[pid] = {
#             "property_id": pid,
#             "address": p.address,
#             "city": p.city,
#             "state": p.state,
#             "zip_code": p.zip_code,
#             "sq_ft": p.sq_ft,
#             "bedrooms": p.bedrooms,
#             "bathrooms": p.bathrooms,
#         }

#         # HOA row
#         if p.hoa_fee is not None or p.hoa_contact:
#             hoa_rows.append(
#                 {
#                     "property_id": pid,
#                     "hoa_fee": p.hoa_fee,
#                     "hoa_contact": p.hoa_contact,
#                 }
#             )

#         # Valuation row
#         if p.avm_value is not None or p.market_value is not None:
#             valuation_rows.append(
#                 {
#                     "property_id": pid,
#                     "avm_value": p.avm_value,
#                     "avm_confidence": p.avm_confidence,
#                     "market_value": p.market_value,
#                 }
#             )

#         # Rehab row
#         if (
#             p.light_rehab_cost is not None
#             or p.medium_rehab_cost is not None
#             or p.heavy_rehab_cost is not None
#         ):
#             rehab_rows.append(
#                 {
#                     "property_id": pid,
#                     "light_rehab_cost": p.light_rehab_cost,
#                     "medium_rehab_cost": p.medium_rehab_cost,
#                     "heavy_rehab_cost": p.heavy_rehab_cost,
#                 }
#             )

#     return list(property_rows.values()), hoa_rows, valuation_rows, rehab_rows


# def load_to_db(properties, hoa, valuations, rehabs):
#     """
#     Insert normalized data into MySQL tables.
#     """
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Properties
#     if properties:
#         cursor.executemany(
#             """
#             INSERT INTO properties
#             (property_id, address, city, state, zip_code, sq_ft, bedrooms, bathrooms)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """,
#             [
#                 (
#                     r["property_id"],
#                     r["address"],
#                     r["city"],
#                     r["state"],
#                     r["zip_code"],
#                     r["sq_ft"],
#                     r["bedrooms"],
#                     r["bathrooms"],
#                 )
#                 for r in properties
#             ],
#         )

#     # HOA
#     if hoa:
#         cursor.executemany(
#             """
#             INSERT INTO hoa
#             (property_id, hoa_fee, hoa_contact)
#             VALUES (%s, %s, %s)
#             """,
#             [
#                 (r["property_id"], r["hoa_fee"], r["hoa_contact"])
#                 for r in hoa
#             ],
#         )

#     # Valuations
#     if valuations:
#         cursor.executemany(
#             """
#             INSERT INTO valuations
#             (property_id, avm_value, avm_confidence, market_value)
#             VALUES (%s, %s, %s, %s)
#             """,
#             [
#                 (
#                     r["property_id"],
#                     r["avm_value"],
#                     r["avm_confidence"],
#                     r["market_value"],
#                 )
#                 for r in valuations
#             ],
#         )

#     # Rehab Estimates
#     if rehabs:
#         cursor.executemany(
#             """
#             INSERT INTO rehab_estimates
#             (property_id, light_rehab_cost, medium_rehab_cost, heavy_rehab_cost)
#             VALUES (%s, %s, %s, %s)
#             """,
#             [
#                 (
#                     r["property_id"],
#                     r["light_rehab_cost"],
#                     r["medium_rehab_cost"],
#                     r["heavy_rehab_cost"],
#                 )
#                 for r in rehabs
#             ],
#         )

#     conn.commit()
#     cursor.close()
#     conn.close()


# def main():
#     logging.info("Initialising database / tables...")
#     init_db()

#     logging.info("Loading raw JSON from %s", DATA_PATH)
#     records = load_raw()

#     logging.info("Transforming %d records", len(records))
#     properties, hoa, valuations, rehabs = transform(records)

#     logging.info(
#         "Prepared %d properties, %d hoa, %d valuations, %d rehab rows",
#         len(properties),
#         len(hoa),
#         len(valuations),
#         len(rehabs),
#     )

#     logging.info("Loading into MySQL...")
#     load_to_db(properties, hoa, valuations, rehabs)
#     logging.info("ETL complete.")
    

# if __name__ == "__main__":
#     main()



import os
import json
import logging
import re
from typing import List, Dict, Any

from pydantic import ValidationError

from models import PropertyRecord
from utils import get_connection, init_db


# ---------- Logging setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Path to JSON file (relative to this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "fake_property_data_new.json")


def load_raw(path: str = DATA_PATH) -> List[Dict[str, Any]]:
    """
    Load raw JSON. Expects a top-level list of property objects.
    """
    logging.info("Loading raw JSON from %s", path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected top-level JSON array (list of properties)")

    logging.info("Loaded %d raw records", len(data))
    return data


def clean_sqft(sqft_str: Any) -> int | None:
    """
    SQFT_Total looks like '5649 sqft'. Extract numeric part.
    """
    if sqft_str is None:
        return None
    text = str(sqft_str)
    nums = re.findall(r"\d+", text)
    if not nums:
        return None
    return int(nums[0])


def transform(records: List[Dict[str, Any]]):
    """
    Transform raw JSON into normalized tables:
    - properties
    - valuation
    - hoa
    - rehab
    """
    property_rows: List[Dict[str, Any]] = []
    valuation_rows: List[Dict[str, Any]] = []
    hoa_rows: List[Dict[str, Any]] = []
    rehab_rows: List[Dict[str, Any]] = []

    property_id_counter = 1

    for raw in records:
        try:
            rec = PropertyRecord(**raw)
        except ValidationError as e:
            logging.warning("Skipping record due to validation error: %s", e)
            continue

        pid = property_id_counter
        property_id_counter += 1

        # properties table row
        property_rows.append(
            {
                "property_id": pid,
                "address": rec.Address,
                "city": rec.City,
                "state": rec.State,
                "zip_code": rec.Zip,
                "sqft_total": clean_sqft(rec.SQFT_Total),
                "bedrooms": rec.Bed,
                "bathrooms": rec.Bath,
                "year_built": rec.Year_Built,
                "latitude": rec.Latitude,
                "longitude": rec.Longitude,
            }
        )

        # valuation rows (one per item in Valuation list)
        for v in rec.Valuation:
            valuation_rows.append(
                {
                    "property_id": pid,
                    "list_price": v.List_Price,
                    "zestimate": v.Zestimate,
                    "arv": v.ARV,
                    "expected_rent": v.Expected_Rent,
                    "rent_zestimate": v.Rent_Zestimate,
                    "low_fmr": v.Low_FMR,
                    "high_fmr": v.High_FMR,
                    "redfin_value": v.Redfin_Value,
                    "previous_rent": v.Previous_Rent,
                }
            )

        # hoa rows
        for h in rec.HOA:
            hoa_rows.append(
                {
                    "property_id": pid,
                    "hoa_fee": h.HOA,
                    "hoa_flag": h.HOA_Flag,
                }
            )

        # rehab rows
        for r in rec.Rehab:
            rehab_rows.append(
                {
                    "property_id": pid,
                    "underwriting_rehab": r.Underwriting_Rehab,
                    "rehab_calculation": r.Rehab_Calculation,
                    "flooring_flag": r.Flooring_Flag,
                    "foundation_flag": r.Foundation_Flag,
                    "roof_flag": r.Roof_Flag,
                    "hvac_flag": r.HVAC_Flag,
                    "kitchen_flag": r.Kitchen_Flag,
                    "bathroom_flag": r.Bathroom_Flag,
                    "appliances_flag": r.Appliances_Flag,
                    "windows_flag": r.Windows_Flag,
                    "landscaping_flag": r.Landscaping_Flag,
                    "trashout_flag": r.Trashout_Flag,
                }
            )

    logging.info(
        "Transformed into %d properties, %d valuations, %d hoa, %d rehab rows",
        len(property_rows),
        len(valuation_rows),
        len(hoa_rows),
        len(rehab_rows),
    )

    return property_rows, valuation_rows, hoa_rows, rehab_rows


def load_to_db(properties, valuations, hoas, rehabs):
    """
    Insert transformed data into MySQL tables.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Properties
    if properties:
        cursor.executemany(
            """
            INSERT INTO properties
            (property_id, address, city, state, zip_code, sqft_total, bedrooms, bathrooms, year_built, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                (
                    r["property_id"],
                    r["address"],
                    r["city"],
                    r["state"],
                    r["zip_code"],
                    r["sqft_total"],
                    r["bedrooms"],
                    r["bathrooms"],
                    r["year_built"],
                    r["latitude"],
                    r["longitude"],
                )
                for r in properties
            ],
        )

    # Valuation
    if valuations:
        cursor.executemany(
            """
            INSERT INTO valuation
            (property_id, list_price, zestimate, arv, expected_rent, rent_zestimate,
             low_fmr, high_fmr, redfin_value, previous_rent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                (
                    r["property_id"],
                    r["list_price"],
                    r["zestimate"],
                    r["arv"],
                    r["expected_rent"],
                    r["rent_zestimate"],
                    r["low_fmr"],
                    r["high_fmr"],
                    r["redfin_value"],
                    r["previous_rent"],
                )
                for r in valuations
            ],
        )

    # HOA
    if hoas:
        cursor.executemany(
            """
            INSERT INTO hoa
            (property_id, hoa_fee, hoa_flag)
            VALUES (%s, %s, %s)
            """,
            [
                (
                    r["property_id"],
                    r["hoa_fee"],
                    r["hoa_flag"],
                )
                for r in hoas
            ],
        )

    # Rehab
    if rehabs:
        cursor.executemany(
            """
            INSERT INTO rehab
            (property_id, underwriting_rehab, rehab_calculation,
             flooring_flag, foundation_flag, roof_flag, hvac_flag, kitchen_flag,
             bathroom_flag, appliances_flag, windows_flag, landscaping_flag, trashout_flag)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                (
                    r["property_id"],
                    r["underwriting_rehab"],
                    r["rehab_calculation"],
                    r["flooring_flag"],
                    r["foundation_flag"],
                    r["roof_flag"],
                    r["hvac_flag"],
                    r["kitchen_flag"],
                    r["bathroom_flag"],
                    r["appliances_flag"],
                    r["windows_flag"],
                    r["landscaping_flag"],
                    r["trashout_flag"],
                )
                for r in rehabs
            ],
        )

    conn.commit()
    cursor.close()
    conn.close()


def main():
    logging.info("Initialising database / tables...")
    init_db()

    records = load_raw()

    logging.info("Transforming records...")
    properties, valuations, hoas, rehabs = transform(records)

    logging.info("Loading into MySQL...")
    load_to_db(properties, valuations, hoas, rehabs)

    logging.info("ETL complete.")


if __name__ == "__main__":
    main()
