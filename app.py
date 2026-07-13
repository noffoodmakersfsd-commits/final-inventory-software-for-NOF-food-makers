import streamlit as st
import pandas as pd
import database
import engine
import os
import json
from PIL import Image
import io
import base64

# Page configurations for a premium industrial look
st.set_page_config(
    page_title="NOF Food Makers Pvt Ltd", 
    page_icon="🏭", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure DB initialization gets triggered
if 'db_initialized' not in st.session_state:
    database.init_db()
    st.session_state.db_initialized = True

# Logo Settings File
LOGO_SETTINGS_FILE = "logo_settings.json"

# Default logo settings
DEFAULT_LOGO_SETTINGS = {
    "size": 80,
    "rotation": 0,
    "position_x": 0,
    "position_y": 0,
    "border_radius": 50,
    "border_width": 3,
    "opacity": 1.0
}

def load_logo_settings():
    """Load logo settings from JSON file"""
    if os.path.exists(LOGO_SETTINGS_FILE):
        try:
            with open(LOGO_SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_LOGO_SETTINGS.copy()
    return DEFAULT_LOGO_SETTINGS.copy()

def save_logo_settings(settings):
    """Save logo settings to JSON file"""
    with open(LOGO_SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def get_logo_path():
    """Get existing logo path"""
    for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']:
        if os.path.exists(f"logo{ext}"):
            return f"logo{ext}"
    return None

def image_to_base64(img):
    """Convert PIL Image to base64"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Load logo settings - GLOBAL SCOPE
logo_settings = load_logo_settings()

# ==========================================
# LOGO EDITOR FUNCTION
# ==========================================

def logo_editor():
    """Logo Editor Modal - Edit logo settings"""
    global logo_settings
    
    logo_path = get_logo_path()
    
    with st.expander("✏️ Edit Logo Settings", expanded=False):
        st.markdown("### 🎨 Logo Editor")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if logo_path:
                try:
                    img = Image.open(logo_path)
                    preview_img = img.copy()
                    preview_size = 120
                    preview_img = preview_img.resize((preview_size, preview_size))
                    
                    if logo_settings['rotation'] != 0:
                        preview_img = preview_img.rotate(logo_settings['rotation'], expand=True)
                    
                    st.image(preview_img, width=preview_size)
                    st.caption("Current Preview")
                except:
                    st.info("📷 No logo loaded")
            else:
                st.info("📷 No logo uploaded")
        
        with col2:
            st.markdown("#### 📤 Upload New Logo")
            uploaded_file = st.file_uploader(
                "Choose an image...", 
                type=['png', 'jpg', 'jpeg', 'webp', 'svg'],
                key="logo_uploader"
            )
            if uploaded_file is not None:
                with open("logo.png", "wb") as f:
                    f.write(uploaded_file.getvalue())
                st.success("✅ Logo uploaded! Reloading...")
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### 🔧 Adjust Logo Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            new_size = st.slider(
                "Size (px)", 
                min_value=30, 
                max_value=200, 
                value=logo_settings['size'],
                step=5,
                key="logo_size"
            )
            
            new_rotation = st.slider(
                "Rotation (°)", 
                min_value=-180, 
                max_value=180, 
                value=logo_settings['rotation'],
                step=5,
                key="logo_rotation"
            )
            
            new_border_radius = st.slider(
                "Roundness (%)", 
                min_value=0, 
                max_value=50, 
                value=logo_settings['border_radius'],
                step=5,
                key="logo_border_radius"
            )
        
        with col2:
            new_pos_x = st.slider(
                "Horizontal Position", 
                min_value=-50, 
                max_value=50, 
                value=logo_settings['position_x'],
                step=2,
                key="logo_pos_x"
            )
            
            new_pos_y = st.slider(
                "Vertical Position", 
                min_value=-50, 
                max_value=50, 
                value=logo_settings['position_y'],
                step=2,
                key="logo_pos_y"
            )
            
            new_border_width = st.slider(
                "Border Width", 
                min_value=0, 
                max_value=10, 
                value=logo_settings['border_width'],
                step=1,
                key="logo_border_width"
            )
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("💾 Save Settings", use_container_width=True):
                logo_settings['size'] = new_size
                logo_settings['rotation'] = new_rotation
                logo_settings['border_radius'] = new_border_radius
                logo_settings['position_x'] = new_pos_x
                logo_settings['position_y'] = new_pos_y
                logo_settings['border_width'] = new_border_width
                save_logo_settings(logo_settings)
                st.success("✅ Settings saved! Refreshing...")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset Defaults", use_container_width=True):
                save_logo_settings(DEFAULT_LOGO_SETTINGS.copy())
                logo_settings = load_logo_settings()
                st.success("🔄 Reset to defaults! Refreshing...")
                st.rerun()
        
        with col3:
            if logo_path and st.button("🗑️ Delete Logo", use_container_width=True):
                try:
                    os.remove(logo_path)
                    st.success("🗑️ Logo deleted!")
                    st.rerun()
                except:
                    st.error("Could not delete logo")

# Premium CSS Styling with Logo Overlay
st.markdown(f"""
    <style>
    .main {{ background-color: #f8f9fa; }}
    div[data-testid="stMetricValue"] {{ font-size: 32px; font-weight: 700; color: #1e3d59; }}
    div[data-testid="stMetricLabel"] {{ font-size: 14px; font-weight: 600; color: #5c6b73; }}
    .stButton>button, .stDownloadButton>button {{ 
        border-radius: 6px; 
        font-weight: bold; 
        background-color: #1e3d59 !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{
        background-color: #2a5298 !important;
        transform: scale(1.02);
    }}
    div.stDownloadButton > button {{
        background-color: #2e7d32 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
    }}
    
    .company-header {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 15px 0;
        border-bottom: 3px solid #1e3d59;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        position: relative;
        transition: all 0.3s ease;
    }}
    .company-header .logo-container {{
        display: flex;
        align-items: center;
        gap: 20px;
        position: relative;
    }}
    .company-header .logo-text h1 {{
        color: #1e3d59;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    .company-header .logo-text p {{
        color: #5c6b73;
        font-size: 14px;
        margin: 5px 0 0 0;
        letter-spacing: 2px;
        font-weight: 500;
    }}
    .company-header .logo-wrapper {{
        position: relative;
        display: inline-block;
        border-radius: {logo_settings['border_radius']}%;
        border: {logo_settings['border_width']}px solid #1e3d59;
        padding: 5px;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        transform: translate({logo_settings['position_x']}px, {logo_settings['position_y']}px);
    }}
    .company-header .logo-wrapper:hover {{
        transform: translate({logo_settings['position_x']}px, {logo_settings['position_y']}px) scale(1.05);
        box-shadow: 0 6px 25px rgba(0,0,0,0.25);
    }}
    .company-header .logo-wrapper img {{
        border-radius: {logo_settings['border_radius']}%;
        width: {logo_settings['size']}px;
        height: {logo_settings['size']}px;
        object-fit: cover;
        transform: rotate({logo_settings['rotation']}deg);
        transition: all 0.3s ease;
    }}
    .company-header .logo-wrapper .edit-icon {{
        position: absolute;
        bottom: -8px;
        right: -8px;
        background: #1e3d59;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        border: 2px solid white;
        z-index: 10;
    }}
    .company-header .logo-wrapper .edit-icon:hover {{
        transform: scale(1.15);
        background: #2a5298;
    }}
    
    .watermark-logo {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        opacity: 0.08;
        z-index: 999;
        pointer-events: none;
        width: 150px;
        height: auto;
        filter: grayscale(100%);
        transform: rotate({logo_settings['rotation']}deg);
    }}
    
    .sidebar-brand {{
        text-align: center;
        padding: 10px 0;
        border-bottom: 2px solid #1e3d59;
        margin-bottom: 15px;
    }}
    .sidebar-brand h3 {{
        color: #1e3d59;
        font-size: 16px;
        font-weight: 700;
        margin: 5px 0 0 0;
    }}
    .sidebar-brand p {{
        color: #5c6b73;
        font-size: 11px;
        margin: 2px 0 0 0;
    }}
    .sidebar-brand .mini-logo {{
        border-radius: 50%;
        border: 2px solid #1e3d59;
        padding: 3px;
        background: white;
        width: 50px;
        height: 50px;
        object-fit: cover;
        margin: 0 auto;
        display: block;
    }}
    
    .content-card {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# COMPANY HEADER WITH LOGO
# ==========================================

logo_path = get_logo_path()

if logo_path:
    try:
        img = Image.open(logo_path)
        img_header = img.copy()
        img_header = img_header.resize((logo_settings['size'], logo_settings['size']))
        
        if logo_settings['rotation'] != 0:
            img_header = img_header.rotate(logo_settings['rotation'], expand=True)
        
        img_b64 = image_to_base64(img_header)
        
        img_watermark = img.copy()
        img_watermark = img_watermark.resize((200, 200))
        if logo_settings['rotation'] != 0:
            img_watermark = img_watermark.rotate(logo_settings['rotation'], expand=True)
        watermark_b64 = image_to_base64(img_watermark)
        
        st.markdown(f"""
        <div class="company-header">
            <div class="logo-container">
                <div class="logo-wrapper">
                    <img src="data:image/png;base64,{img_b64}" alt="NOF Logo"/>
                    <div class="edit-icon">✏️</div>
                </div>
                <div class="logo-text">
                    <h1>🏭 NOF FOOD MAKERS Pvt Ltd</h1>
                    <p>Smart Factory Management System</p>
                </div>
            </div>
        </div>
        <img src="data:image/png;base64,{watermark_b64}" class="watermark-logo" alt="NOF Logo Watermark"/>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown("""
        <div class="company-header">
            <div class="logo-container">
                <div class="logo-text">
                    <h1>🏭 NOF FOOD MAKERS Pvt Ltd</h1>
                    <p>Smart Factory Management System</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="company-header">
        <div class="logo-container">
            <div class="logo-text">
                <h1>🏭 NOF FOOD MAKERS Pvt Ltd</h1>
                <p>Smart Factory Management System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📤 Upload Company Logo", expanded=False):
        uploaded_file = st.file_uploader(
            "Choose an image for company logo...", 
            type=['png', 'jpg', 'jpeg', 'webp', 'svg'],
            key="logo_uploader_main"
        )
        if uploaded_file is not None:
            with open("logo.png", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("✅ Logo uploaded! Refreshing...")
            st.rerun()

if logo_path:
    logo_editor()

# 🖨️ NATIVE DOWNLOAD-TO-PRINT ENGINE
def display_print_engine(dataframe, report_title):
    if dataframe.empty: return
    html_table = dataframe.to_html(index=False, classes='table')
    html_document = f"""
    <!DOCTYPE html><html><head><title>{report_title}</title>
    <style>body{{font-family:'Segoe UI',sans-serif;padding:35px;color:#222;}} table{{width:100%;border-collapse:collapse;margin-top:20px;font-size:13px;}} th,td{{border:1px solid #bbb;padding:10px;text-align:left;}} th{{background-color:#1e3d59;color:white;}} h2{{color:#1e3d59;}}</style>
    </head><body onload="window.print();"><h2>🏭 NOF FOOD MAKERS Pvt Ltd</h2><h4>Report: {report_title}</h4><hr/>{html_table}</body></html>
    """
    st.download_button(
        label="🖨️ Print Report", data=html_document,
        file_name=f"{report_title.replace(' ', '_').lower()}.html", mime="text/html",
        key=f"dl_{report_title.replace(' ', '_')}_{len(dataframe)}"
    )

# --- SECURITY APP STATES CONFIGURATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = "Worker"
if 'user_dept' not in st.session_state: st.session_state.user_dept = "All"
if 'active_username' not in st.session_state: st.session_state.active_username = ""

# --- DROPDOWN LOGIN SYSTEM PANEL ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; margin-top:50px;'>🔐 Login</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            system_users_list = database.fetch_all_users()
            user_dropdown_options = [user['username'] for user in system_users_list]
            
            selected_user = st.selectbox("Select User:", user_dropdown_options)
            password = st.text_input("Password:", type="password")
            
            if st.form_submit_button("Sign In", use_container_width=True):
                matched_account = next((u for u in system_users_list if u['username'] == selected_user), None)
                if matched_account and matched_account['password'] == password:
                    st.session_state.logged_in = True
                    st.session_state.active_username = matched_account['username']
                    st.session_state.user_role = matched_account['role']
                    st.session_state.user_dept = matched_account['assigned_dept']
                    st.success("Welcome! Authentication Successful.")
                    st.rerun()
                else:
                    st.error("❌ Invalid Password. Please check and try again.")
else:
    # --- CONTROL BAR ---
    title_col, logout_col = st.columns([5, 1])
    with title_col:
        st.markdown(f"### 👋 Welcome, **{st.session_state.active_username}**")
        st.caption(f"🔑 Role: **{st.session_state.user_role}** | 📦 Dept: **{st.session_state.user_dept}**")
    with logout_col:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
    st.write("---")

    # --- Sidebar Navigation Routing ---
    master_pages_hub = [
        "📊 Stock Dashboard", "➕ New Item", 
        "🌾 Raw Materials", "📦 Empty Cartons", "📜 Paper Reels", "📦 Finished Goods",
        "📦 New Order", "⚙️ Production Floor", 
        "👤 Customers", "⚙️ Settings", "👤 About"
    ]
    
    if st.session_state.user_role == "Worker":
        if st.session_state.user_dept == "Raw Material": 
            allowed_screens = ["🌾 Raw Materials"]
        elif st.session_state.user_dept == "Empty Carton": 
            allowed_screens = ["📦 Empty Cartons"]
        elif st.session_state.user_dept == "Paper Reels": 
            allowed_screens = ["📜 Paper Reels"]
        elif st.session_state.user_dept == "Finished Goods":
            allowed_screens = ["📦 Finished Goods"]
        else: 
            allowed_screens = ["👤 About"]
    elif st.session_state.user_role == "Secondary":
        allowed_screens = [p for p in master_pages_hub if p != "⚙️ Settings"]
    else:
        allowed_screens = master_pages_hub

    st.sidebar.markdown("### 🗺️ Navigation")
    page = st.sidebar.radio("Select Screen:", allowed_screens)

    if 'order_cart' not in st.session_state:
        st.session_state.order_cart = []

    # ==========================================
    # 1. STOCK DASHBOARD
    # ==========================================
    if page == "📊 Stock Dashboard":
        st.subheader("📊 Stock Dashboard")
        d_tab1, d_tab2, d_tab3, d_tab4 = st.tabs(["📦 Finished Goods", "🌾 Raw Materials", "📦 Empty Cartons", "📜 Paper Reels"])
        
        with d_tab1:
            raw_data = database.fetch_all_inventory()
            if raw_data:
                df_stock = pd.DataFrame(raw_data)
                f_col1, f_col2, f_col3 = st.columns(3)
                search_query_fg = f_col1.text_input("Search Product:", key="search_fg")
                selected_packing = f_col2.selectbox("Filter Packing:", ["All"] + sorted(df_stock['packing'].dropna().unique().tolist()))
                selected_unit = f_col3.selectbox("Filter Unit:", ["All"] + sorted(df_stock['unit'].dropna().unique().tolist()))
                
                if search_query_fg:
                    df_stock = df_stock[df_stock['item_name'].str.contains(search_query_fg, case=False, na=False)]
                if selected_packing != "All":
                    df_stock = df_stock[df_stock['packing'] == selected_packing]
                if selected_unit != "All":
                    df_stock = df_stock[df_stock['unit'] == selected_unit]
                
                if not df_stock.empty:
                    df_display = df_stock[['id', 'item_name', 'packing', 'category', 'current_stock', 'safety_stock', 'unit']].copy()
                    
                    def highlight_low_stock(row):
                        if row['current_stock'] <= row['safety_stock']:
                            return ['background-color: #ffebee; color: #c62828; font-weight: bold'] * len(row)
                        return [''] * len(row)
                    
                    styled_df = df_display.style.apply(highlight_low_stock, axis=1)
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                    
                    low_stock_items = df_stock[df_stock['current_stock'] <= df_stock['safety_stock']]
                    if not low_stock_items.empty:
                        st.warning("🚨 Low Stock Alert - Production Needed:")
                        for index, row in low_stock_items.iterrows():
                            deficit = row['safety_stock'] - row['current_stock'] + 100
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{row['item_name']}** - Stock: `{row['current_stock']}` | Safety: `{row['safety_stock']}` | Need: `{deficit}`")
                            with col2:
                                if st.button(f"Order", key=f"gen_{row['id']}"):
                                    database.insert_order("Auto-System", row['item_name'], deficit, 'Pending Production')
                                    st.success(f"✅ Order generated for {row['item_name']}!")
                                    st.rerun()
                    
                    df_print = df_display[['id', 'item_name', 'packing', 'category', 'current_stock', 'safety_stock', 'unit']].copy()
                    df_print.columns = ['ID', 'Product', 'Packing', 'Category', 'Stock', 'Safety', 'Unit']
                    display_print_engine(df_print, "Stock Status")
                    
                    if st.session_state.user_role in ["Master", "Secondary"]:
                        with st.expander("🛠️ Edit / Delete Product"):
                            selected_id_fg = st.selectbox("Select Product ID:", df_stock['id'].tolist(), key="sb_edit_fg")
                            target_fg = df_stock[df_stock['id'] == selected_id_fg].iloc[0]
                            
                            ec1, ec2, ec3 = st.columns(3)
                            edit_fg_name = ec1.text_input("Product Name:", value=str(target_fg['item_name']))
                            edit_fg_pack = ec2.text_input("Packing:", value=str(target_fg['packing']))
                            edit_fg_cat = ec3.text_input("Category:", value=str(target_fg['category']))
                            
                            ec4, ec5, ec6 = st.columns(3)
                            edit_fg_unit = ec4.text_input("Unit:", value=str(target_fg['unit']))
                            edit_fg_safety = ec5.number_input("Safety Stock:", min_value=0, value=int(target_fg['safety_stock']))
                            edit_fg_stock = ec6.number_input("Current Stock:", min_value=0, value=int(target_fg['current_stock']))
                            
                            btn_col1, btn_col2 = st.columns(2)
                            if btn_col1.button("💾 Save Changes", use_container_width=True):
                                if database.update_inventory_item(selected_id_fg, edit_fg_name, edit_fg_pack, edit_fg_cat, edit_fg_unit, edit_fg_safety, edit_fg_stock):
                                    st.success("Updated successfully!")
                                    st.rerun()
                            if btn_col2.button("🗑️ Delete", use_container_width=True):
                                if database.delete_inventory_item(selected_id_fg):
                                    st.warning("Product deleted.")
                                    st.rerun()
                else:
                    st.warning("No records found.")
            else:
                st.info("No items registered.")

        def render_dept_stock_tab(dept_name, search_key):
            rm_data = database.fetch_materials_by_dept(dept_name)
            if rm_data:
                df_rm = pd.DataFrame(rm_data)
                sc1, sc2 = st.columns(2)
                q_txt = sc1.text_input(f"Search {dept_name}:", key=f"s_{search_key}")
                q_unit = sc2.selectbox(f"Filter Unit:", ["All"] + sorted(df_rm['unit'].unique().tolist()), key=f"u_{search_key}")
                
                if q_txt: df_rm = df_rm[df_rm['material_name'].str.contains(q_txt, case=False, na=False)]
                if q_unit != "All": df_rm = df_rm[df_rm['unit'] == q_unit]
                
                if not df_rm.empty:
                    def highlight_low_stock_mat(row):
                        safety = 10
                        if row['current_stock'] <= safety:
                            return ['background-color: #ffebee; color: #c62828; font-weight: bold'] * len(row)
                        return [''] * len(row)
                    
                    df_rm_display = df_rm[['id', 'material_name', 'current_stock', 'unit']].copy()
                    styled_df = df_rm_display.style.apply(highlight_low_stock_mat, axis=1)
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                    
                    df_print = df_rm_display.copy()
                    df_print.columns = ['ID', 'Item', 'Stock', 'Unit']
                    display_print_engine(df_print, f"{dept_name} Stock")
                    
                    if st.session_state.user_role in ["Master", "Secondary"]:
                        with st.expander(f"🛠️ Edit / Delete {dept_name} Item"):
                            selected_id_mat = st.selectbox("Select Item ID:", df_rm['id'].tolist(), key=f"sb_edit_mat_{search_key}")
                            target_mat = df_rm[df_rm['id'] == selected_id_mat].iloc[0]
                            
                            mc1, mc2, mc3 = st.columns(3)
                            edit_mat_name = mc1.text_input("Item Name:", value=str(target_mat['material_name']), key=f"name_mat_{selected_id_mat}")
                            edit_mat_stock = mc2.number_input("Stock:", value=float(target_mat['current_stock']), key=f"stock_mat_{selected_id_mat}")
                            edit_mat_unit = mc3.text_input("Unit:", value=str(target_mat['unit']), key=f"unit_mat_{selected_id_mat}")
                            
                            mb1, mb2 = st.columns(2)
                            if mb1.button("💾 Save Changes", use_container_width=True, key=f"save_mat_btn_{selected_id_mat}"):
                                if database.update_material_item(selected_id_mat, edit_mat_name, edit_mat_stock, edit_mat_unit):
                                    st.success("Updated!")
                                    st.rerun()
                            if mb2.button("🗑️ Delete", use_container_width=True, key=f"del_mat_btn_{selected_id_mat}"):
                                if database.delete_material_item(selected_id_mat):
                                    st.warning("Deleted.")
                                    st.rerun()
                else:
                    st.warning("No records found.")
            else:
                st.info(f"No records found.")

        with d_tab2: render_dept_stock_tab("Raw Material", "rm")
        with d_tab3: render_dept_stock_tab("Empty Carton", "ec")
        with d_tab4: render_dept_stock_tab("Paper Reels", "pr")

    # ==========================================
    # DEPARTMENTS LOGS ENGINE (FIXED - DYNAMIC OUT)
    # ==========================================
    elif page in ["🌾 Raw Materials", "📦 Empty Cartons", "📜 Paper Reels"]:
        target_dept = ""
        default_unit = ""
        if page == "🌾 Raw Materials": target_dept, default_unit = "Raw Material", "Kg"
        elif page == "📦 Empty Cartons": target_dept, default_unit = "Empty Carton", "Pcs"
        elif page == "📜 Paper Reels": target_dept, default_unit = "Paper Reels", "Rolls"
            
        st.title(f"🏭 {target_dept} Department")
        sub_tab1, sub_tab2 = st.tabs(["📥 Stock IN", "📤 Stock OUT"])
        
        cust_list = database.fetch_all_customers()
        cust_names = [c['customer_name'] for c in cust_list] if cust_list else []
        existing_items = [r['material_name'] for r in database.fetch_materials_by_dept(target_dept)]
        
        with sub_tab1:
            with st.form(f"in_form_{target_dept}", clear_on_submit=True):
                m_name = st.selectbox("Item:", existing_items) if existing_items else st.text_input("Item Name:")
                col_in1, col_in2 = st.columns(2)
                m_qty = col_in1.number_input("Quantity:", min_value=0.1, step=0.5, value=10.0)
                source_supplier = col_in2.selectbox("From:", cust_names) if cust_names else col_in2.text_input("Vendor:", value="External Vendor")
                
                if st.form_submit_button("💾 Record IN", use_container_width=True) and m_name:
                    items_all = database.fetch_materials_by_dept(target_dept)
                    matched_unit = next((i['unit'] for i in items_all if i['material_name'] == m_name), default_unit)
                    logged_action = f"IN [From: {source_supplier}]"
                    if database.insert_or_update_material(m_name, target_dept, matched_unit, m_qty, logged_action):
                        st.success("✅ Stock IN recorded!")
                        st.rerun()

        # ===== FIXED OUT SECTION - DYNAMIC =====
        with sub_tab2:
            st.markdown("### 📤 Stock OUT")
            
            # OUT Type Selection - WITHOUT FORM (for dynamic behavior)
            out_type = st.radio("Type:", ["Factory Use", "Sale"], horizontal=True, key=f"out_type_{target_dept}")
            
            # Customer details - show only if Sale is selected
            customer_name = "Factory Use"
            if out_type == "Sale":
                st.markdown("---")
                st.markdown("### 👤 Customer Details")
                cust_names_local = [c['customer_name'] for c in cust_list] if cust_list else []
                if cust_names_local:
                    customer_name = st.selectbox("Select Customer:", cust_names_local, key=f"sale_cust_{target_dept}")
                else:
                    customer_name = st.text_input("Customer Name:", value="Walk-in Customer", key=f"sale_cust_input_{target_dept}")
                st.markdown("---")
            
            # Form for submission
            with st.form(f"out_form_{target_dept}", clear_on_submit=True):
                m_name = st.selectbox("Item:", existing_items) if existing_items else st.text_input("Item Name:")
                m_qty = st.number_input("Quantity:", min_value=0.1, step=0.5, value=1.0)
                
                if st.form_submit_button("🔥 Record OUT", use_container_width=True) and m_name:
                    items_all = database.fetch_materials_by_dept(target_dept)
                    matched_unit = next((i['unit'] for i in items_all if i['material_name'] == m_name), default_unit)
                    
                    if out_type == "Sale":
                        action_context = f'SALE [Customer: {customer_name}]'
                    else:
                        action_context = 'FACTORY USE'
                    
                    if database.insert_or_update_material(m_name, target_dept, matched_unit, m_qty, action_context):
                        st.warning(f"⚠️ Stock reduced! ({out_type})")
                        st.rerun()
                            
        st.write("---")
        st.subheader("📋 Transaction Log")
        col_f1, col_f2, col_f3 = st.columns([2, 2, 3])
        start_date = col_f1.date_input("From:", value=pd.Timestamp.now() - pd.Timedelta(days=30), key=f"sd_{target_dept}")
        end_date = col_f2.date_input("To:", value=pd.Timestamp.now(), key=f"ed_{target_dept}")
        search_item = col_f3.text_input("🔍 Filter:", placeholder="Search...", key=f"sh_{target_dept}")
        
        s_str = start_date.strftime("%Y-%m-%d 00:00:00")
        e_str = end_date.strftime("%Y-%m-%d 23:59:59")
        
        logs = database.fetch_material_logs(target_dept, start_str=s_str, end_str=e_str, search_query=search_item)
        
        if logs:
            df_logs = pd.DataFrame(logs)
            df_logs.columns = ['ID', 'Item', 'Event', 'Qty', 'Time']
            display_print_engine(df_logs, f"{target_dept} Log")
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            
            if st.session_state.user_role in ["Master", "Secondary"]:
                with st.expander("🚨 Delete Log Entry"):
                    target_log_id = st.selectbox("Select Log ID:", df_logs['ID'].tolist(), key=f"sb_log_{target_dept}")
                    if st.button("🗑️ Delete", use_container_width=True):
                        if database.delete_material_log(target_log_id):
                            st.warning(f"Log {target_log_id} deleted.")
                            st.rerun()
        else:
            st.info("No transactions found.")

    # ==========================================
    # FINISHED GOODS DEPT (FIXED - DYNAMIC OUT)
    # ==========================================
    elif page == "📦 Finished Goods":
        st.title("🏭 Finished Goods")
        
        inventory = database.fetch_all_inventory()
        inv_names = [item['item_name'] for item in inventory] if inventory else []
        
        sub_tab1, sub_tab2 = st.tabs(["📥 Stock IN", "📤 Stock OUT"])
        
        cust_list = database.fetch_all_customers()
        cust_names = [c['customer_name'] for c in cust_list] if cust_list else []
        
        with sub_tab1:
            with st.form("fg_in_form", clear_on_submit=True):
                item_name = st.selectbox("Product:", inv_names) if inv_names else st.text_input("Product Name:")
                col1, col2 = st.columns(2)
                qty_in = col1.number_input("Quantity:", min_value=0.1, step=0.5, value=10.0)
                source = col2.selectbox("Source:", cust_names) if cust_names else col2.text_input("Source:", value="Production")
                
                if st.form_submit_button("💾 Record IN", use_container_width=True) and item_name:
                    target_item = next((i for i in inventory if i['item_name'] == item_name), None)
                    if target_item:
                        new_stock = target_item['current_stock'] + qty_in
                        if database.update_stock_level(item_name, new_stock):
                            st.success(f"✅ Stock added! New: {new_stock}")
                            st.rerun()
                    else:
                        st.error("Item not found!")

        # ===== FIXED OUT SECTION - DYNAMIC =====
        with sub_tab2:
            st.markdown("### 📤 Stock OUT")
            
            # OUT Type Selection - WITHOUT FORM (for dynamic behavior)
            out_type = st.radio("Type:", ["Factory Use", "Sale"], horizontal=True, key="fg_out_type")
            
            # Customer details - show only if Sale is selected
            customer_name = "Factory Use"
            if out_type == "Sale":
                st.markdown("---")
                st.markdown("### 👤 Customer Details")
                if cust_names:
                    customer_name = st.selectbox("Select Customer:", cust_names, key="fg_sale_cust")
                else:
                    customer_name = st.text_input("Customer Name:", value="Walk-in Customer", key="fg_sale_cust_input")
                st.markdown("---")
            
            # Form for submission
            with st.form("fg_out_form", clear_on_submit=True):
                item_name = st.selectbox("Product:", inv_names) if inv_names else st.text_input("Product Name:")
                col1, col2 = st.columns(2)
                qty_out = col1.number_input("Quantity:", min_value=0.1, step=0.5, value=1.0)
                
                if st.form_submit_button("🔥 Record OUT", use_container_width=True) and item_name:
                    target_item = next((i for i in inventory if i['item_name'] == item_name), None)
                    if target_item:
                        if target_item['current_stock'] >= qty_out:
                            new_stock = target_item['current_stock'] - qty_out
                            if database.update_stock_level(item_name, new_stock):
                                status = "Fulfilled" if out_type == "Sale" else "Factory Use"
                                database.insert_order(customer_name, item_name, qty_out, status)
                                st.warning(f"⚠️ Stock deducted! New: {new_stock} ({out_type})")
                                st.rerun()
                        else:
                            st.error(f"❌ Insufficient stock! Available: {target_item['current_stock']}")
                    else:
                        st.error("Item not found!")
        
        st.write("---")
        st.subheader("📊 Inventory")
        if inventory:
            df_inv = pd.DataFrame(inventory)
            df_display = df_inv[['id', 'item_name', 'packing', 'category', 'current_stock', 'safety_stock', 'unit']]
            df_display.columns = ['ID', 'Product', 'Packing', 'Category', 'Stock', 'Safety', 'Unit']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            if st.session_state.user_role in ["Master", "Secondary"]:
                with st.expander("🛠️ Edit / Delete Product"):
                    sel_id = st.selectbox("Select Product ID:", df_inv['id'].tolist(), key="edit_fg_dept")
                    target = df_inv[df_inv['id'] == sel_id].iloc[0]
                    
                    c1, c2, c3 = st.columns(3)
                    new_name = c1.text_input("Product:", value=target['item_name'])
                    new_pack = c2.text_input("Packing:", value=target['packing'])
                    new_cat = c3.text_input("Category:", value=target['category'])
                    c4, c5, c6 = st.columns(3)
                    new_unit = c4.text_input("Unit:", value=target['unit'])
                    new_safety = c5.number_input("Safety Stock:", min_value=0, value=int(target['safety_stock']))
                    new_stock = c6.number_input("Current Stock:", min_value=0, value=int(target['current_stock']))
                    
                    btn1, btn2 = st.columns(2)
                    if btn1.button("💾 Save Changes", key="update_fg_dept"):
                        if database.update_inventory_item(sel_id, new_name, new_pack, new_cat, new_unit, new_safety, new_stock):
                            st.success("✅ Updated!")
                            st.rerun()
                    if btn2.button("🗑️ Delete", key="del_fg_dept"):
                        if database.delete_inventory_item(sel_id):
                            st.warning("⚠️ Deleted!")
                            st.rerun()
        else:
            st.info("No inventory found.")

    # ==========================================
    # NEW ITEM
    # ==========================================
    elif page == "➕ New Item":
        st.subheader("➕ Add New Item")
        with st.form("universal_add_item_form", clear_on_submit=True):
            col_u1, col_u2 = st.columns(2)
            item_name_input = col_u1.text_input("Item Name:")
            selected_dept = col_u2.selectbox("Department:", ["Finished Goods", "Raw Material", "Empty Carton", "Paper Reels"])
            
            col_u3, col_u4, col_u5 = st.columns(3)
            if selected_dept == "Finished Goods":
                pack_details = col_u3.text_input("Packing:", value="12x50 Box")
                prod_cat = col_u4.selectbox("Category:", ["Toffee", "Bubblegum", "Chocolates", "Others"])
                unit_type = col_u5.text_input("Unit:", value="Jars")
                safety_stock_input = st.number_input("Safety Stock:", min_value=1, value=50)
            else:
                pack_details, prod_cat, safety_stock_input = "", "", 0
                unit_type = col_u3.text_input("Unit:", value="Kg" if selected_dept == "Raw Material" else ("Pcs" if selected_dept == "Empty Carton" else "Rolls"))
                
            if st.form_submit_button("💾 Save Item", use_container_width=True) and item_name_input:
                if selected_dept == "Finished Goods":
                    database.insert_inventory(item_name_input, pack_details, prod_cat, unit_type, safety_stock_input, 0)
                else:
                    database.insert_or_update_material(item_name_input, selected_dept, unit_type, 0.0, 'INITIAL REGISTRATION')
                st.success(f"🎉 '{item_name_input}' registered!")
                st.rerun()

        st.write("---")
        st.subheader("📋 Registered Items")
        
        all_inv = database.fetch_all_inventory()
        all_raw = database.fetch_materials_by_dept("Raw Material")
        all_carton = database.fetch_materials_by_dept("Empty Carton")
        all_reels = database.fetch_materials_by_dept("Paper Reels")
        
        def normalize_inventory_data(data_list, dept_name):
            normalized = []
            for item in data_list:
                row = {
                    'id': item.get('id', ''),
                    'item_name': item.get('item_name') or item.get('material_name', ''),
                    'packing': item.get('packing', '-'),
                    'category': item.get('category', '-'),
                    'unit': item.get('unit', '-'),
                    'current_stock': item.get('current_stock', 0),
                    'safety_stock': item.get('safety_stock', 0),
                    'department': dept_name
                }
                if not row['item_name'] or row['item_name'] == '':
                    row['item_name'] = f"Unnamed (ID: {row['id']})"
                normalized.append(row)
            return normalized
        
        inv_data = normalize_inventory_data(all_inv, "Finished Goods")
        raw_data = normalize_inventory_data(all_raw, "Raw Material")
        carton_data = normalize_inventory_data(all_carton, "Empty Carton")
        reels_data = normalize_inventory_data(all_reels, "Paper Reels")
        
        df_inv = pd.DataFrame(inv_data) if inv_data else pd.DataFrame()
        df_raw = pd.DataFrame(raw_data) if raw_data else pd.DataFrame()
        df_carton = pd.DataFrame(carton_data) if carton_data else pd.DataFrame()
        df_reels = pd.DataFrame(reels_data) if reels_data else pd.DataFrame()
        
        dept_filter = st.selectbox("Filter Department:", ["All", "Finished Goods", "Raw Material", "Empty Carton", "Paper Reels"])
        search_item = st.text_input("🔍 Search:", placeholder="Type to search...")
        
        if dept_filter == "All":
            combined_data = []
            if not df_inv.empty:
                df_inv_copy = df_inv.copy()
                combined_data.append(df_inv_copy)
            if not df_raw.empty:
                df_raw_copy = df_raw.copy()
                combined_data.append(df_raw_copy)
            if not df_carton.empty:
                df_carton_copy = df_carton.copy()
                combined_data.append(df_carton_copy)
            if not df_reels.empty:
                df_reels_copy = df_reels.copy()
                combined_data.append(df_reels_copy)
            
            if combined_data:
                df_all = pd.concat(combined_data, ignore_index=True)
                if search_item:
                    df_all = df_all[df_all['item_name'].str.contains(search_item, case=False, na=False)]
                
                display_cols = ['item_name', 'department', 'packing', 'category', 'unit', 'current_stock', 'safety_stock']
                df_display = df_all[display_cols].copy()
                df_display.columns = ['Item', 'Department', 'Packing', 'Category', 'Unit', 'Stock', 'Safety']
                df_display = df_display.fillna('-')
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.info("No items registered.")
        else:
            if dept_filter == "Finished Goods":
                df_show = df_inv
            elif dept_filter == "Raw Material":
                df_show = df_raw
            elif dept_filter == "Empty Carton":
                df_show = df_carton
            elif dept_filter == "Paper Reels":
                df_show = df_reels
            else:
                df_show = pd.DataFrame()
            
            if not df_show.empty:
                if search_item:
                    df_show = df_show[df_show['item_name'].str.contains(search_item, case=False, na=False)]
                
                if dept_filter == "Finished Goods":
                    display_cols = ['id', 'item_name', 'packing', 'category', 'unit', 'current_stock', 'safety_stock']
                    col_names = ['ID', 'Item', 'Packing', 'Category', 'Unit', 'Stock', 'Safety']
                else:
                    display_cols = ['id', 'item_name', 'unit', 'current_stock']
                    col_names = ['ID', 'Item', 'Unit', 'Stock']
                
                df_display = df_show[display_cols].copy()
                df_display.columns = col_names
                df_display = df_display.fillna('-')
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                if st.session_state.user_role in ["Master", "Secondary"]:
                    with st.expander(f"🛠️ Edit / Delete {dept_filter} Item"):
                        sel_id = st.selectbox("Select ID:", df_show['id'].tolist(), key=f"edit_{dept_filter.replace(' ', '_')}")
                        target = df_show[df_show['id'] == sel_id].iloc[0]
                        
                        if dept_filter == "Finished Goods":
                            c1, c2, c3 = st.columns(3)
                            new_name = c1.text_input("Name:", value=target['item_name'])
                            new_pack = c2.text_input("Packing:", value=target['packing'] if target['packing'] != '-' else '')
                            new_cat = c3.text_input("Category:", value=target['category'] if target['category'] != '-' else '')
                            c4, c5, c6 = st.columns(3)
                            new_unit = c4.text_input("Unit:", value=target['unit'] if target['unit'] != '-' else '')
                            new_safety = c5.number_input("Safety Stock:", min_value=0, value=int(target['safety_stock']))
                            new_stock = c6.number_input("Current Stock:", min_value=0, value=int(target['current_stock']))
                            
                            btn1, btn2 = st.columns(2)
                            if btn1.button("💾 Update", key=f"update_{dept_filter.replace(' ', '_')}"):
                                if database.update_inventory_item(sel_id, new_name, new_pack, new_cat, new_unit, new_safety, new_stock):
                                    st.success("✅ Updated!")
                                    st.rerun()
                            if btn2.button("🗑️ Delete", key=f"del_{dept_filter.replace(' ', '_')}"):
                                if database.delete_inventory_item(sel_id):
                                    st.warning("⚠️ Deleted!")
                                    st.rerun()
                        else:
                            c1, c2, c3 = st.columns(3)
                            new_name = c1.text_input("Name:", value=target['item_name'])
                            new_unit = c2.text_input("Unit:", value=target['unit'] if target['unit'] != '-' else '')
                            new_stock = c3.number_input("Stock:", min_value=0, value=float(target['current_stock']))
                            
                            btn1, btn2 = st.columns(2)
                            if btn1.button("💾 Update", key=f"update_{dept_filter.replace(' ', '_')}"):
                                if database.update_material_item(sel_id, new_name, new_stock, new_unit):
                                    st.success("✅ Updated!")
                                    st.rerun()
                            if btn2.button("🗑️ Delete", key=f"del_{dept_filter.replace(' ', '_')}"):
                                if database.delete_material_item(sel_id):
                                    st.warning("⚠️ Deleted!")
                                    st.rerun()
            else:
                st.info(f"No {dept_filter.lower()} registered.")

    # ==========================================
    # NEW ORDER
    # ==========================================
    elif page == "📦 New Order":
        st.subheader("🛒 New Order")
        cust_list = database.fetch_all_customers()
        if not cust_list:
            st.warning("Please register customers first.")
        else:
            cust_names = [c['customer_name'] for c in cust_list]
            selected_customer = st.selectbox("Customer:", cust_names)
            
            inv_list = database.fetch_all_inventory()
            inv_names = [i['item_name'] for i in inv_list]
            
            if inv_names:
                col_i1, col_i2 = st.columns([3, 1])
                selected_item = col_i1.selectbox("Product:", inv_names)
                order_qty = col_i2.number_input("Quantity:", min_value=1, value=100)
                
                if st.button("➕ Add to Order"):
                    st.session_state.order_cart.append({'item_name': selected_item, 'quantity': order_qty})
                    st.rerun()
            
            if st.session_state.order_cart:
                st.write("### Cart Items:")
                st.dataframe(pd.DataFrame(st.session_state.order_cart), use_container_width=True)
                
                c_btn1, c_btn2 = st.columns(2)
                if c_btn1.button("🗑️ Clear Cart"):
                    st.session_state.order_cart = []
                    st.rerun()
                if c_btn2.button("💾 Confirm Order"):
                    for cart_item in st.session_state.order_cart:
                        engine.process_new_order(selected_customer, cart_item['item_name'], cart_item['quantity'])
                    st.session_state.order_cart = []
                    st.success("✅ Order confirmed!")
                    st.rerun()

    # ==========================================
    # PRODUCTION FLOOR
    # ==========================================
    elif page == "⚙️ Production Floor":
        st.subheader("⚙️ Production Floor")
        
        all_inv = database.fetch_all_inventory()
        low_stock_items = []
        if all_inv:
            for item in all_inv:
                if item['current_stock'] <= item['safety_stock']:
                    low_stock_items.append(item)
        
        if low_stock_items:
            st.info("📋 Products needing production:")
            df_low = pd.DataFrame(low_stock_items)
            df_low['needed'] = df_low['safety_stock'] - df_low['current_stock'] + 100
            
            display_cols = ['item_name', 'current_stock', 'safety_stock', 'needed']
            df_display_low = df_low[display_cols].copy()
            df_display_low.columns = ['Product', 'Stock', 'Safety', 'Required']
            st.dataframe(df_display_low, use_container_width=True, hide_index=True)
            
            st.write("---")
            st.write("### Actions")
            
            col1, col2 = st.columns(2)
            with col1:
                selected_low_item = st.selectbox("Select Product:", df_low['item_name'].tolist())
            with col2:
                prod_qty = st.number_input("Qty:", min_value=1, value=100, step=50)
            
            if st.button("📤 Generate Order"):
                database.insert_order("Auto-System", selected_low_item, prod_qty, 'Pending Production')
                st.success(f"✅ Order generated for {selected_low_item}!")
                st.rerun()
            
            if st.button("⚡ Generate All Orders"):
                for item in low_stock_items:
                    deficit = item['safety_stock'] - item['current_stock'] + 100
                    database.insert_order("Auto-System", item['item_name'], deficit, 'Pending Production')
                st.success(f"✅ Orders generated for {len(low_stock_items)} items!")
                st.rerun()
        else:
            st.success("✅ All products above safety levels.")
        
        st.write("---")
        st.subheader("📋 Active Orders")
        
        prod_data = database.fetch_pending_production()
        if prod_data:
            df_pending = pd.DataFrame(prod_data)
            display_print_engine(df_pending, "Active Orders")
            st.dataframe(df_pending, use_container_width=True, hide_index=True)
            
            st.write("---")
            selected_done_id = st.selectbox("Complete Order ID:", [str(task['schedule_id']) for task in prod_data])
            if st.button("✅ Mark as Completed"):
                conn = database.get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status='Fulfilled' WHERE id=?;", (selected_done_id,))
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"Order {selected_done_id} completed!")
                st.rerun()
        else:
            st.info("✅ No pending orders.")
            
        st.write("---")
        st.subheader("📋 Order History")
        all_orders = database.fetch_all_orders()
        if all_orders:
            df_orders = pd.DataFrame(all_orders)
            st.dataframe(df_orders, use_container_width=True, hide_index=True)
            
            if st.session_state.user_role in ["Master", "Secondary"]:
                with st.expander("🗑️ Delete Order"):
                    target_ord_id = st.selectbox("Order ID:", df_orders['Order ID'].tolist())
                    if st.button("🗑️ Delete", use_container_width=True):
                        if database.delete_order_record(target_ord_id):
                            st.warning("Order deleted.")
                            st.rerun()

    # ==========================================
    # CUSTOMERS
    # ==========================================
    elif page == "👤 Customers":
        st.subheader("👤 Customers / Suppliers")
        with st.form("add_customer_form", clear_on_submit=True):
            cc1, cc2 = st.columns(2)
            c_name = cc1.text_input("Name:")
            c_phone = cc2.text_input("Phone:")
            c_address = st.text_area("Address:")
            if st.form_submit_button("Register") and c_name:
                database.insert_customer(customer_name=c_name, phone=c_phone, address=c_address)
                st.success(f"✔️ '{c_name}' registered.")
                st.rerun()

        st.write("---")
        cust_list = database.fetch_all_customers()
        if cust_list:
            df_cust = pd.DataFrame(cust_list)[['id', 'customer_name', 'phone', 'address']]
            display_print_engine(df_cust, "Customers")
            st.dataframe(df_cust, use_container_width=True, hide_index=True)
            
            if st.session_state.user_role in ["Master", "Secondary"]:
                with st.expander("🗑️ Delete Customer"):
                    target_cust_id = st.selectbox("Select ID:", df_cust['id'].tolist())
                    if st.button("🗑️ Delete", use_container_width=True):
                        if database.delete_customer(target_cust_id):
                            st.warning("Customer deleted.")
                            st.rerun()

    # ==========================================
    # SETTINGS (MASTER ONLY)
    # ==========================================
    elif page == "⚙️ Settings":
        if st.session_state.user_role != "Master":
            st.error("⛔ Access Denied! Master only.")
        else:
            st.subheader("⚙️ User Management")
            with st.form("add_new_user_form", clear_on_submit=True):
                st.write("### ➕ New User")
                new_username = st.text_input("Username:")
                new_password = st.text_input("Password:", type="password")
                new_role = st.selectbox("Role:", ["Master", "Secondary", "Worker"])
                new_dept = st.selectbox("Department:", ["All", "Raw Material", "Empty Carton", "Paper Reels", "Finished Goods"])
                
                if st.form_submit_button("💾 Save", use_container_width=True):
                    if new_username and new_password:
                        if database.insert_user(new_username, new_password, new_role, new_dept):
                            st.success(f"🚀 User '{new_username}' registered!")
                            st.rerun()
                        else:
                            st.error("Username already taken.")
            
            st.write("---")
            st.write("### 📋 Users")
            user_directory = database.fetch_all_users()
            
            if user_directory:
                df_users = pd.DataFrame(user_directory)
                st.dataframe(df_users[['id', 'username', 'role', 'assigned_dept']], use_container_width=True, hide_index=True)
                
                with st.expander("🛠️ Edit / Delete User"):
                    target_id = st.selectbox("User ID:", df_users['id'].tolist())
                    target_user = next((u for u in user_directory if u['id'] == target_id), None)
                    
                    if target_user:
                        edit_name = st.text_input("Username:", value=target_user['username'])
                        edit_pass = st.text_input("Password:", value=target_user['password'], type="password")
                        edit_role = st.selectbox("Role:", ["Master", "Secondary", "Worker"], index=["Master", "Secondary", "Worker"].index(target_user['role']))
                        
                        dept_list = ["All", "Raw Material", "Empty Carton", "Paper Reels", "Finished Goods"]
                        current_dept_index = dept_list.index(target_user['assigned_dept']) if target_user['assigned_dept'] in dept_list else 0
                        edit_dept = st.selectbox("Department:", dept_list, index=current_dept_index)
                        
                        col_action1, col_action2 = st.columns(2)
                        if col_action1.button("💾 Update", use_container_width=True):
                            if database.update_user(target_id, edit_name, edit_pass, edit_role, edit_dept):
                                st.success("User updated.")
                                st.rerun()
                                
                        if col_action2.button("🗑️ Delete", use_container_width=True):
                            if edit_name == "admin":
                                st.error("Cannot delete admin.")
                            else:
                                if database.delete_user(target_id):
                                    st.warning("User deleted.")
                                    st.rerun()

    # ==========================================
    # ABOUT
    # ==========================================
    elif page == "👤 About":
        st.subheader("👤 About")
        
        if os.path.exists("my_pic.png"):
            st.image("my_pic.png", caption="Nabeel Naeem", width=200)
        else:
            st.info("📷 Photo not found.")
        
        st.markdown("""
            <h3>👨‍💻 Nabeel Naeem</h3>
            <p><b>ICS Computer Science Student & Factory Operations Manager</b></p>
            <hr/>
            <p><b>NOF FOOD MAKERS Pvt Ltd</b> - Smart Factory OS</p>
            <p>Engineered to eliminate manual errors and enable real-time operational transparency.</p>
            <hr/>
            <p><b>📧</b> nabeel@example.com</p>
            <p><b>📱</b> +92-XXX-XXXXXXX</p>
        """, unsafe_allow_html=True)
