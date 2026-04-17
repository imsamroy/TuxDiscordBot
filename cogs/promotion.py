import discord
from discord.ext import commands

ROLE_MAP = {
    "Class 9": "Class 10",
    "Class 10": "Class 11",
    "Class 11": "Class 12",
    "Class 12": "Passout"
}

class PromotionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def promote(self, ctx):
        guild = ctx.guild
        print(f"promote command called by {ctx.author} in guild {guild.name}")
        member_count = len(guild.members)
        print(f"Total members in guild: {member_count}")
        promoted_count = 0
        for member in guild.members:
            print(f"Checking member: {member.display_name} ({member.id})")
            for old_role, new_role in ROLE_MAP.items():
                old = discord.utils.get(guild.roles, name=old_role)
                new = discord.utils.get(guild.roles, name=new_role)
                if old in member.roles:
                    print(f"Promoting {member.display_name} from {old_role} to {new_role}")
                    await member.remove_roles(old)
                    await member.add_roles(new)
                    # If promoting from Class 12 to Passout, remove Active Member role if present
                    if old_role == "Class 12" and new_role == "Passout":
                        active_role = discord.utils.get(guild.roles, name="Active Member")
                        if active_role and active_role in member.roles:
                            await member.remove_roles(active_role, reason="Graduated to Passout")
                            print(f"Removed 'Active Member' from {member.display_name} (now Passout)")
                    promoted_count += 1
                    break  # Stop after first promotion
        print(f"Total promoted: {promoted_count}")
        await ctx.send(f"Promotion complete! Promoted {promoted_count} members.")

async def setup(bot):
    await bot.add_cog(PromotionCog(bot))
