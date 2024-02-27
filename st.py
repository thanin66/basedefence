import streamlit as st

def calculate_bmi(weight, height):
    """
    คำนวณดัชนีมวลกาย (BMI) โดยใช้น้ำหนัก (kg) และส่วนสูง (เมตร)
    """
    bmi = weight / (height ** 2)
    return bmi

def main():
    st.title("BMI Calculator")

    weight = st.number_input("น้ำหนัก (kg)")
    height = st.number_input("ส่วนสูง (เมตร)")

    if st.button("คำนวณ BMI"):
        bmi = calculate_bmi(weight, height)
        st.write(f"ดัชนีมวลกาย (BMI): {bmi:.2f}")

        if bmi < 18.5:
            st.write("น้ำหนักน้อยกว่าปกติ")
        elif bmi >= 18.5 and bmi < 25:
            st.write("น้ำหนักปกติ")
        elif bmi >= 25 and bmi < 30:
            st.write("น้ำหนักเกิน")
        else:
            st.write("โรคอ้วน")

    if st.button("ไปหน้าถัดไป"):
        st.session_state.page += 1

def side():
    st.title("หน้าที่สอง")
    if st.button("กลับไปหน้าแรก"): 
        st.session_state.page = 1

if "page" not in st.session_state:
    st.session_state.page = 1
if st.session_state.page == 1:
    main()
elif st.session_state.page == 2:
    side()