from typing import List, Dict

# Mock data representing conflicting policies from other departments
EXTERNAL_POLICIES: List[Dict[str, str]] = [
    {
        "department": "HMRC",
        "title": "VAT on Digital Services",
        "content": "You must charge VAT on all digital services supplied to UK consumers, regardless of your turnover. The threshold of £85,000 does NOT apply to digital services."
    },
    {
        "department": "Home Office",
        "title": "Right to Work Checks",
        "content": "From 1 October 2022, employers typically cannot use COVID-19 adjusted right to work checks. You must verify physical documents or use the online share code service."
    },
    {
        "department": "DWP",
        "title": "Universal Credit Capital Limits",
        "content": "If you have more than £16,000 in money, savings and investments, you are not eligible for Universal Credit."
    },
    {
        "department": "DEFRA",
        "title": "Fishing Rod Licenses",
        "content": "You need a rod fishing licence to fish for salmon, trout, freshwater fish, smelt or eel with a rod and line in England (except the River Tweed), Wales and the Border Esk region of Scotland."
    }
]
