from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import subprocess
import uvicorn
import send_reward as SW
import json
import pyodbc

with open("config.json", "r", encoding="utf-8") as file:
    SECRET_FILE = json.load(file)

SERVER = SECRET_FILE["SERVER"]
DATABASE = SECRET_FILE["DATABASE"]
USERNAME = SECRET_FILE["USERNAME"]
PASSWORD = SECRET_FILE["PASSWORD"]
DRIVER = SECRET_FILE["DRIVER"]

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/get_data_esp/")
async def send_tk(humidity: int, temp: float, source: str):
    print(''.center(60, '='))
    print(f'humedad: {humidity} ,temperatura: {temp}, origen: {source}')

    # incert data in db
    with pyodbc.connect(
            'DRIVER=' + DRIVER + ';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD) as conn:
        with conn.cursor() as cursor:
            count = cursor.execute(
                f"INSERT INTO esp8266.dbo.registro_h_t (HUMEDAD, TEMPERATURA, FECHA, ORIGEN) VALUES ({humidity}, {temp}, DEFAULT, {source});").rowcount
            conn.commit()
            print(f'Rows inserted: {str(count)}')

    contract = SW.SendReward()

    contract_state = contract.send_hum_value(humidity)
    print(f"State: {contract_state}")

    sender_balance = contract.get_balance()
    print(f"Balance: {sender_balance}")

    reward = 1
    print(f"Reward: {reward} ")

    send_reward = contract.send_reward(reward=reward,
                                       now_state=contract_state,
                                       now_balance=sender_balance)
    print(send_reward)

    log = {"Humidity": humidity,
           "Temperature": temp,
           "Source": source,
           "State": contract_state,
           "Init balance": sender_balance,
           "Send data": str(send_reward)}

    return log


@app.get('/dashboard/')
async def dashboard(request: Request):
    subprocess.call("/media/oscar/53d0d8e7-064c-4896-b149-1fafedf0f2d2/home/oscar/PycharmProjects/Celo_test/dashboard.py", shell=True)
    return templates.TemplateResponse("new_plot.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
