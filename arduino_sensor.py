import serial

import mysql.connector



# 시리얼 포트 설정

ser = serial.Serial('/dev/ttyACM0', 9600)  # 포트와 보드레이트를 맞게 설정



# MariaDB 연결 설정

mydb = mysql.connector.connect(

    host="localhost",

    user="root",

    password="1111",

    database="flask_login_demo"

)

cursor = mydb.cursor()



# 데이터 삽입 함수 - DHT11 센서 데이터

def insert_dht11_data(temperature, humidity):

    query = "INSERT INTO Dht11_data (Temperature, Humidity) VALUES (%s, %s)"

    cursor.execute(query, (temperature, humidity))

    mydb.commit()



# 데이터 삽입 함수 - 토양 수분 센서 데이터

def insert_soil_moisture_data(soil_moisture):

    query = "INSERT INTO Soil_moisture_data (Soil_moisture) VALUES (%s)"

    cursor.execute(query, (soil_moisture,))

    mydb.commit()



def insert_light_intensity_data(light_intensity):

    query = "INSERT INTO Light_intensity_data(Intensity) VALUES (%s)"

    cursor.execute(query, (light_intensity,))

    mydb.commit()	



try:

    while True:
        try:

            # 시리얼로부터 데이터 읽기

            data = ser.readline().decode().strip()



            # 데이터가 있을 경우에만 처리

            if data:

                print("받은 데이터:", data)



                # 데이터에서 각 센서 데이터 추출

                parts = data.split()



                parts0 = parts[0].split(":")

                parts1 = parts[1].split(":")    

                parts2 = parts[2].split(":")

                parts3 = parts[3].split(":")



                insert_dht11_data(parts0[1], parts1[1])

                insert_soil_moisture_data(parts2[1])

                insert_light_intensity_data(parts3[1])

        except IndexError as e:
            print("인덱스 오류:", e)
            continue

except serial.SerialException as e:

    print("시리얼 포트 오류:", e)

    print("받은 데이터:", data)



except mysql.connector.Error as err:

    print("MySQL 오류:", err)



finally:

    # 연결 종료

    if 'ser' in locals() and ser.is_open:

        ser.close()

    if 'mydb' in locals() and mydb.is_connected():

        cursor.close()

        mydb.close()




