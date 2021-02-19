#!/usr/bin/env python3

import discord
from discord.ext import commands
from extras import *

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

client = commands.Bot(command_prefix="s?")
class MyHelpCommand(commands.DefaultHelpCommand):
	def __init__(self, **options):
		self.paginator = commands.Paginator()
		super().__init__(**options)
		self.paginator.prefix = ""
		self.paginator.suffix = ""
		self.no_category = "Commands"
	def add_indented_commands(self, commands, *, heading, max_size=None):
		if not commands:
			return

		self.paginator.add_line(heading)
		max_size = max_size or self.get_max_size(commands)

		get_width = discord.utils._string_width
		for command in commands:
			name = command.name
			width = max_size - (get_width(name) - len(name))
			entry = '{0}**{1:<{width}}**: {2}'.format(self.indent * ' ', name, command.short_doc, width=width)
			self.paginator.add_line(self.shorten_text(entry))
	def get_ending_note(self):
		command_name = self.invoked_with
		return "Type {0}{1} command for more info on a command.\n".format(self.clean_prefix, command_name)
	async def send_pages(self):
		destination = self.get_destination()
		e = discord.Embed(color=discord.Color.blurple(), description='')
		for page in self.paginator.pages:
			e.description += page
		await destination.send(embed=e)

client.help_command = MyHelpCommand()
@client.event
async def on_ready():
	print("logged in as {0.user}".format(client))

@client.command(aliases=["sp"],description="Spoilers either your previous message's attachments, your previous message's text, the rest of the message's text, or the message's attachments.",brief="Spoilers your stuff",category="d")
async def spoiler(ctx,*text):
	use_prev_msg = True if text == () and len(ctx.message.attachments) == 0 else False
	if use_prev_msg:
		async for message in ctx.channel.history(limit=10):
			if message.author != ctx.author:
				continue
			if message == ctx.message:
				continue
			msg = message
			break
	else:
		msg = ctx.message
	txt = msg.content if msg != ctx.message else " ".join(text)
	images = await attachments_to_files(msg.attachments,True)
	await msg.delete()
	if use_prev_msg:
		await ctx.message.delete()
	if len(images) == 0:
		txt = f"|| {txt} ||"
	imitated = ctx.author
	avatar = await imitated.avatar_url_as(format="png").read()
	hook = await ctx.channel.create_webhook(name=imitated.display_name,avatar=avatar)
	await hook.send(content=txt,files=images)
	await hook.delete()

@client.command(aliases=["sw"])
async def swear(ctx,*text):
	pass


client.run(token)