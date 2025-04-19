import discord
from discord.ext import commands
import os
from discord import app_commands
import random
import subprocess
from discord import Intents, Client, Interaction, Game
from discord.app_commands import CommandTree
from datetime import timedelta, datetime, timezone
import aiohttp
from keep_alive import keep_alive
import asyncio

TOKEN=os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!" , intents=discord.Intents.all())

def number_to_emoji(number):
    if 1 <= number <= 9:
        return f"{chr(0x0030 + number)}\uFE0F\u20E3"
    return None

@bot.event
async def on_ready ():
    activity_stetas=random.choice(("週末京都現実逃避","2:23 AM","SUMMER TRIANGLE","You and Me","10℃"))
    await bot.change_presence(activity=discord.Game(name="/help｜"f"Join server{len(bot.guilds)}｜""Listening "+activity_stetas))
    print("起動")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期")
    except Exception as e:
        print(e)

embed = [
    discord.Embed(description="## __Table of Contents__")
    .add_field(name="`Page1`", value="投票コマンドの説明", inline=False)
    .add_field(name="`Page2`", value="BAN・time outのコマンドの説明", inline=False)
    .add_field(name="`Page3`", value="Minecraft Serverの説明", inline=False)
    .add_field(name="`Page4`", value="その他のコマンドの説明", inline=False)
    .add_field(name="⇩ご不明点", value="<@795470464909836329>", inline=False)
    .set_author(name="by", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg"),
    discord.Embed(description="## Page1")
    .add_field(name="/decision", value="投票を開始", inline=False)
    .add_field(name="`title`", value="投票のタイトル", inline=True)
    .add_field(name="`q1`", value="1つ目の回答を作成", inline=True)
    .add_field(name="`q2`", value="2つ目の回答を作成", inline=True)
    .add_field(name="/vote", value="複数投票(q3～q9、※q4～q9任意)を開始", inline=False)
    .add_field(name="`q1`", value="1つ目の回答を作成", inline=True)
    .add_field(name="`q2`", value="2つ目の回答を作成", inline=True)
    .add_field(name="`q3`", value="3つ目の回答を作成", inline=True)
    .set_author(name="py", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg"),
    discord.Embed(description="## Page2")
    .add_field(name="/timeout", value="時間指定式タイムアウト", inline=False)
    .add_field(name="`member`", value="タイムアウトするメンバー", inline=True)
    .add_field(name="`duration`", value="時間を指定(秒単位)", inline=True)
    .add_field(name="/ban", value="指定式BAN", inline=False)
    .add_field(name="`member`", value="BANするメンバー", inline=True)
    .add_field(name="`reason`", value="BANする理由", inline=True)
    .set_author(name="py", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg"),
    discord.Embed(description="## Page3")
    .add_field(name="/port", value="Server addressを表示", inline=False)
    .add_field(name="/port_start", value="Portを解放", inline=True)
    .add_field(name="/port_stop", value="Portを閉鎖", inline=True)
    .add_field(name="/server_start", value="Minecraft Serverを起動", inline=False)
    .add_field(name="/server_stop", value="Minecraft Serverを停止", inline=True)
    .add_field(name="/server_status", value="Minecraft Serverの状況", inline=True)
    .add_field(name="/server_player_list", value="Minecraft Serverに参加している人を表示", inline=True)
    .add_field(name="Onlineの時しかServerは起動できません。",value="左：Online\n右：Offline",inline=False)
    .set_image(url="https://cdn.discordapp.com/attachments/1239808781601476682/1338051368740589600/image.jpg?ex=67a9acf2&is=67a85b72&hm=d7402a154310555f257c3c78c509d69f7145be1168ac116d90ccc3251ffb992b&")
    .set_author(name="py", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg"),
    discord.Embed(description="## Page4")
    .add_field(name="/omikuzi", value="おみくじを開始", inline=False)
    .add_field(name="/server", value="サーバー情報を表示", inline=False)
    .add_field(name="/user", value="ユーザー情報を表示", inline=False)
    .add_field(name="/hurupa", value="ランダムでVALORANTのフルパを作成", inline=False)
    .set_author(name="py", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg")
]

ce = "◁"
ce2 = "▷"

class EmbedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.current_page = 0

    @discord.ui.button(label=ce, style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=embed[self.current_page], view=self)

    @discord.ui.button(label=ce2, style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(embed) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=embed[self.current_page], view=self)

@bot.tree.command(name="help", description="BOTの説明")
async def send_pages(interaction: discord.Interaction):
    view = EmbedView()
    await interaction.response.send_message(embed=embed[0], view=view)

@bot.tree.command(name='vote', description='複数投票を作成')
@app_commands.describe(time='投票の時間',title='投票の名前')
@app_commands.choices(
    time=[
        app_commands.Choice(name='10秒', value='10s'),
        app_commands.Choice(name='30分', value='30m'),
        app_commands.Choice(name='1時間', value='1h'),
        app_commands.Choice(name='2時間', value='2h'),
        app_commands.Choice(name='3時間', value='3h'),
        app_commands.Choice(name='12時間', value='12h'),
        app_commands.Choice(name='1日', value='1d'),
        app_commands.Choice(name='1週間', value='1w'),
        app_commands.Choice(name='1か月', value='1mo')
    ]
)
async def vote(
    interaction: discord.Interaction, 
    title: str, 
    time: app_commands.Choice[str], 
    q1: str, 
    q2: str, 
    q3: str, 
    q4: str = None, 
    q5: str = None, 
    q6: str = None, 
    q7: str = None, 
    q8: str = None, 
    q9: str = None, 
):
    
    choices = [q1, q2, q3]
    if q4: choices.append(q4)
    if q5: choices.append(q5)
    if q6: choices.append(q6)
    if q7: choices.append(q7)
    if q8: choices.append(q8)
    if q9: choices.append(q9)

    embed = discord.Embed(title="",description=f"## {title}\n\n" +"\n".join([f"{number_to_emoji(i + 1)}：{choice}" for i, choice in enumerate(choices)]))
    message = await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()

    for i in range(len(choices)):
        await message.add_reaction(f"{i+1}\N{COMBINING ENCLOSING KEYCAP}")
    time_mapping = {
        '10s': 10,
        '30m': 1800,
        '1h': 3600,
        '2h': 7200,
        '3h': 10800,
        '12h': 43200,
        '1d': 86400,
        '1w': 604800,
        '1mo': 2592000
    }

    if time.value in time_mapping:
        await asyncio.sleep(time_mapping[time.value])

    message = await interaction.channel.fetch_message(message.id)
    results = [(reaction.emoji, reaction.count - 1) for reaction in message.reactions]

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    result_embed = discord.Embed(title=f"{title} の結果")
    result_embed.description = "\n".join([f"{r[0]}： {r[1]}票" for r in sorted_results])
    await message.clear_reactions()
    await message.edit(embed=result_embed)

TIME_CHOICES = {
    '10秒': 10,
    '30分': 30 * 60,
    '1時間': 60 * 60,
    '2時間': 2 * 60 * 60,
    '3時間': 3 * 60 * 60,
    '12時間': 12 * 60 * 60,
    '1日': 24 * 60 * 60,
    '1週間': 7 * 24 * 60 * 60,
    '1か月': 30 * 24 * 60 * 60
}

@bot.tree.command(name='decision', description='Yes or No')
@app_commands.describe(
    title='判断のタイトル',
    q1='選択肢1',
    q2='選択肢2',
    time='判断の時間'
)
@app_commands.choices(time=[
    app_commands.Choice(name='10秒', value='10秒'),
    app_commands.Choice(name='30分', value='30分'),
    app_commands.Choice(name='1時間', value='1時間'),
    app_commands.Choice(name='2時間', value='2時間'),
    app_commands.Choice(name='3時間', value='3時間'),
    app_commands.Choice(name='12時間', value='12時間'),
    app_commands.Choice(name='1日', value='1日'),
    app_commands.Choice(name='1週間', value='1週間'),
    app_commands.Choice(name='1か月', value='1か月')
])
async def decision(interaction: discord.Interaction, time: str,title:str, q1: str, q2: str):
    choices = [q1, q2]

    embed = discord.Embed(title="", description="## "+title)
    embed.add_field(name="⭕ "+q1,value="",inline=False)
    embed.add_field(name="❌ "+q2,value="",inline=False)
    message = await interaction.response.send_message(embed=embed)

    message = await interaction.original_response()

    await message.add_reaction("⭕")
    await message.add_reaction("❌")

    wait_time = TIME_CHOICES[time]
    await asyncio.sleep(wait_time)

    message = await interaction.channel.fetch_message(message.id)
    results = [(reaction.emoji, reaction.count - 1) for reaction in message.reactions]

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    result_embed = discord.Embed(title=f"{title} の結果")
    result_embed.description = "\n".join([f"{r[0]}： {r[1]}票" for r in sorted_results])
    await message.clear_reactions()
    await message.edit(embed=result_embed)

@bot.tree.command(name="omikuzi",description="おみくじ")
async def omikuazi(interaction: discord.Interaction):
   text_random=random.choice(("大吉","中吉","小吉","吉","末吉","凶","大凶"))
   text_message=str(text_random)
   await interaction.response.send_message(text_message,ephemeral=True)

@bot.tree.command(name="mc",description="Minecraftserverの詳細")
async def mc(interaction: discord.Interaction): 
   embed = discord.Embed(description="### [MOD](https://d.kuku.lu/d87h2ccud) ＆ [Minecraft](https://www.youtube.com/watch?v=xt_1ASLcdY4)")
   embed.add_field(name="java : `java 17`",value="",inline=False)
   embed.add_field(name="mod : `dimension`",value="",inline=False)
   embed.add_field(name="ver : `FORGE 1.20.1`",value="",inline=False)
   embed.add_field(name="address : `black-tar.gl.joinmc.link`",value="",inline=False)
   embed.add_field(name="・黄昏の森",value="The Twilight Forest",inline=False)
   embed.add_field(name="・ディープアンドダーカー",value="Deeper and Darker",inline=False)
   embed.add_field(name="・ビヨンドアース",value="Beyond Earth",inline=False)
   embed.add_field(name="・ブルースカイズ",value="Blue Skies",inline=False)
   embed.add_field(name="・トロピクラフト",value="Tropicraft",inline=False)
   embed.add_field(name="・エーテル",value="The Aether",inline=False)
   user_id = "795470464909836329"
   member_list = list(bot.get_all_members())
   for i in range(len(member_list)):
        if str(member_list[i].id) == user_id:
            user = member_list[i]
   latte = f"{user._user.mention} "
   embed.add_field(name="⇩ご不明点",value=latte,inline=False)
   await interaction.response.send_message(embed=embed)

@bot.tree.command(name="server",description="serverの詳細")
async def server(interaction: discord.Interaction): 
  guild = interaction.user.guild
  roles =[role for role in guild.roles]
  text_channels = [text_channels for text_channels in guild.text_channels]
  embed = discord.Embed(description="")
  embed.add_field(name="Adomin",value=f"{interaction.guild.owner}",inline=False)
  embed.add_field(name="ID",value=f"{interaction.guild.id}",inline=False)
  embed.add_field(name="Channel",value=f"{len(text_channels)}",inline=False)
  embed.add_field(name="Roll",value=f"{len(roles)}",inline=False)
  embed.add_field(name="Server Booster",value=f"{guild.premium_subscription_count}",inline=False)
  embed.add_field(name="Member",value=f"{guild.member_count}",inline=False)
  embed.add_field(name="Create Server",value=f"{guild.created_at}",inline=False)
  embed.add_field(name="Executor",value=f"{interaction.user}")
  await interaction.response.send_message(embed=embed)

@bot.tree.command(name="user",description="userの詳細")
async def user(interaction: discord.Interaction): 
  embed = discord.Embed(title=f"user {interaction.user.name}",description="userinfo")
  embed.add_field(name="Name",value=f"{interaction.user.mention}",inline=False)
  embed.add_field(name="ID",value=f"{interaction.user.id}",inline=False)
  embed.add_field(name="ACTIVITY",value=f"{interaction.user.activity}",inline=False)
  embed.add_field(name="TOP_ROLE",value=f"{interaction.user.top_role}",inline=False)
  embed.add_field(name="Discriminator",value=f"#{interaction.user.discriminator}",inline=False)
  embed.add_field(name="Join Server",value=f"{interaction.user.joined_at.strftime('%d.%m.%Y, %H:%M Uhr')}",inline=False)
  embed.add_field(name="Create Account",value=f"{interaction.user.created_at.strftime('%d.%m.%Y, %H:%M Uhr')}",inline=False)
  embed.set_thumbnail(url=f"{interaction.user.avatar.url}")
  embed.add_field(name="Executor",value=f"{interaction.user}")
  await interaction.response.send_message(embed=embed)
     
ID_ROLE_MEMBER = 1222196302780301335

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(ID_ROLE_MEMBER)
    await member.add_roles(role)

@bot.event
async def on_message(message):
 user_id=699823803924086794
 if message.author.id !=user_id:
    return
 text_random=random.choice(("ゆ♡い♡か♡だ♡い♡す♡き♡","ゆいちゃんのおしゃぶりはやっぱり甘いな～","ゆいちゃ～ん😀そんなこと言わないでおじさんと濃厚な夜をすごそーよ♡","僕がゆいちゃんを守るよ！","そんなのプンプンしないでw今日生理かな?wアイス食べる?w","ゆいちゃんの3日目の生理の血は少ししょっぱいね♡ww"))
 text_message=str(text_random)
 await message.reply(text_message)

@bot.tree.command(name="hurupa",description="VALORANTのキャラをランダムで決める(フルパ)")
async def hurupa(interaction: discord.Interaction):
   due=random.choice(("ジェット","レイズ","フェニックス","レイナ","ヨル","ネオン","アイソ"))
   senti=random.choice(("セージ","キルジョイ","サイファー","デッドロック","チェンバー","ヴァイス"))
   initiator=random.choice(("ソーヴァ","KAY/O","スカイ","フェイド","ブリーチ","ゲッコー"))
   controller=random.choice(("ブリム","アストラ","ヴァイパー","オーメン","ハーバ","クローヴ"))
   amari=random.choice(("ジェット","レイズ","フェニックス","レイナ","ヨル","ネオン","アイソ","セージ","キルジョイ","サイファー","デッドロック","チェンバー","ヴァイス","ソーヴァ","KAY/O","スカイ","フェイド","ブリーチ","ゲッコー","ブリム","アストラ","ヴァイパー","オーメン","ハーバ","クローヴ"))
   text_message=str(due+"、"+senti+"、"+initiator+"、"+controller+"、"+amari)
   await interaction.response.send_message(text_message)

intents = discord.Intents.default()
intents.members = True

HEADERS = {
    'Authorization': f'Bot {TOKEN}',
    'Content-Type': 'application/json'
}
@bot.tree.command(name="timeout",description="指定したユーザーをタイムアウト")
@app_commands.describe(member="timeout member", duration="秒")
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int):
    timeout_duration = timedelta(seconds=duration)
    end_time = (datetime.now(timezone.utc) + timeout_duration).isoformat()

    url = f"https://discord.com/api/v10/guilds/{interaction.guild_id}/members/{member.id}"

    json_data = {
        "communication_disabled_until": end_time
    }
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=json_data, headers=HEADERS) as response:
            if response.status == 200:
                await interaction.response.send_message(f'{member.mention} がタイムアウトされました。時間： {duration // 60} 分')
            else:
                await interaction.response.send_message(f'タイムアウトに失敗しました。 {member.display_name}: {response.status} - {await response.text()}')
@bot.tree.command(name="ban", description="指定したメンバーをBANします。")

@app_commands.describe(member="BANするメンバー", reason="BANの理由")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.ban_members:
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.name} がBANされました。理由: {reason}")
        except Exception as e:
            await interaction.response.send_message(f"エラー: {e}")
    else:
        await interaction.response.send_message("BANする権限がありません。")
image_list = [
    "https://cdn.discordapp.com/attachments/1306889720185360457/1316013321039904798/1297746895715831912remix-1729511878909.png?ex=67957caa&is=67942b2a&hm=26c7fbc432f5c61e2decea84291f66bb018e03b2c2b11f062fcd4537e536b161&",
    "https://cdn.discordapp.com/attachments/1306889720185360457/1316578022291410974/IMG_6580.jpg?ex=67959055&is=67943ed5&hm=1e4a21c6d50e4c6e3c778271c283ef1521f228a0bdb9dc42240c3d254b3f8c96&",
    "https://cdn.discordapp.com/attachments/1232685016190812373/1332672772496691291/PXL_20240314_032316294.jpg?ex=67961bbc&is=6794ca3c&hm=34d5278e442a720e7ebbb4cd4303d8bc481e51e18b7551f62a9fcee6878f7099&",
    "https://cdn.discordapp.com/attachments/1230409136106373131/1332672808450527334/IMG_3455.jpg?ex=67961bc5&is=6794ca45&hm=772bf1d7df5ba775a4a40c9246aed7d1bcd6f59e3795b13ec0a372fe668f0d7f&",
    "https://cdn.discordapp.com/attachments/1230409136106373131/1332672808924221471/IMG_3848.jpg?ex=67961bc5&is=6794ca45&hm=9450a9dce670519bf96ef196e5608e8871d2afad5a73c57f05afb40c8026da3f&",
    "https://cdn.discordapp.com/attachments/1230409136106373131/1332672809918267453/IMG_3459.jpg?ex=67961bc5&is=6794ca45&hm=814b8dd0468841013be542588b2a757649d937ed704bf608d36b1ad42a9e0b2d&",
    "https://cdn.discordapp.com/attachments/1230409136106373131/1332672810535092336/IMG_1795.png?ex=67961bc5&is=6794ca45&hm=8e6cc965fe13a5c7f68e12fa7286229a4301a615d48e9efb6bcbb0350b5e98da&",
    "https://cdn.discordapp.com/attachments/1010395994841690134/1332673473981710406/IMG_1967.jpg?ex=67961c64&is=6794cae4&hm=3ac4714c1935327c2aebfbcc5c6357f51cdd527577517f7388e74dac4bfba74f&",
    "https://cdn.discordapp.com/attachments/1010395994841690134/1332673630039183422/1716879781992.jpg?ex=67961c89&is=6794cb09&hm=1b899a385511ff26715e053f816660de6e0870b52038f8f28c2b3f41f426ced6&",
]

message_list1="放課後教室の中で俺と君は2人きりなにも起こらないはずもなくそっと、まおに声をかける「まーお！」\n下を向いている君は俺と目線を合わせ俺を見つめ顔を赤らめる、 (可愛い、♡♡心の中でそう思う)口には出せないこの気持ちを胸に秘めたとき、\n俺の体はもう動いている後ろからいきなり抱きつき手を胸にまわす舐めまわすようにブラホックを外しパイを触る後ろからでも安易に想像できる君の表情僕の吐息とまおの息が混ざり合うとき俺とまおはひとつになるだよ♡\nあー可愛いねまお本当にだぁいすき頭の中はまおでいっぱい気づいた時にはバックで君をハメていた俺は一振一振に赤ちゃん作っちゃおうと声を出しそのたんびに君の子宮が俺を締め付ける(子宮で返事してるんだね♡)\n後ろからのバックハグで愛を感じながら中に出すで10秒間全て出し切るまおの膣から俺の性器を伝たる精液が溢れてる\n後ろから耳に思いを込めてまお、愛してるよと言葉をかける\n明日もしようね♡"


message_list2="まおﾁｬﾝ💗❗🎵(^_^)まおﾁｬﾝも今日も2時までお仕事カナ❗❓（￣ー￣?）このホテル🏨、すごいキレイ（笑）😃(^o^)なんだって😚😄僕と一緒に行こうよ😍ﾅﾝﾁｬｯﾃ(^з<)(^o^)😍"


message_list3="放課後教室の中で俺と君は2人きりなにも起こらないはずもなくそっと、まおに声をかける「まーお！下を向いている君は俺と目線を合わせ俺を見つめ顔を赤らめる、 (可愛い、♡♡心の中でそう思う)口には出せないこの気持ちを胸に秘めたとき、\n俺の体はもう動いている後ろからいきなり抱きつき手を胸にまわす舐めまわすようにブラホックを外しパイを触る後ろからでも安易に想像できる君の表情僕の吐息とまおの息が混ざり合うとき俺とまおはひとつになるだよ♡\nあー可愛いねまお本当にだぁいすき頭の中はまおでいっぱい気づいた時にはバックで君をハメていた俺は一振一振に赤ちゃん作っちゃおうと声を出しそのたんびに君の子宮が俺を締め付ける(子宮で返事してるんだね♡)\n後ろからのバックハグで愛を感じながら中に出すで10秒間全て出し切るまおの膣から俺の性器を伝たる精液が溢れてる\n後ろから耳に思いを込めてまお、愛してるよと言葉をかける\n明日もしようね♡"


message_list4="「まおたんこれ！おとしたにょ！」　「松尾さんありがとう...」まおたんはそういいながら俺にはにかんだ「気がした」　　次の日まおたんがあのキーホルダーを付けてないのを見て、「まおたん俺が拾ったあのキーホルダーどうしたの？」そう聞いたときまおたんは「またなくしちゃったんだ」と言った　でも俺は知ってるよ、まおたんがキーホルダーをゴミ箱に捨てたことを　まおたんどうして...俺はそう考えたが一つ考えを思いついた　「まおたんを自分のものにすればいいんだ」と　「俺だけのまおちゃん...松尾まおにしてあげるからね♡」　　　　　　　　　　　　　　　　まおちゃんの家と帰り道は調べた…家族もこの時間はいないはず…　　　「まおちゃん今から松尾まおちゃんにしてあげるからね♡」　学校終わりおないきはまおちゃんの家に向かっていった。"


message_list5="こちらが 手塚はるま無双さんの\n濃厚手塚はるまナナミトッピングです\nうっひょ～～～～～～！\n着席時 コップに水垢が付いていたのを見て\n大きな声を出したら なおきさんからの誠意で\nコンドームをサービスしてもらいました！\n俺のハメ撮りでこのホテル潰す事だってできるんだぞって事で\nいただきま～～～～す！まずは体から\nコラ～！\nこれでもかって位サラサラな肌には\nローションが塗られており 怒りのあまり\nテンガを全部倒してしまいました～！\nすっかりホテル側も立場を弁え 誠意のディルドを貰った所で\nお次に 圧倒的存在感の性器を\n啜る～！ 殺すぞ～！\nワシワシとした食感の中には、毛が入っており\nさすがのはるまも フロントに入って行ってしまいました～！\nちなみに、なおきさんが土下座している様子は ぜひサブチャンネルをご覧ください"


message_list6="まおちゃんの顔が青ざめていくのをマスク越しでもわかるよ、けどねまおちゃん俺の愛はもう我慢できない急いで家に入る君その時僕は2回の君の部屋へと壁を登る\n「つーいた！ここがまおちゃんの部屋かぁ」気づいた時にはまおちゃんの布団の上にうずくまって腰を振りまくっていたまおちゃんの上がった息が下の階段から聞こえてくる俺は上にいるのにね♡\n扉が開く俺はもう下の服は脱いだまおがバックをおろし布団に座るすかさず君の布団に隠れていた僕は「まーおたん！！と後ろから抱きかかる」キャ！と慌てふためく君の口を押えて下半身を擦り付け制服のスカートを貫通させる勢いで擦り付け背中に1発出してしまった、\nもう止まらない\nそのまま完全に孕ませまおたん苗字付けモードに入った俺はまおちゃんの口を押えている手から声が振動しているのを感じて興奮する「まおちゃん叫んでるんだぁ♡」、まおちゃんの布団の上に押し倒してフル勃起した俺のをマスクをずらさせてまおちゃんの口まおちゃんに無理やり突っ込むジュボジュボ音を立てながら口で僕のを舐めてくる目からは涙がでている君そんなに嬉しいのかな？口の中をパンパンにするほど射精したらすかさずまおちゃんのスカートをずらしまだ濡れてない君の名器に指を突っ込むそのまま叫ばせないように流れるように頭に枕を押し付けて窒息させる、時々顔を見て泣き叫ぶ君を見て股間から我慢汁が漏れる。\n「そろそろ濡れてきたかな」\nビンビンにたった僕のを君のにぶち込む、入れ込んだ瞬間君の子宮が疼いて僕の精子を欲しているのが分かる、松尾まおにしてあげるからね、♡\n君の叫び声と俺の膣を突く音のハーモニーが堪らない、泣きながら抵抗するところもかわぁいい♡\nそのまま高速ピストンをして中に\n「孕めオラァ！！！と声と共に全てをぶち込む」\nﾋﾞｭﾙﾙﾙﾙﾙビューー！！！！！！！！\n「はぁはぁ...///」俺は息が漏れる\nまおちゃんが全てを察して静かに号泣している。\nそこでそっと俺はまおちゃんの耳元に耳を舐めながら\n「まおちゃんいいや松尾まおちゃん僕との赤ちゃんの名前は何にしようか」あー本当にだぁいすき\n泣いている中出しされた君を横に\nそろそろバレるとまずいので窓からチャリに跨り家に帰る\nあーまおちゃん本当に大好きだよこれからは一緒に子育て頑張ろうね♡"


message_list7="おないき女説＜ー検証しろ！\nなおき\n出すよ\n中道\n出すよ\nBy手塚"


message_list8="第1話 四中工へようこそ!\n第2話 おすすめされた電気科...!\n第3話 話しかけてくれた優しそうな先生!\n第4話 これがリア友…!?\n第5話 初めての実習!\n第6話 単位0と言われて\n第7話 友達より大切なひと\n第8話 誘惑のレポート代行\n第9話 プライベート補修\n第10話 遅刻\n第11話 転校\n最終話 四中工へようこ"

message_list9="なおき曰く\n膨らみから想像できる程よいおっぱいの大きさ。APEXに誘った時のあの顔バトミントンで見た、丁寧に剃られているであろう脇。この脇から下の剃られ具合も簡単に想像できる。キッツキツのパイパンまんこにﾊﾟﾝﾊﾟﾝﾊﾟﾝおそらく俺は3振りでイってしまうだろう。中出しされて頬を赤らめるまお。子供にはなんて名前つけようね、と耳もとで囁き可愛い唇にそっとキス。まお、絶対幸せにするからね。\nByなおき"

message_list10="ある夏の夕暮れ、街の喧騒が微かに遠のき、赤く染まった空が二人を包む。 主人公のおないきは高校1年生。 彼の澄んだ瞳は日々の憂鬱を隠しながら、ただ一つの光を探してた。それが、まあだった。\nまおは図書館の常連。彼女はいつもお気に入りの窓際の席で本を読んでいる。おないきはまおに一目惚れし、その影を追う日々が続いている。しかし、おないきは不器用な性格、彼女の前では、おならしかでづ、言葉がでない。\nある昼休み、まおが借りた本を返しに来た瞬間、おないきの心が不意に叫んだ。 「まおたん！APEX一緒にしませんか？」\n「いや、大丈夫...」 おないきの心はどん底に落ちた。そこには異様な空気間。誰も近づくことができない。まるで山口の無領空処みたいだ。帰り道、明るい空を見つめた。 沈む太陽。照らされたおないき。まるでおないきの心情を表している。\nそのとき、おないきの心の中で何かが振り返る。まおの声がふいに聞こえる。「いや、大丈夫...」\nその瞬間、おないきは確信した。俺はチー牛だと。"

message_list11="高校に入ったあの春\n俺は初めての恋をした。\nあの日窓から外を見ている君に恋をした。\n「まおたんかわいいなぁ…」まおたんを愛するの気持ちが止められなくなったあの日俺はまおたんに話しかけた。\n「まおたん！俺と一緒にエーペックスしませんか？俺ダイヤだからキャリーしてあげるよ！」\n「ちょっと、大丈夫です…」おないきは初めて自分がまおたんにキモがられていることに気づいた。\nそしてその後手塚が言ったんだ…「まおたんはボキと一緒にエーペックスするんだにょ！」\n俺はその時理解してしまった。自分はこんなチェンバー以下だと言うことを…"

message_list12="帰り道、\n「おーい！」\nそう呼ぶ声が聞こえる。\nふと後ろを振り向くとそこには\nまおがいた\nでも呼ばれているのはボキじゃないいつまでたっても仲良くなれない現状に劣等感を覚えた。駐輪場でうろたえているとまおが帰って行ってしまった、\n「あぁ」ふと声を漏らし\nあの美しい顔、体自分の物に出来たらと妄想にふけっているとふと何かが落ちているのが見えた\n見覚えのあるぬいぐるみのキーホルダー\n間違いないまおちゃんのだ\n「届けてあげなきゃ！」\nそう思い立ちぬいぐるみの匂いを嗅いだあとバックにしまってまおを追いかけるように後を急いだ"

message_list13="もうテロだろこれ\nbyあかせあつき君！"  

message_list14="待望の過去編登場ここで明かされるなおきとまおの物語\n映画公開記念の前編公開中！\nボキは、松尾。小学6年生だ。\n同じクラスのまおに恋してる。\n「あ、じゃ、私こっちだから」\nまおはそこで別れようとする。まおの家は学校からちょっと遠いところにあるらしい。ボキとまおの帰り道が分かれる交差点がある。\n「また明日な」\n「うん。ばいばい」\nボキはまおの背中が見えなくなるまでそこに立っていた。そして、見えなくなった途端に走り出した。家に着いてもまだドキドキしていた。\n「ただいまー！」\n「おかえりー！ おやつあるよ」\n「やったー！」\nボキはおやつを急いで食べる。\n「ごちそうさまでした！」\n「お粗末さまでした」\nお母さんが食器を片付ける。\n「ねえ、お母さん」\n「ん？ なに？」\n「ボキね、好きな人できたよ」\n「……え？ ……え！？」\nお母さんは持っていたお皿を落としそうになった。でも、なんとか落とさずにすんだ。そして、また洗い場にもどる。\n「……だ、だれ？」\n「まお」\n「まお……？」\n「おっと、お話は一旦ここまで！」\nボキとまおたんがラブラブになっていくまでの物語を是非劇場で！"

message_list15="今日はまおたんとはめはめするの！😡⃤   By福本\n今日はななみんとハメハメするの！😡⃤ By手塚"

message_list16="おなたんとまーおちゃんの伝説子宮エントリー物語\n深夜の都会、煌びやかなネオンの下でおなたんとまーおちゃんは出会った。その瞬間、二人の魂は運命の渦に巻き込まれた。\n「まーおちゃん、君の瞳に見える未来が、俺を呼んでいる。」\n「おなたん…私、君に委ねたい。」\nこうして二人は手を取り合い、夜の街を駆け抜け、辿り着いたのは静かなホテル。そこには人知れず伝説が眠る部屋があった。\n扉を開けると、不思議な光が二人を包み込む。ベッドの上で向かい合うと、おなたんは震える声で言った。\n「ここで始まるんだ、俺たちの物語が。」\nまーおちゃんは静かに頷き、二人はひとつになった。愛のエネルギーが迸り、まるで宇宙が生まれる瞬間のような輝きが広がった。その光は部屋を超え、街を照らし、人々の心を震わせた。\n数ヶ月後、まーおちゃんは新たな命を宿していた。それはただの命ではない。二人の愛の結晶であり、世界を変える存在だった。\n「おなたん、この子が…私たちの未来だね。」\n「ああ、まーおちゃん。これが伝説の始まりだ。」\nこうして、おなたんとまーおちゃんは、子宮を舞台に新たな冒険へと旅立つのであった。彼らの物語は永遠に語り継がれるだろう。"  

message_list17="第1話 VRCへようこそ!\n第2話 おすすめされたJPT...!\n第3話 話しかけてくれたお姉さん!\n第4話 これがフレンド…!?\n第5話 初めての女性アバター!\n第6話 メス堕ちと言われて\n第7話 フレンドより大切なひと\n第8話 誘惑のR改変\n第9話 プライベートROOM\n第10話 お塩\n第11話 転生\n最終話 VRCへようこそ"

message_list18="実は私、1日半、PC閉じてないんです！\n「VRチャット」って知ってますか？\n現実で孤立してるから\n心配しなくても電子の世界で生活できるし、ストレスもかからない！\n顔も見えなくて、お砂糖もできちゃうし、何か失敗しても責められたりする問題がないし\n彼女だって出来て何よりみんな優しいから\nむしろ、現実で生きない方が良いんです！\n「VRチャット」、みんなも試してみてねー!"


@bot.tree.command(name="onaiki", description="ランダムでおないきの写真と怪文章を送信します。※この物語は全てフィクションです。")
async def onaiki(interaction: discord.Interaction):
    if not image_list:
        await interaction.response.send_message("画像が登録されていません！", ephemeral=True)
        return
    random_image = random.choice(image_list)
    message_lists = [
        message_list1, message_list2, message_list3, message_list4, message_list5, message_list6, message_list7, message_list8, message_list9, message_list10, message_list11, message_list12, message_list13, message_list15, message_list16, message_list17, message_list18
                     ]
    random_list = random.choice(message_lists)
    embed = discord.Embed(title="おないき", description=random_list)
    embed.set_image(url=random_image)
    await interaction.response.send_message(embed=embed)

TOKEN=os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!" , intents=discord.Intents.all())

def number_to_emoji(number):
    if 1 <= number <= 9:
        return f"{chr(0x0030 + number)}\uFE0F\u20E3"
    return None

@bot.event
async def on_ready ():
    activity_stetas=random.choice(("週末京都現実逃避","2:23 AM","SUMMER TRIANGLE","You and Me","10℃"))
    await bot.change_presence(activity=discord.Game(name="/help｜"f"Join server{len(bot.guilds)}｜""Listening "+activity_stetas))
    print("起動")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期")
    except Exception as e:
        print(e)
from dotenv import load_dotenv


load_dotenv()

GUILD_ID=1363034682253508740
VERIFY_ROLE_ID=1363069009968365698
TOKEN=os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- 認証ボタンの定義 ---------------- #
class VerifyButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.button(label="認証を始める", style=discord.ButtonStyle.success)
    async def start_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの認証ボタンではありません。", ephemeral=True)
            return

        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        answer = num1 + num2

        # 正解＋不正解の選択肢をランダムに生成
        options = [answer]
        while len(options) < 4:
            fake = random.randint(1, 20)
            if fake != answer and fake not in options:
                options.append(fake)
        random.shuffle(options)

        # セレクトメニューを作成
        select = discord.ui.Select(
            placeholder=f"{num1} + {num2} = ?",
            options=[
                discord.SelectOption(label=str(option), value=str(option))
                for option in options
            ]
        )

        async def select_callback(interaction_select: discord.Interaction):
            selected = int(select.values[0])
            if selected == answer:
                role = interaction.guild.get_role(VERIFY_ROLE_ID)
                await interaction.user.add_roles(role)
                await interaction_select.response.send_message("✅ 正解です！ロールを付与しました。", ephemeral=True)
            else:
                await interaction_select.response.send_message("❌ 不正解です！再度やり直してください。", ephemeral=True)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message(
            content="以下の選択肢から正しい答えを選択してください。",
            view=view,
            ephemeral=True
        )

# ---------------- スラッシュコマンド ---------------- #
@bot.tree.command(name="verify", description="...")
@app_commands.guilds(discord.Object(id=GUILD_ID))  # ギルド限定
async def verify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="",
        description="## 📑 簡単な計算をして認証をしてください。",
        color=0x00ffcc
    )
    embed.set_image(url="https://i.pinimg.com/originals/78/41/b9/7841b9967f7bb4cd5ef200f24ee04adb.gif")
    view = VerifyButton(interaction.user.id)
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="r")
async def rules(interaction: discord.Interaction):
    embed = discord.Embed(
        description="## 📌 利用規約・注意事項【Crafted Bots】",
        color=3447003
    )

    embed.add_field(
        name="🎉 ようこそ、Crafted Bots -【全ての代行サービスを】へ",
        value="以下の利用規約・注意事項をご確認の上、ご利用をお願いいたします。",
        inline=False
    )
    embed.add_field(
        name="✅ ご利用にあたって",
        value="・本サーバーは、BOT販売・代行・設定支援などを目的とした開発者支援型サービスサーバーです。\n・全てのユーザーは以下の利用規約に同意したものとみなします。",
        inline=False
    )
    embed.add_field(
        name="🛡️ サービス全般について",
        value="・提供するBOT・ファイル・設定等は、商用利用不可／個人利用限定です。（※別途許可がある場合を除く）\n・再配布、転売、複製しての配布行為は禁止です。\n・各サービスは「現状有姿」で提供しており、動作保証・永久保証は行いません。",
        inline=False
    )
    embed.add_field(
        name="🧾 購入・依頼に関する注意事項",
        value="・購入後のキャンセル・返金は基本不可とします。\n・BOT起動代行などの継続サービスについては、料金未納の場合はサービスを停止させていただきます。",
        inline=False
    )
    embed.add_field(
        name="🧑‍⚖️ 禁止事項",
        value="・他利用者・運営への迷惑行為、誹謗中傷、荒らし行為\n・他サービスやコミュニティへの過度な勧誘・宣伝\n・サーバーの情報・ファイルを許可なく外部に公開する行為",
        inline=False
    )
    embed.add_field(
        name="⚠️ 運営からのお願い",
        value="・すべてのやりとりは、円滑かつ丁寧なコミュニケーションを心がけてください。",
        inline=False
    )
    embed.add_field(
        name="📝 改定について",
        value="・本利用規約は予告なく変更・更新される場合があります。",
        inline=False
    )
    embed.set_footer(text="Crafted Bots運営チーム")
    embed.set_author(name="py", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buy")
async def buy(interaction: discord.Interaction):
    embed = discord.Embed(
        description="## 📌 ご購入される方へ【Crafted Bots】"
    )
    embed.add_field(
        name="Bot作成中のため数日間DMの方で依頼をおねがい致します。",
        value="",
        inline=False
    )
    embed.set_image(url="https://i.pinimg.com/originals/91/1f/f6/911ff6a5913ed95b4af78ab454184e88.gif")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="n")
async def consult(interaction: discord.Interaction):
    embed = discord.Embed(
        description="## 📌 質問・相談・見積もりされる方へ【Crafted Bots】"
    )
    embed.add_field(
        name="Bot作成中のため数日間DMの方で、質問・相談・見積もりをおねがい致します。",
        value="",
        inline=False
    )
    embed.set_image(url="https://i.pinimg.com/originals/ab/76/de/ab76def5a6d4bd6cef3c3bc614122ed8.gif")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hello", description="...")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("hello")

# ---------------- 起動時イベント ---------------- #
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ {len(synced)}個のコマンドをギルド {GUILD_ID} に同期しました。")
    except Exception as e:
        print(f"同期エラー: {e}")
        
keep_alive()
  
bot.run(TOKEN)