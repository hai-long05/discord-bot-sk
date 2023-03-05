import binascii

from discord.ext.commands import Context, Bot, Cog, command


class ConverterCog(Cog): 
    def __init__(self, bot: Bot):
        self.bot = bot


    @command(name='asciitobinary')
    async def asciitobinary(self, ctx: Context, *args):
        encoding = 'utf-8'
        errors = 'surrogatepass'
        to_convert = ''.join(args)
        bits = bin(int(binascii.hexlify(to_convert.encode(encoding, errors)), 16))[2:]
        return await ctx.reply(bits.zfill(8 * ((len(bits) + 7) // 8)))

    
    @asciitobinary.error
    async def binarytoascii_error(self, ctx, error):
        await ctx.reply("Invalid input")


    @command(name='binarytoascii')
    async def binarytoascii(self, ctx: Context, *args):
        encoding = 'utf-8'
        errors = 'surrogatepass'
        bits = ''.join(args)
        n = int(bits, 2)
        return await ctx.reply(self.int2bytes(n).decode(encoding, errors))


    def int2bytes(self, i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


    @binarytoascii.error
    async def binarytoascii_error(self, ctx, error):
        await ctx.reply("Invalid input")