import discord
from discord.ext import commands
from typing import TYPE_CHECKING,Optional
import datetime
import submits
if TYPE_CHECKING:
    from bot import Bot

class Example(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    def get_time(self,data):
        times = datetime.datetime.fromtimestamp(data).strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        return times

    @commands.command(name="todo")
    async def todo(self, ctx: commands.Context,query:Optional[int] = None):
        pend = submits.submits
        if query == None:
            if len(pend) == 0:
                embed = discord.Embed(title="KOREANBOTS 대기 목록",
                                      description="현재 대기중인 봇이 없습니다.")
                return await ctx.reply(embed=embed)
            num = 0
            embed = discord.Embed(title="KOREANBOTS 대기 목록")
            for i in pend:
                num += 1
                embed.add_field(
                    name=f"{num}번째",
                    value=f"ID: {i.id}",
                    inline=False
                )
            return await ctx.reply(embed=embed)
        for i in pend:
            if i.id == query:
                print(i.date)
                embed = discord.Embed(
                    title=i.id,
                    description=self.get_time(data=i.date) + f"\n[Invite](https://discord.com/oauth2/authorize?client_id={i.id}&scope=bot&permissions=0&guild_id=653083797763522580&disable_guild_select=true)"
                )
                return await ctx.reply(embed=embed)

        try:
            if query != 0:
                datas = pend[query-1]
                embed = discord.Embed(
                    title=datas.id,
                    description=self.get_time(
                        data=datas.date) + f"\n[Invite](https://discord.com/oauth2/authorize?client_id={datas.id}&scope=bot&permissions=0&guild_id=653083797763522580&disable_guild_select=true)"
                )
                return await ctx.reply(
                    embed=embed
                )
            elif query >= 0:
                return await ctx.reply("최소 1번째부터 찾을수있습니다.")
        except IndexError:
            return await ctx.reply(f"`{query}`번째 대기봇을 찾지못하였습니다.")

    @commands.command(name="approve")
    async def approve(self,ctx:commands.Context,query:int):
        pend = submits.submits
        approve=submits.approved_submits
        for i in pend:
            if i.id == query:
                pend.remove(i)
                approve.append(i)
                return await ctx.reply(f"`{i.id}` 봇을 승인하였습니다.")
        return await ctx.reply(f"`{query}` 봇을 찾지못하여 승인하지 못하였습니다.")

    @commands.command(name="deny")
    async def deny(self,ctx:commands.Context,query:int):
        pend = submits.submits
        for i in pend:
            if i.id == query:
                pend.remove(i)
                return await ctx.reply(f"`{i.id}` 봇을 거부하였습니다.")
        return await ctx.reply(f"`{query}` 봇을 찾지못하여 거부하지 못하였습니다.")


def setup(bot: "Bot"):
    bot.add_cog(Example(bot))
