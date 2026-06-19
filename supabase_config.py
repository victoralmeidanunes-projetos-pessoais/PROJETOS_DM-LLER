from supabase import create_client

SUPABASE_URL = "https://yruwsicscttnphjvrjhc.supabase.co"

SUPABASE_KEY = "sb_publishable_cMclO4izvQ1jzD3TzXXzGg_lSKDMsod"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)