import discord
from discord.ext import commands

class ActiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="active")
    @commands.has_permissions(manage_roles=True)
    async def active(self, ctx):
        """
        Assigns the 'Active Member' role to every member who has any of the roles:
        'Class 9', 'Class 10', 'Class 11', 'Class 12'.
        """
        guild = ctx.guild
        role_names = ["Class 9", "Class 10", "Class 11", "Class 12"]
        active_role = discord.utils.get(guild.roles, name="Active Member")
        if not active_role:
            active_role = await guild.create_role(name="Active Member")

        count = 0
        for member in guild.members:
            if any(discord.utils.get(member.roles, name=role) for role in role_names):
                if active_role not in member.roles:
                    try:
                        await member.add_roles(active_role, reason="Marked as active member")
                        count += 1
                    except discord.Forbidden:
                        await ctx.send(f"Missing permissions to add role to {member.display_name}.")
        await ctx.send(f"Assigned 'Active Member' role to {count} members.")

async def setup(bot):
    await bot.add_cog(ActiveCog(bot))
