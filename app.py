import streamlit as st
from cryptography.fernet import Fernet

# Streamlit sarlavhasi va kirish matni
st.title("Ma'lumotlarni Shifrlash Ilovasi")
st.write("Quyida kiritilgan matnni shifrlang va deshifrlang.")

# Kalit yaratish yoki kiritish
key_placeholder = st.empty()
if 'key' not in st.session_state:
    st.session_state['key'] = Fernet.generate_key()

def regenerate_key():
    st.session_state['key'] = Fernet.generate_key()
    key_placeholder.info(f"Yangi kalit: {st.session_state['key'].decode()}")

# Kalitni ko'rsatish va qayta yaratish
key_placeholder.info(f"Kalit: {st.session_state['key'].decode()}")
st.button("Yangi Kalit Yaratish", on_click=regenerate_key)
cipher = Fernet(st.session_state['key'])

# Foydalanuvchi matn kiritishi
user_input = st.text_area("Matnni kiriting", "")

if st.button("Shifrlash"):
    if user_input:
        encrypted_text = cipher.encrypt(user_input.encode())
        st.success("Shifrlangan Matn:")
        st.code(encrypted_text.decode())
    else:
        st.error("Iltimos, matn kiriting.")

if st.button("Deshifrlash"):
    if user_input:
        try:
            decrypted_text = cipher.decrypt(user_input.encode()).decode()
            st.success("Deshifrlangan Matn:")
            st.code(decrypted_text)
        except Exception as e:
            st.error("Deshifrlashda xatolik yuz berdi. Iltimos, to'g'ri matn kiriting.")
    else:
        st.error("Iltimos, shifrlangan matn kiriting.")
