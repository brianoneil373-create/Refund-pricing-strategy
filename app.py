import streamlit as st

# Set page title and layout
st.set_page_config(
    page_title="Bundle Refund Calculator",
    page_icon="📦",
    layout="centered"
)

st.title("📦 Operations Refund Calculator")
st.markdown("Calculate customer refund amounts for bundles according to company refund policy.")

# Define bundle data and base prices (EGP) based on Sheet4
BUNDLES = {
    "The Ultimate Grooming Bundle": {
        "ماكينة حلاقة تريمايز للرجال": 3099.00,
        "تريمايز جل الاستحمام": 349.00,
        "مزيل رائحة العرق من تريمايز": 349.00,
        "تريمايز غسول المناطق الحساسة": 349.00,
    },
    "The Full Routine Bundle": {
        "تريمايز جل الاستحمام": 333.00,
        "مزيل رائحة العرق من تريمايز": 333.00,
        "تريمايز غسول المناطق الحساسة": 333.00,
    },
    "Intimate Bundle": {
        "مزيل رائحة العرق من تريمايز": 374.50,
        "تريمايز غسول المناطق الحساسة": 374.50,
    },
    "The Intimate Care Kit - أسود/أخضر/أزرق": {
        "ماكينة حلاقة تريمايز للرجال": 3132.3333333333335,
        "مزيل رائحة العرق من تريمايز": 382.3333333333333,
        "تريمايز غسول المناطق الحساسة": 382.3333333333333,
    }
}

DISCOUNT_OPTIONS = {
    "0%": 0.00,
    "5%": 0.05,
    "10%": 0.10,
    "25%": 0.25,
    "50%": 0.50
}

# --- Step 1: Select Bundle ---
selected_bundle_name = st.selectbox(
    "1. Please specify the bundle:",
    options=list(BUNDLES.keys())
)

bundle_items = BUNDLES[selected_bundle_name]

# --- Step 2: Select Refund Type ---
refund_type = st.selectbox(
    "2. Select Refund Type:",
    options=["Full Refund", "Partial Refund"]
)

# --- Step 3: Select Discount Percentage ---
discount_label = st.selectbox(
    "3. Select Discount Percentage (%):",
    options=list(DISCOUNT_OPTIONS.keys())
)
discount_pct = DISCOUNT_OPTIONS[discount_label]

st.markdown("---")

# --- Step 4: Logic & Calculation ---

if refund_type == "Full Refund":
    st.subheader("📋 Full Refund Summary")
    
    # Calculate base price total
    total_base_price = sum(bundle_items.values())
    
    # Apply discount
    discounted_total = total_base_price * (1 - discount_pct)
    
    # Fixed shipping deduction for Full Refund
    shipping_deduction = 200.00
    
    # Final Refund
    final_refund = discounted_total - shipping_deduction
    
    # Breakdown Table
    st.write("**Bundle Breakdown:**")
    item_rows = []
    for item_name, base_price in bundle_items.items():
        discounted_item_price = base_price * (1 - discount_pct)
        item_rows.append({
            "Item Name": item_name,
            "Base Price (EGP)": f"{base_price:.2f}",
            "After Discount (EGP)": f"{discounted_item_price:.2f}"
        })
    st.dataframe(item_rows, use_container_width=True)
    
    st.markdown(f"""
    * **Bundle Original Base Price:** EGP {total_base_price:,.2f}
    * **Bundle Price Paid ({discount_label} Discount):** EGP {discounted_total:,.2f}
    * **Shipping Fee Deduction:** - EGP {shipping_deduction:,.2f}
    """)
    
    if final_refund > 0:
        st.success(f"### 💰 Final Refund Amount: EGP {final_refund:,.2f}")
    else:
        st.warning(f"### 💰 Final Refund Amount: EGP 0.00 (Shipping deduction exceeds refund amount)")

else:  # Partial Refund
    st.subheader("📋 Partial Refund Selection")
    
    # Multiselect for returned items
    returned_items = st.multiselect(
        "Select the item(s) returned by the customer:",
        options=list(bundle_items.keys())
    )
    
    if not returned_items:
        st.info("Please select at least one item being returned to calculate the partial refund.")
    else:
        partial_base_total = sum(bundle_items[item] for item in returned_items)
        partial_discounted_total = partial_base_total * (1 - discount_pct)
        shipping_deduction = 100.00
        
        final_refund = partial_discounted_total - shipping_deduction
        
        st.write("**Selected Items Refund Breakdown:**")
        item_rows = []
        for item_name in returned_items:
            base_price = bundle_items[item_name]
            discounted_price = base_price * (1 - discount_pct)
            item_rows.append({
                "Item Name": item_name,
                "Base Price (EGP)": f"{base_price:.2f}",
                "Refund Amount ({})".format(discount_label): f"{discounted_price:.2f}"
            })
        st.dataframe(item_rows, use_container_width=True)
        
        st.markdown(f"""
        * **Subtotal for Returned Items ({discount_label} Discount):** EGP {partial_discounted_total:,.2f}
        * **Shipping Fee Deduction:** - EGP {shipping_deduction:,.2f}
        """)
        
        if final_refund > 0:
            st.success(f"### 💰 Final Refund Amount: EGP {final_refund:,.2f}")
        else:
            st.warning(f"### 💰 Final Refund Amount: EGP 0.00 (Shipping deduction exceeds item refund)")
