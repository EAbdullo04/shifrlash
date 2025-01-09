import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
import joblib
from datetime import datetime
import requests  # API orqali oltin narxini olish uchun kutubxona

# Login va parol uchun shifrlash funksiyasi
def generate_key():
    return Fernet.generate_key()

def encrypt_password(password, key):
    cipher = Fernet(key)
    return cipher.encrypt(password.encode())

def verify_password(encrypted_password, password, key):
    cipher = Fernet(key)
    try:
        return cipher.decrypt(encrypted_password).decode() == password
    except Exception:
        return False

# Kalitni saqlash
if 'key' not in st.session_state:
    st.session_state['key'] = generate_key()

# Login va parol ma'lumotlari
stored_login = "admin"
stored_password = encrypt_password("admin123", st.session_state['key'])

# Login tizimi
st.title("Tizimga Kirish")
login_input = st.text_input("Loginni kiriting")
password_input = st.text_input("Parolni kiriting", type="password")

if st.button("Kirish"):
    if login_input == stored_login and verify_password(stored_password, password_input, st.session_state['key']):
        st.success("Tizimga muvaffaqiyatli kirdingiz!")

        # Oltin narxi bashorati dasturi
        st.title("Oltin narxi bashorati")
        st.write("Kelajakdagi sanani tanlang va bashoratlangan oltin narxini ko'ring.")

        # 1. Modelni yuklash
        model = joblib.load("oltin1.pkl")  # Model fayli yuklangan deb hisoblanadi

        # 2. Foydalanuvchidan kelajakdagi sanani olish
        future_date = st.date_input("Sanani tanlang:", value=datetime(2024, 12, 13))

        # Sanani xususiyatlarga ajratish
        year = future_date.year
        month = future_date.month
        day = future_date.day
        day_of_year = future_date.timetuple().tm_yday

        # 3. Bashorat qilish
        if st.button("Bashoratni ko'rish"):
            input_data = pd.DataFrame({
                "Year": [year],
                "Month": [month],
                "Day": [day],
                "DayOfYear": [day_of_year]
            })
            prediction = model.predict(input_data)
            st.write(f"Bashorat qilingan oltin narxi: **${prediction[0]:,.2f} USD**")

        # 4. Bugungi oltin narxini olish (api-ninjas orqali)
        def get_current_gold_price():
            api_url = 'https://api.api-ninjas.com/v1/goldprice'
            headers = {'X-Api-Key': 'BBmkbdXKOWYZHpDRy76UFw==8UmOG7IHI9XryWjO'}  # API kalitini bu yerga qo'shing

            try:
                response = requests.get(api_url, headers=headers)
                if response.status_code == requests.codes.ok:
                    data = response.json()
                    return data['price']
                else:
                    return None
            except requests.exceptions.RequestException as e:
                print("Error:", str(e))
                return None

        # Bugungi oltin narxini ko'rsatish
        current_price = get_current_gold_price()
        if current_price:
            st.write(f"Bugungi oltin narxi: **${current_price:,.2f} USD**")
        else:
            st.write("Bugungi oltin narxini olishda xatolik yuz berdi.")

        # 5. Qo'shimcha ma'lumot
        st.write("Oltin narxi ma'lumotlari asosida bashorat qilingan modeldan foydalaniladi.")
    else:
        st.error("Login yoki parol noto'g'ri.")
