import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://yruwsicscttnphjvrjhc.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)