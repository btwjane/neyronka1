import requests
import base64
import time
from random import randint
from aiogram import Bot, Dispatcher, types, executor

Api = '6568119850:AAH-ER82OOFuL_1SnkUoSwdSybahbt0xjjs'
bot = Bot(token=Api)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Попробуй мою нейронку шедеврум на минималках')


def generate_image(prompt_text):
    prompt = {
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
            "seed": randint(10000, 200000000)
        },
        "messages": [
            {
                "weight": 1,
                "text": prompt_text
            }
        ]
        }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVNyRXPDQfuf44Mp-PDq4xbuLXJWO-RzHMMJvYj"
    }

    response = requests.post(url=url, headers=headers, json=prompt)
    result = response.json()
    print(result)

    operation_id = result ['id']

    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(url=operation_url, headers=headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
            break
        else:
            print('Ожидайте, изображение не готово')
            time.sleep(5)

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.reply('Идет генерация изображения, жди')

    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo=image_data)
    except Exception as e:
        await message.reply(f"Произошла ошибка:{e}")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)