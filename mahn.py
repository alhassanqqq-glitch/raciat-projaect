import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="نظام CRM الذكي", layout="wide")

# محاكاة قاعدة بيانات بسيطة
if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame(columns=[
        "الاسم", "البريد الإلكتروني", "الحالة", "القيمة المتوقعة", "تاريخ الإضافة"
    ])

# القائمة الجانبية
st.sidebar.title("لوحة التحكم")
menu = st.sidebar.radio("انتقل إلى:", ["لوحة العرض", "إضافة عميل جديد", "إدارة الصفقات"])

# 1. صفحة لوحة العرض (Dashboard)
if menu == "لوحة العرض":
    st.header("📊 ملخص الأداء")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي العملاء", len(st.session_state.customers))
    with col2:
        total_val = st.session_state.customers["القيمة المتوقعة"].sum() if not st.session_state.customers.empty else 0
        st.metric("إجمالي المبيعات المتوقعة", f"${total_val}")
    with col3:
        st.metric("حالات المتابعة", "5")

    st.subheader("قائمة العملاء الحالية")
    st.table(st.session_state.customers)

# 2. صفحة إضافة عميل
elif menu == "إضافة عميل جديد":
    st.header("➕ إضافة عميل جديد")
    with st.form("customer_form"):
        name = st.text_input("اسم العميل")
        email = st.text_input("البريد الإلكتروني")
        status = st.selectbox("حالة العميل", ["جديد", "مهتم", "تفاوض", "تم البيع", "مستبعد"])
        value = st.number_input("القيمة المتوقعة ($)", min_value=0)
        submitted = st.form_submit_button("حفظ العميل")
        
        if submitted:
            new_data = {
                "الاسم": name,
                "البريد الإلكتروني": email,
                "الحالة": status,
                "القيمة المتوقعة": value,
                "تاريخ الإضافة": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.customers = pd.concat([st.session_state.customers, pd.DataFrame([new_data])], ignore_index=True)
            st.success("تم إضافة العميل بنجاح!")

# 3. إدارة الصفقات (Visual Pipeline)
elif menu == "إدارة الصفقات":
    st.header("📈 مراحل الصفقات")
    if st.session_state.customers.empty:
        st.info("لا توجد صفقات لعرضها حالياً.")
    else:
        # عرض بسيط للمراحل
        st.bar_chart(st.session_state.customers.groupby("الحالة")["القيمة المتوقعة"].sum())
