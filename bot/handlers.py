import re

import requests
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from app.api.endpoints.building import create_building_endpoint, get_all_building_endpoint, delete_building_endpoint
from app.schemas import BuildingCreate
from bot.keyboards import get_keyboard, get_callback_btns
from bot.utils import send_photo_to_chat

handlers_router = Router()


class RunBuilding(StatesGroup):
    pk = State()
    images = State()
    defects = State()


@handlers_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Выберите объект:')
    all_obj = await get_all_building_endpoint()
    for obj in all_obj:
        await message.answer(f"{obj.address}", reply_markup=get_callback_btns(btns={
            'Выбрать': f'get_{obj.id}',
        }))

    await state.set_state(RunBuilding.pk)


@handlers_router.callback_query(F.data.startswith('get_'), RunBuilding.pk)
async def get_build_command(callback: CallbackQuery, state: FSMContext):
    pk = int(callback.data.split("_")[-1])
    await state.update_data(pk=pk)
    await state.set_state(RunBuilding.images)
    await callback.message.answer('Отлично! Теперь отправьте фотографии объекта.')


@handlers_router.message(RunBuilding.images, or_f(F.photo))
async def add_images_command(message: Message, state: FSMContext):
    await state.update_data(images=message.photo[-1].file_id)

    data = await state.get_data()
    photo = data["images"]
    chat_id = "-4269903146"

    await send_photo_to_chat(chat_id, photo, state)


@handlers_router.message(RunBuilding.defects, F.text)
async def add_defects_command(message: Message, state: FSMContext):
    print(message.text)




# Ниже команды для админа
ADMIN_KB = get_keyboard(
    [
        "Добавить",
        "Список",
    ]
)


@handlers_router.message(Command("admin"))
async def admin_start_command(message: Message):
    await message.answer("Выберите действие:", reply_markup=ADMIN_KB)


@handlers_router.message(F.text == 'Список')
async def admin_all_objects_command(message: Message):
    all_obj = await get_all_building_endpoint()
    for obj in all_obj:
        await message.answer(f"{obj.address}\n"
                             f"{obj.images}",
                             reply_markup=get_callback_btns(btns={
                                 'Удалить': f'delete_{obj.id}',
                             })
                             )


@handlers_router.callback_query(F.data.startswith('delete_'))
async def delete_command(callback: CallbackQuery):
    pk = int(callback.data.split("_")[-1])
    await delete_building_endpoint(pk)
    await callback.message.answer("Удалён!")


class AddBuilding(StatesGroup):
    address = State()


@handlers_router.message(StateFilter(None), F.text == 'Добавить')
async def add_buidling_command(message: Message, state: FSMContext):
    await message.answer("Введите адресс объекта")
    await state.set_state(AddBuilding.address)


@handlers_router.message(AddBuilding.address, F.text)
async def add_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()

    try:
        building_create = BuildingCreate(address=data['address'])
        await create_building_endpoint(building_create)
        await message.answer('Объект создан')
        await state.clear()
    except Exception as e:
        await message.answer(f'Ошибка отправки {e}')
        await state.clear()


@handlers_router.message(Command("chat_id"))
async def show_chat_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID: {chat_id}")
