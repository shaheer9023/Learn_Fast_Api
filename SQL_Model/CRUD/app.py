import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # FastAPI ka URL

st.set_page_config(page_title="Users CRUD with JWT", page_icon="🔐", layout="centered")
st.title("🔐 Users CRUD App")
st.write("Made with ❤️ by Shaheer Ahmad")

if "token" not in st.session_state:
    st.session_state.token = None

# =====================
# Login Section
# =====================
if not st.session_state.token:
    st.subheader("🔑 Super Admin Login")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit = st.form_submit_button("Login")

        if submit:
            data = {"username": username, "password": password}
            try:
                response = requests.post(f"{BASE_URL}/auth/login", data=data)
                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    st.success("✅ Login successful! You can now use the CRUD features.")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.sidebar.success("✅ Logged in")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "❌ Delete"])

    # CREATE
    with tab1:
        st.subheader("➕ Create User")
        name = st.text_input("Enter username")
        password = st.text_input("Enter password")
        if st.button("Create"):
            if name and password:
                response = requests.post(f"{BASE_URL}/users/", json={"username": name, "password": password}, headers=headers)
                if response.status_code == 200:
                    st.success("✅ User Created Successfully!")
                    st.json(response.json())
                else:
                    st.error("❌ Failed to create user")

    # READ
    with tab2:
        st.subheader("📖 Read Users")
        if st.button("Load Users"):
            response = requests.get(f"{BASE_URL}/users/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    st.table(data)
                else:
                    st.info("ℹ️ No users found")
            else:
                st.error("❌ Failed to fetch users")

    # UPDATE
    with tab3:
        st.subheader("✏️ Update User")
        record_id = st.number_input("Enter User ID", min_value=1, step=1)
        new_name = st.text_input("Enter new username")
        new_password = st.text_input("Enter new password")
        if st.button("Update"):
            if new_name and new_password:
                response = requests.put(f"{BASE_URL}/users/{record_id}", json={"username": new_name, "password": new_password}, headers=headers)
                if response.status_code == 200:
                    st.success("✅ User Updated Successfully!")
                    st.json(response.json())
                else:
                    st.error("❌ Failed to update user")

    # DELETE
    with tab4:
        st.subheader("❌ Delete User")
        del_id = st.number_input("Enter User ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            response = requests.delete(f"{BASE_URL}/users/{del_id}", headers=headers)
            if response.status_code == 200:
                st.success("✅ User Deleted Successfully!")
                st.json(response.json())
            else:
                st.error("❌ Failed to delete user")
