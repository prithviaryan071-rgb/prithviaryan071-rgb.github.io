"""
PORTFOLIO COPY -- SALES INTELLIGENCE AGENT (prototype)
=====================================================
This is the working prototype of the sales intelligence agent I built at
Tricog Health. It is published here so the logic can be read end to end.

Company data has been removed: the live spreadsheet ID and tab references are
placeholders, and the built-in sample rows use invented manager, dealer and
customer names. The structure, column names and calculations are unchanged, so
the file still runs as-is on the sample data.
"""

"""
SME SALES INTELLIGENCE AGENT
============================
This bot reads your live "SME Intelligence Hub" Google Sheet and answers
sales-performance questions for ASMs: achievement vs target, gaps,
top dealers to lean on, and open leads.

HOW TO CONNECT YOUR REAL LIVE SHEET
------------------------------------
1. Open your Google Sheet in the browser.
2. Click Share -> "Anyone with the link" -> Viewer.
3. Copy the SHEET_ID from the URL:
   https://docs.google.com/spreadsheets/d/  <-- THIS PART -->  /edit
4. For each tab (OMS 2026, SME AOP 2026, Inside Sales Dashboard), open that
   tab and look at the URL end: ...#gid=123456789  <- copy that number too.
5. Paste the SHEET_ID and the three gids into the CONFIG section below.

Until you plug in your real sheet, this script runs on realistic SAMPLE DATA
(built into this file) so you can see the whole thing working end-to-end.
"""

import pandas as pd

# ============================================================
# CONFIG -- fill these in with your real sheet details later
# ============================================================
USE_LIVE_GOOGLE_SHEET = False   # runs on the built-in sample data
SHEET_ID = "YOUR_SHEET_ID_HERE"
GID_ORDERS = "YOUR_ORDERS_TAB_GID"
GID_TARGETS = "YOUR_TARGETS_TAB_GID"
GID_LEADS = "YOUR_LEADS_TAB_GID"

# Leads count as OPEN when their Status is anything EXCEPT these:
CLOSED_STATUSES = {"deferred", "won"}   # compared case-insensitively


# ============================================================
# STEP 1: LOAD DATA (live sheet OR sample data)
# ============================================================

def _sheet_csv_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"


def _normalize_month(series):
    """Your OMS sheet uses 'Jan-2026' (hyphen). Your AOP sheet uses 'Jan 2026'
    (space) as a COLUMN NAME. This turns any 'Jan 2026' / 'Jan-2026' /
    'Jan  2026' style text into one consistent form: 'Jan-2026'."""
    return (series.astype(str).str.strip()
            .str.replace(r"\s+", "-", regex=True))


def load_orders():
    if USE_LIVE_GOOGLE_SHEET:
        df = pd.read_csv(_sheet_csv_url(GID_ORDERS))
        df.columns = df.columns.str.strip()  # real sheet has stray spaces in headers
        df["Month"] = _normalize_month(df["Month"])
        for col in ["Qty", "H/W Rev", "Interpretation Rev"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df
    # ---- sample data, using your REAL column names ----
    return pd.DataFrame([
        {"Month": "Jan-2026", "ASM": "Rahul", "ZM": "Zone Manager South",
         "Type Of Segment": "SME", "Product": "VCARDIA", "Model Offered": "Basic",
         "Level Of Sale": "Secondary Sale", "CP Code": "DLR-001",
         "Dealer Involvement/Inside Sales": "Northline Medical", "Qty": 1,
         "H/W Rev": 16500, "Interpretation Rev": 0},
        {"Month": "Jan-2026", "ASM": "Rahul", "ZM": "Zone Manager South",
         "Type Of Segment": "SME", "Product": "VCARDIA", "Model Offered": "Ultimate",
         "Level Of Sale": "Secondary Sale", "CP Code": "DLR-002",
         "Dealer Involvement/Inside Sales": "Greenfield Medical Systems", "Qty": 1,
         "H/W Rev": 6000, "Interpretation Rev": 1000},
        {"Month": "Jan-2026", "ASM": "Rahul", "ZM": "Zone Manager South",
         "Type Of Segment": "Primary", "Product": "VCARDIA", "Model Offered": "NA",
         "Level Of Sale": "Primary Sale", "CP Code": "DLR-002",
         "Dealer Involvement/Inside Sales": "Greenfield Medical Systems", "Qty": 6,
         "H/W Rev": 189000, "Interpretation Rev": 0},
        {"Month": "Feb-2026", "ASM": "Rahul", "ZM": "Zone Manager South",
         "Type Of Segment": "SME", "Product": "VCARDIA", "Model Offered": "Basic",
         "Level Of Sale": "Secondary Sale", "CP Code": "DLR-001",
         "Dealer Involvement/Inside Sales": "Northline Medical", "Qty": 1,
         "H/W Rev": 1, "Interpretation Rev": 0},
        {"Month": "Jan-2026", "ASM": "Anita", "ZM": "Zone Manager North",
         "Type Of Segment": "SME", "Product": "VCARDIA", "Model Offered": "Basic",
         "Level Of Sale": "Secondary Sale", "CP Code": "DLR-003",
         "Dealer Involvement/Inside Sales": "Vertex Medical Devices", "Qty": 1,
         "H/W Rev": 1, "Interpretation Rev": 0},
    ])


def load_targets():
    if USE_LIVE_GOOGLE_SHEET:
        df = pd.read_csv(_sheet_csv_url(GID_TARGETS))
        df.columns = df.columns.str.strip()  # real sheet has stray spaces in headers
        # Month COLUMN NAMES like "Jan 2026" need to become "Jan-2026" too,
        # so they match the Month values used in the orders sheet.
        rename_map = {}
        for col in df.columns:
            if any(m in str(col) for m in
                   ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
                rename_map[col] = str(col).strip().replace(" ", "-")
        return df.rename(columns=rename_map)
    # ---- sample data, using your REAL column names ----
    return pd.DataFrame([
        {"ASM Name": "Rahul", "Product": "Secondary", "Jan-2026": 16, "Feb-2026": 16},
        {"ASM Name": "Rahul", "Product": "Basic", "Jan-2026": 8, "Feb-2026": 8},
        {"ASM Name": "Rahul", "Product": "Ultimate", "Jan-2026": 5, "Feb-2026": 5},
        {"ASM Name": "Rahul", "Product": "Advance", "Jan-2026": 3, "Feb-2026": 3},
        {"ASM Name": "Anita", "Product": "Secondary", "Jan-2026": 13, "Feb-2026": 15},
    ])


def load_leads():
    if USE_LIVE_GOOGLE_SHEET:
        df = pd.read_csv(_sheet_csv_url(GID_LEADS))
        df.columns = df.columns.str.strip()  # fixes 'CP Name ' -> 'CP Name'
        return df
    # ---- sample data, using your REAL Inside Sales tracker columns ----
    return pd.DataFrame([
        {"ASM": "Rahul Menon", "CP Name": "Northline Medical", "Status": "Deferred",
         "Customer Name": "Riverside Clinic"},
        {"ASM": "Rahul Menon", "CP Name": "Greenfield Medical Systems", "Status": "In Progress",
         "Customer Name": "Lakeside Diagnostics"},
        {"ASM": "Rahul Menon", "CP Name": "Northline Medical", "Status": "Won",
         "Customer Name": "Parkview Multi Speciality"},
        {"ASM": "Rahul Menon", "CP Name": "Greenfield Medical Systems", "Status": "Customer Delay",
         "Customer Name": "Meridian Labs"},
        {"ASM": "", "CP Name": "Blank Row Dealer", "Status": "In Progress",
         "Customer Name": "Should Be Ignored"},
        {"ASM": "Anita Sharma", "CP Name": "Vertex Medical", "Status": "Deferred",
         "Customer Name": "Hilltop Diagnostic Centre"},
        {"ASM": "Anita Sharma", "CP Name": "Vertex Medical", "Status": "Not Attended",
         "Customer Name": "Central Hospital"},
    ])


# ============================================================
# STEP 2: CORE COUNTING ENGINE (Section 4 of your spec)
# ============================================================

def units_achieved(orders, asm, month, segment_type=None, model=None, dealer=None):
    """The one filtering trick everything else is built from."""
    df = orders[(orders["ASM"] == asm) & (orders["Month"] == month)]
    if segment_type:
        df = df[df["Type Of Segment"] == segment_type]
    if model:
        df = df[df["Model Offered"] == model]
    if dealer:
        df = df[df["CP Code"] == dealer]
    return int(df["Qty"].sum())


def revenue_achieved(orders, asm, month, column, dealer=None):
    df = orders[
        (orders["ASM"] == asm) &
        (orders["Month"] == month) &
        (orders["Type Of Segment"].isin(["SME", "Primary"])) &
        (orders["Model Offered"].isin(["Basic", "Advance", "Ultimate", "NA", "AI + LVEF"]))
    ]
    if dealer:
        df = df[df["CP Code"] == dealer]
    return float(df[column].sum())


def primary_units(orders, asm, month):
    return units_achieved(orders, asm, month, segment_type="Primary")


def basic_units(orders, asm, month, dealer=None):
    return units_achieved(orders, asm, month, model="Basic", dealer=dealer)


def ultimate_units(orders, asm, month, dealer=None):
    return units_achieved(orders, asm, month, model="Ultimate", dealer=dealer)


def advance_units(orders, asm, month, dealer=None):
    return units_achieved(orders, asm, month, model="Advance", dealer=dealer)


def secondaries_total(orders, asm, month, dealer=None):
    return (basic_units(orders, asm, month, dealer)
            + ultimate_units(orders, asm, month, dealer)
            + advance_units(orders, asm, month, dealer))


def hardware_revenue(orders, asm, month, dealer=None):
    return revenue_achieved(orders, asm, month, "H/W Rev", dealer)


def ecg_pack_revenue(orders, asm, month, dealer=None):
    return revenue_achieved(orders, asm, month, "Interpretation Rev", dealer)


# ============================================================
# STEP 3: TARGETS + GAP
# ============================================================

def get_target(targets, asm, month, product="Secondary"):
    row = targets[(targets["ASM Name"] == asm) & (targets["Product"] == product)]
    if row.empty or month not in row.columns:
        return 0
    return float(row.iloc[0][month])


def gap_to_target(orders, targets, asm, month, product="Secondary"):
    target = get_target(targets, asm, month, product)
    if product == "Secondary":
        achieved = secondaries_total(orders, asm, month)
    elif product == "Basic":
        achieved = basic_units(orders, asm, month)
    elif product == "Ultimate":
        achieved = ultimate_units(orders, asm, month)
    elif product == "Advance":
        achieved = advance_units(orders, asm, month)
    else:
        achieved = 0
    return {"asm": asm, "month": month, "product": product,
            "target": target, "achieved": achieved, "gap": target - achieved}


# ============================================================
# STEP 4: DEALER RANKING (which dealers to lean on)
# ============================================================

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def months_from_jan_to(target_month):
    """Return every month from January up to and including target_month.
    e.g. 'Feb-2026' -> ['Jan-2026', 'Feb-2026']. January is always included."""
    try:
        abbr, year = target_month.split("-")
        idx = MONTH_ORDER.index(abbr)
    except (ValueError, IndexError):
        return [target_month]
    return [f"{MONTH_ORDER[i]}-{year}" for i in range(idx + 1)]


def top_dealers(orders, asm, months, top_n=3):
    """Rank an ASM's dealers by total secondary units over a list of months.
    Groups by the real dealer NAME (Dealer Involvement/Inside Sales), not the
    internal CP Code."""
    df = orders[(orders["ASM"] == asm) & (orders["Month"].isin(months))]
    ranked = (
        df[df["Model Offered"].isin(["Basic", "Ultimate", "Advance"])]
        .groupby("Dealer Involvement/Inside Sales")["Qty"].sum()
        .sort_values(ascending=False)
    )
    return ranked.head(top_n)


# ============================================================
# STEP 5: OPEN LEADS
# ============================================================

def open_leads_by_dealer(leads, asm):
    """Matches ASM names even when the leads sheet spells them slightly
    differently, e.g. Orders sheet has 'Anita' but Leads sheet has
    'Anita Sharma'. We match if either name starts with the other.
    A lead is OPEN when its Status is anything except 'Deferred' or 'Won'."""
    asm_lower = asm.strip().lower()
    leads_asm = leads["ASM"].fillna("").astype(str).str.strip().str.lower()
    mask = leads_asm.apply(lambda x: bool(x) and (x.startswith(asm_lower) or asm_lower.startswith(x)))
    mine = leads[mask]
    status = mine["Status"].fillna("").astype(str).str.strip().str.lower()
    open_only = mine[~status.isin(CLOSED_STATUSES)]
    return open_only.groupby("CP Name").size().sort_values(ascending=False)


# ============================================================
# STEP 6: SIMPLE Q&A FRONT END
# ============================================================

def ask(question, asm, month, orders, targets, leads):
    q = question.lower()

    if "gap" in q or "target" in q or "how am i doing" in q or "behind" in q:
        g = gap_to_target(orders, targets, asm, month, "Secondary")
        if g["gap"] <= 0:
            return (f"Great news {asm} — in {month} you achieved {g['achieved']} secondary "
                     f"units against a target of {g['target']}. You're ahead by {-g['gap']}!")
        return (f"{asm}, in {month} you've achieved {g['achieved']} secondary units "
                 f"against a target of {g['target']}. You're short by {g['gap']} units.")

    if "dealer" in q or "lean on" in q or "focus" in q or "which agent" in q:
        months = months_from_jan_to(month)  # Jan through the queried month, inclusive
        ranked = top_dealers(orders, asm, months)
        if ranked.empty:
            return f"No dealer sales found for {asm} from Jan through {month}."
        lines = [f"  - {name}: {qty} units" for name, qty in ranked.items()]
        return f"Top dealers for {asm} to lean on (Jan-{month}):\n" + "\n".join(lines)

    if "open lead" in q or "pending" in q or "pipeline" in q:
        leads_by_dealer = open_leads_by_dealer(leads, asm)
        if leads_by_dealer.empty:
            return f"{asm} has no open leads right now. Clean pipeline!"
        lines = [f"  - {cp}: {count} open lead(s)" for cp, count in leads_by_dealer.items()]
        return f"Open leads for {asm}, by dealer:\n" + "\n".join(lines)

    return ("I can answer questions about: your gap to target, which dealers to lean on, "
            "and your open leads. Try asking one of those!")


# ============================================================
# DEMO RUN
# ============================================================

if __name__ == "__main__":
    orders = load_orders()
    targets = load_targets()
    leads = load_leads()

# ============================================================
# INTERACTIVE RUN -- asks you for the ASM name and month each time
# ============================================================

if __name__ == "__main__":
    orders = load_orders()
    targets = load_targets()
    leads = load_leads()

    print("=" * 60)
    print("SME AGENT -- type an ASM name and a month to check them.")
    print("Month format example: Jan-2026, Feb-2026, Mar-2026")
    print("Type 'quit' as the ASM name to exit.")
    print("=" * 60)

    while True:
        ASM = input("\nASM name: ").strip()
        if ASM.lower() == "quit":
            break
        MONTH = input("Month (e.g. Jan-2026): ").strip()

        print("\nQ: How am I doing against my target?")
        print("A:", ask("how am i doing against my target", ASM, MONTH, orders, targets, leads))

        print("\nQ: Which dealers should I lean on?")
        print("A:", ask("which dealers should I lean on", ASM, MONTH, orders, targets, leads))

        print("\nQ: What open leads do I have?")
        print("A:", ask("what open leads do i have", ASM, MONTH, orders, targets, leads))

        print("\n" + "-" * 60)
        print("Raw numbers, for sanity-checking against the sheet by hand:")
        print("-" * 60)
        print("Primary units:", primary_units(orders, ASM, MONTH))
        print("Basic units:", basic_units(orders, ASM, MONTH))
        print("Ultimate units:", ultimate_units(orders, ASM, MONTH))
        print("Advance units:", advance_units(orders, ASM, MONTH))
        print("Secondaries total:", secondaries_total(orders, ASM, MONTH))
        print("Hardware revenue:", hardware_revenue(orders, ASM, MONTH))
        print("ECG pack revenue:", ecg_pack_revenue(orders, ASM, MONTH))

    print("\nGoodbye!")
