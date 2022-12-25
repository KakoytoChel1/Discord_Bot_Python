import apikeys
import disnake
import random
import data_base_logic as db
from disnake.ext import commands


intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)
conn = None


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(description="Creating order menu for mayors.")
async def get_order_menu(inter: disnake.ApplicationCommandInteraction):
    if inter.guild.get_member(inter.author.id).guild_permissions.administrator:
        order_menu = disnake.Embed(
            title="Заказать постройку здания",
            description="Механизм что предоставляет возможность мэру облегчить свою жизнь,"
                        " и заказать постройку у билдеров в министерстве. Чтобы создать новый раздел,"
                        " и сформировать заказ нажмите на кнопку ниже.",
            color=disnake.Colour.green()
        )

        await inter.response.send_message(embed=order_menu, components=[
            disnake.ui.Button(label="🧱Заказ", style=disnake.ButtonStyle.secondary, custom_id="make_order")
        ])


@bot.listen("on_button_click")
async def create_order_menu(inter: disnake.MessageInteraction):
    guild = inter.guild
    everyone_role = guild.get_role(1008433657628864614)
    builder_role = guild.get_role(1051896050341912596)
    mayor_role = guild.get_role(1051902792429752320)
    sp_access_1_role = guild.get_role(1051905373319221349)

    if inter.component.custom_id == "make_order":

        channel = await guild.create_text_channel(name=f"заказ-id-{random.randint(1, 1000)}",
                                                  category=inter.message.channel.category)

        await channel.set_permissions(everyone_role, view_channel=False)
        await channel.set_permissions(builder_role, view_channel=True, send_messages=False)
        await channel.set_permissions(inter.author, view_channel=True, send_messages=True)

        await channel.set_permissions(mayor_role, view_channel=False, send_messages=False)
        await channel.set_permissions(sp_access_1_role, view_channel=False, send_messages=False)

        sub_order_menu = disnake.Embed(
            title="Форма заказа",
            description="1) Ник в майнкрафте\n"
                        "2) Город\n"
                        "3) Несколько скринов (не больше 3)",
            color=disnake.Colour.green()
        )

        sub_order_menu.add_field(
            name="Примечание",
            value="Данный механизм предназначен для непосредственного оповещения строителей"
                  "и упрощения коммуникации с мэрами городов. По этой причине обмен схематикаи доступен только в лс."
        )

        await channel.send(
            content=f"Приветствую {inter.author.mention}, обладатели роли {builder_role.mention} были оповещены!",
            embed=sub_order_menu,
            components=[
                disnake.ui.Button(label="📌Принять", style=disnake.ButtonStyle.secondary,
                                  custom_id="take_order"),
                disnake.ui.Button(label="🔒Закрыть", style=disnake.ButtonStyle.secondary,
                                  custom_id="close_order")
            ])

        user = (channel.id, inter.author.id, inter.author.name)
        db.add_new_item("mainDB.db", user)

    elif inter.component.custom_id == "take_order":
        channel = inter.message.channel
        user = db.select_item("mainDB.db", inter.message.channel.id)

        await channel.send(
            f"{guild.get_member(int(user[2])).mention} ваш заказ был взять{inter.author.mention}, отпишите ему в лс.")

    elif inter.component.custom_id == "close_order":
        user = db.select_item("mainDB.db", inter.message.channel.id)

        if int(user[2]) == inter.author.id or inter.guild.get_member(
                inter.author.id).guild_permissions.administrator == True:
            db.delete_item("mainDB.db", inter.message.channel.id)
            await inter.message.channel.delete()

    await inter.response.defer()


if __name__ == "__main__":
    bot.run(apikeys.TOKEN)