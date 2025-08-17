import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:9876"  # FastAPI ka URL

st.set_page_config(page_title="Myself CRUD with JWT", page_icon="🔐", layout="centered")
st.title("🔐 Myself CRUD App")
st.write("Made with ❤️ by Shaheer Ahmad")

# Session state for token
if "token" not in st.session_state:
    st.session_state.token = None

# =====================
# Login Section
# =====================
if not st.session_state.token:
    st.subheader("🔑 Super Admin Login")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit = st.form_submit_button("Login")

        if submit:
            data = {"username": email, "password": password}
            try:
                response = requests.post(f"{BASE_URL}/login", data=data)
                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    st.success("✅ Login successful! You can now use the CRUD features.")
                else:
                    st.error("❌ Invalid credentials")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    # =====================
    # Logout Button
    # =====================
    st.sidebar.success("✅ Logged in as Super Admin")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.rerun()

    # =====================
    # CRUD Tabs
    # =====================
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "❌ Delete"])

    # CREATE
    with tab1:
        st.subheader("➕ Create Record")
        name = st.text_input("Enter name to create")
        if st.button("Create"):
            if name:
                response = requests.post(f"{BASE_URL}/myself/", json={"name": name}, headers=headers)
                if response.status_code == 200:
                    st.success("✅ Record Created Successfully!")
                    st.json(response.json())
                else:
                    st.error("❌ Failed to create record")
            else:
                st.warning("⚠️ Please enter a name")

    # READ
    with tab2:
        st.subheader("📖 Read Records")
        if st.button("Load Records"):
            response = requests.get(f"{BASE_URL}/myself/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    st.table(data)
                else:
                    st.info("ℹ️ No records found")
            else:
                st.error("❌ Failed to fetch records")

    # UPDATE
    with tab3:
        st.subheader("✏️ Update Record")
        record_id = st.number_input("Enter Record ID", min_value=1, step=1)
        new_name = st.text_input("Enter new name for update")
        if st.button("Update"):
            if new_name:
                response = requests.put(
                    f"{BASE_URL}/myself/",
                    json={"id": record_id, "name": new_name},
                    headers=headers
                )
                if response.status_code == 200:
                    st.success("✅ Record Updated Successfully!")
                    st.json(response.json())
                else:
                    st.error("❌ Failed to update record")
            else:
                st.warning("⚠️ Please enter a new name")

    # DELETE
    with tab4:
        st.subheader("❌ Delete Record")
        del_id = st.number_input("Enter Record ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            response = requests.delete(f"{BASE_URL}/myself/{del_id}", headers=headers)
            if response.status_code == 200:
                st.success("✅ Record Deleted Successfully!")
                st.json(response.json())
            else:
                st.error("❌ Failed to delete record")
