import discord
from discord.ext import commands, tasks
import asyncio
import urllib.parse
import random
from datetime import datetime, timedelta, timezone
import os
from flask import Flask
from threading import Thread

# --- CẤU HÌNH MÚI GIỜ VIỆT NAM (UTC+7) ---
VN_TZ = timezone(timedelta(hours=7))

# --- CẤU HÌNH WEB SERVER CHO RENDER & UPTIMEROBOT ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- CẤU HÌNH BOT ---
TOKEN = os.getenv("DISCORD_TOKEN")

WELCOME_CHANNEL_ID = 1379468628549963899  
GOODBYE_CHANNEL_ID = 1449415666233774102  
TICKET_CATEGORY_ID = 1483484606735974491  
MANAGER_CHANNEL_ID = 1535624430699417681
HISTORY_CHANNEL_ID = 1535700411384856688

# --- CẤU HÌNH TÍNH NĂNG PICK ROLE ---
MEMBER_ROLE_NAME = "Member"              # Tên role Member cần kiểm tra
PICK_ROLE_CHANNEL_ID = 1449337984779550720 # ID kênh pick role để bot tag vào DM

# --- CẤU HÌNH THÔNG TIN THANH TOÁN ---
BANK_ID = "MB"          
BANK_ACCOUNT = "999999999498"  
ACCOUNT_NAME = "NGUYEN THANH TUAN" 

# --- CẤU HÌNH DANH MỤC MUA ACCOUNT ---
BUY_CATEGORIES_DATA = {
    "acc-capcut-pro": {
        "name": "Mua Tài Khoản CapCut Pro",
        "emoji": "🛒",
        "style": discord.ButtonStyle.primary,
        "prices": [
            ("Tài Khoản CapCut Standard (1 Tháng)", 55000, "Giá: 55.000 VNĐ"),
            ("Tài Khoản CapCut Standard (12 Tháng)", 799000, "Giá: 799.000 VNĐ"),
            ("Tài Khoản CapCut Pro (1 Tháng)", 89000, "Giá: 89.000 VNĐ"),
            ("Tài Khoản CapCut Pro (12 Tháng)", 859000, "Giá: 859.000 VNĐ"),
            ("Tài Khoản CapCut Ultra (1 Tháng)", 1450000, "Giá: 1.450.000 VNĐ"),
            ("Tài Khoản CapCut Ultra (12 Tháng)", 13989000, "Giá: 13.989.000 VNĐ")
        ]
    },
    "acc-canva-pro": {
        "name": "Mua Tài Khoản Canva Pro",
        "emoji": "🛒",
        "style": discord.ButtonStyle.primary,
        "prices": [
            ("Tài Khoản Canva Pro (1 Năm)", 150000, "Giá: 150.000 VNĐ")
        ]
    },
    "acc-youtube-premium": {
        "name": "Mua Tài Khoản Youtube Premium",
        "emoji": "🛒",
        "style": discord.ButtonStyle.primary,
        "prices": [
            ("Youtube Premium (1 Tháng)", 30000, "Giá: 30.000 VNĐ")
        ]
    },
    "acc-tiktok-clone": {
            "name": "Mua Tài Khoản TikTok Clone",
            "emoji": "🛒",
            "style": discord.ButtonStyle.primary,
            "prices": [
                ("TikTok Clone (1 Con)", 5000, "Giá: 5.000 VNĐ")
            ]
    },
    "acc-gmail-clone": {
            "name": "Mua Tài Khoản Gmail (Reg Trên 1 Tháng)",
            "emoji": "🛒",
            "style": discord.ButtonStyle.primary,
            "prices": [
                ("Gmail Reg Trên 1 Tháng (1 Con)", 4000, "Giá: 4.000 VNĐ")
            ]
    }
}

# --- CẤU HÌNH DANH MỤC RANDOM ACCOUNT ---
RANDOM_CATEGORIES_DATA = {
    "random-facebook-co-1": {
        "name": "Random Tài Khoản Facebook Cổ (2012-2022)",
        "emoji": "🎲",
        "style": discord.ButtonStyle.primary,
        "prices": [
            ("Random FB Cổ 2012-2022", 20000, "Giá: 20.000 VNĐ")
        ]
    },
    "random-facebook-co-2": {
        "name": "Random Tài Khoản Facebook Cổ (2008-2016)",
        "emoji": "🎲",
        "style": discord.ButtonStyle.primary,
        "prices": [
            ("Random FB Cổ 2008-2016", 50000, "Giá: 50.000 VNĐ")
        ]
    },
    "random-tiktok-us": {
        "name": "Random Tài Khoản TikTok US",
        "emoji": "🎲",
        "style": discord.ButtonStyle.primary,
        "prices": [
            ("Random TikTok US", 15000, "Giá: 15.000 VNĐ")
        ]
    }
}

intents = discord.Intents.default()
intents.members = True  
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

welcome_channels = {}
goodbye_channels = {}

# --- HÀM HỖ TRỢ GỬI DM KIỂM TRA ROLE ---
async def check_and_send_pick_role_dm(member):
    if member.bot:
        return
    
    # Tìm xem member đã có role Member chưa
    member_role = discord.utils.get(member.roles, name=MEMBER_ROLE_NAME)
    if not member_role:
        try:
            channel_mention = f"<#{PICK_ROLE_CHANNEL_ID}>"
            dm_content = f"Bạn chưa Pick Role tại {channel_mention} để hiển thị và sử dụng toàn vẹn chức năng của máy chủ, hãy pick role Member nhé!"
            await member.send(dm_content)
        except Exception:
            # Trường hợp thành viên chặn tin nhắn riêng (DM) từ bot
            pass

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập thành công với tên: {bot.user}")
    if not background_check_roles.is_running():
        background_check_roles.start()

# --- TASK TỰ ĐỘNG KIỂM TRA TOÀN BỘ THÀNH VIÊN (CHẠY ĐỊNH KỲ 6 TIẾNG/LẦN) ---
@tasks.loop(hours=6)
async def background_check_roles():
    for guild in bot.guilds:
        # Đảm bảo bot đã cache đủ danh sách thành viên
        try:
            async for member in guild.fetch_members(limit=None):
                await check_and_send_pick_role_dm(member)
                await asyncio.sleep(1.5) # Khoảng nghỉ chống rate-limit của Discord
        except Exception as e:
            print(f"Lỗi khi quét thành viên ở server {guild.name}: {e}")

@background_check_roles.before_loop
async def before_background_check_roles():
    await bot.wait_until_ready()

# ==========================================
# LỆNH SETUP WELCOME & GOODBYE
# ==========================================

@bot.command(name="setwelcome")
@commands.has_permissions(administrator=True)
async def set_welcome(ctx):
    welcome_channels[ctx.guild.id] = ctx.channel.id
    await ctx.send(f"✅ Đã thiết lập kênh {ctx.channel.mention} làm **kênh chào mừng** thành viên thành công!")

@bot.command(name="setgoodbye")
@commands.has_permissions(administrator=True)
async def set_goodbye(ctx):
    goodbye_channels[ctx.guild.id] = ctx.channel.id
    await ctx.send(f"✅ Đã thiết lập kênh {ctx.channel.mention} làm **kênh tạm biệt** thành viên thành công!")

# --- LỆNH THỦ CÔNG CHO ADMIN KIỂM TRA LẠI TOÀN BỘ SERVER ---
@bot.command(name="checkrole")
@commands.has_permissions(administrator=True)
async def manual_check_role(ctx):
    await ctx.send("🔄 Đang tiến hành quét toàn bộ thành viên chưa pick role và gửi tin nhắn riêng...")
    count = 0
    async for member in ctx.guild.fetch_members(limit=None):
        if not member.bot:
            member_role = discord.utils.get(member.roles, name=MEMBER_ROLE_NAME)
            if not member_role:
                try:
                    channel_mention = f"<#{PICK_ROLE_CHANNEL_ID}>"
                    await member.send(f"Bạn chưa Pick Role tại {channel_mention} để hiển thị và sử dụng toàn vẹn chức năng của máy chủ, hãy pick role Member nhé!")
                    count += 1
                    await asyncio.sleep(1.5)
                except Exception:
                    pass
    await ctx.send(f"✅ Đã hoàn tất quét! Đã gửi thông báo nhắc nhở tới {count} thành viên chưa pick role.")


# ==========================================
# TÍNH NĂNG 1: CHÀO MỪNG & TẠM BIỆT & AUTO CHECK ROLE
# ==========================================

@bot.event
async def on_member_join(member):
    # Tự động gửi DM nhắc nhở pick role khi thành viên mới vào
    await check_and_send_pick_role_dm(member)

    channel_id = welcome_channels.get(member.guild.id, WELCOME_CHANNEL_ID)
    channel = member.guild.get_channel(channel_id)
    
    if channel:
        current_time_str = datetime.now(VN_TZ).strftime("%d/%m/%Y lúc %H:%M:%S")
        
        embed = discord.Embed(
            title=f"👋 CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI {member.guild.name}",
            description=(
                f"Xin chào {member.mention}! Chúc bạn có những trải nghiệm vui vẻ tại Server.\n\n"
                f"💬 **CHAT Ở**: <#1379468628549963900>\n"
                f"💎 **PICK ROLE TẠI** <#1449337984779550720>\n"
                f"🛡️ **ĐỌC LUẬT MÁY CHỦ** <#1449315501787451402>"
            ),
            color=discord.Color.from_rgb(255, 100, 150)
        )
        embed.set_author(name=member.guild.name, icon_url=member.guild.icon.url if member.guild.icon else member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="https://i.pinimg.com/originals/da/79/68/da7968c54b12ba7ebf7dfd70dd1faaf2.gif")
        embed.set_footer(text=f"{member.guild.name} • {current_time_str}")
        
        await channel.send(content=f"Welcome {member.mention} to **{member.guild.name}**", embed=embed)

@bot.event
async def on_member_remove(member):
    channel_id = goodbye_channels.get(member.guild.id, GOODBYE_CHANNEL_ID)
    channel = member.guild.get_channel(channel_id)
    
    if channel:
        embed = discord.Embed(
            title="😢 Thành viên rời server",
            description=f"**{member.name}** đã rời khỏi server. Hẹn gặp lại bạn vào một ngày gần nhất!",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)


# ==========================================
# TÍNH NĂNG 2: TICKET, NÚT DANH MỤC & ADMIN MANAGER
# ==========================================

class WarrantySelect(discord.ui.Select):
    def __init__(self, ticket_channel_id: int, customer: discord.User, product_name: str, quantity: int, total_price: int, order_code: str, ticket_type: str):
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.order_code = order_code
        self.ticket_type = ticket_type

        options = [
            discord.SelectOption(label="Không bảo hành", value="0", description="Sản phẩm không áp dụng bảo hành", emoji="❌")
        ] + [
            discord.SelectOption(label=f"Bảo hành {i} tháng", value=str(i), description=f"Thời hạn bảo hành {i} tháng", emoji="🛡️")
            for i in range(1, 13)
        ]
        super().__init__(placeholder="👉 Chọn thời gian bảo hành cho sản phẩm...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        months = int(self.values[0])
        if months == 0:
            warranty_text = "Không bảo hành"
        else:
            warranty_text = f"{months} tháng"

        modal = AccountInputModal(
            self.ticket_channel_id, 
            self.customer, 
            self.product_name, 
            self.quantity, 
            self.total_price,
            warranty_text,
            self.order_code,
            self.ticket_type
        )
        await interaction.response.send_modal(modal)

class WarrantySelectView(discord.ui.View):
    def __init__(self, ticket_channel_id: int, customer: discord.User, product_name: str, quantity: int, total_price: int, order_code: str, ticket_type: str):
        super().__init__(timeout=60)
        self.add_item(WarrantySelect(ticket_channel_id, customer, product_name, quantity, total_price, order_code, ticket_type))

class AccountInputModal(discord.ui.Modal, title="Gửi thông tin tài khoản cho khách"):
    username_input = discord.ui.TextInput(label="Tài khoản của bạn", placeholder="Nhập tài khoản...", required=True)
    password_input = discord.ui.TextInput(label="Mật khẩu của bạn", placeholder="Nhập mật khẩu...", required=True)
    two_fa_input = discord.ui.TextInput(label="Mã 2FA (nếu có)", placeholder="Nhập mã 2FA...", required=False)
    token_input = discord.ui.TextInput(label="Token (nếu có)", placeholder="Nhập token...", required=False)
    cookie_input = discord.ui.TextInput(label="Cookie (nếu có)", placeholder="Nhập cookie...", required=False, style=discord.TextStyle.paragraph)

    def __init__(self, ticket_channel_id: int, customer: discord.User, product_name: str, quantity: int, total_price: int, warranty_text: str, order_code: str, ticket_type: str):
        super().__init__()
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.warranty_text = warranty_text
        self.order_code = order_code
        self.ticket_type = ticket_type

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        ticket_channel = guild.get_channel(self.ticket_channel_id)

        if not ticket_channel:
            await interaction.followup.send("❌ Không tìm thấy kênh ticket của khách hàng này!", ephemeral=True)
            return

        current_time_str = datetime.now(VN_TZ).strftime("%d/%m/%Y lúc %H:%M:%S")

        acc_text = (
            f"Cảm ơn bạn đã thanh toán, quý khách vui lòng tiến hành đăng nhập theo thông tin tài khoản được cung cấp bên dưới "
            f"(Nếu gặp bất cứ lỗi nào vui lòng trình bày rõ ở Ticket này để Admin Hoặc Support sẽ giải quyết & bảo hành ngay cho bạn)\n\n"
            f"• **Mã đơn hàng:** `{self.order_code}`\n"
            f"• **Tên sản phẩm:** {self.product_name}\n"
            f"• **Số lượng:** {self.quantity}\n"
            f"• **Giá:** {self.total_price:,} VNĐ\n"
            f"• **Thời gian bảo hành:** {self.warranty_text}\n"
            f"• **Thời gian giao:** {current_time_str}\n"
            f"• **Tài khoản của bạn:** `{self.username_input.value}`\n"
            f"• **Mật khẩu của bạn:** `{self.password_input.value}`\n"
        )
        if self.two_fa_input.value:
            acc_text += f"• **Mã 2FA (nếu có):** `{self.two_fa_input.value}`\n"
        if self.token_input.value:
            acc_text += f"• **Token (nếu có):** `{self.token_input.value}`\n"
        if self.cookie_input.value:
            acc_text += f"• **Cookie (nếu có):** `{self.cookie_input.value}`\n"

        embed = discord.Embed(
            title="📦 THÔNG TIN TÀI KHOẢN ĐÃ GIAO",
            description=acc_text.replace(",", "."),
            color=discord.Color.green()
        )
        
        await ticket_channel.send(content=f"{self.customer.mention}", embed=embed)

        try:
            dm_embed = discord.Embed(
                title="📦 THÔNG TIN TÀI KHOẢN ĐÃ GIAO",
                description=acc_text.replace(",", "."),
                color=discord.Color.green()
            )
            await self.customer.send(embed=dm_embed)
        except Exception:
            pass  

        # --- GỬI LỊCH SỬ MUA HÀNG VÀO KÊNH LỊCH SỬ ---
        history_channel = guild.get_channel(HISTORY_CHANNEL_ID)
        if history_channel:
            user_id_str = str(self.customer.id)
            if len(user_id_str) > 4:
                masked_user_id = user_id_str[:1] + "******" + user_id_str[-1:]
            else:
                masked_user_id = user_id_str[0] + "******" + user_id_str[-1]
            
            t_type = str(self.ticket_type) if self.ticket_type else "mua-acc"
            display_type = "Mua Account" if "mua" in t_type else "Random Account"
            
            history_msg = f"👤 Khách hàng {masked_user_id} vừa thanh toán và giao dịch thành công ☑️\nLoại: {display_type}\nSố lượng: {self.quantity}\nGiá: {self.total_price:,} VNĐ\nBảo hành: {self.warranty_text}\nVào lúc: {current_time_str}".replace(",", ".")
            
            history_embed = discord.Embed(
                description=history_msg,
                color=discord.Color.blue()
            )
            history_embed.set_image(url="https://i.ibb.co/Y4TM5QRM/C40-F0704-7988-4206-98-BF-5326-B8-DCF0-EF.gif")
            await history_channel.send(embed=history_embed)

        await interaction.followup.send("✅ Đã gửi thông tin tài khoản vào ticket và hộp thư riêng (DM) của khách hàng thành công!", ephemeral=True)

class ConfirmRefundView(discord.ui.View):
    def __init__(self, ticket_channel_id: int, customer: discord.User, order_code: str):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.order_code = order_code

    @discord.ui.button(label="⚠️ Xác nhận hoàn tiền", style=discord.ButtonStyle.danger, custom_id="btn_confirm_refund_final")
    async def confirm_refund(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        ticket_channel = guild.get_channel(self.ticket_channel_id)

        for child in self.children:
            child.disabled = True
        try:
            await interaction.message.edit(view=self)
        except:
            pass

        await interaction.response.send_message(f"✅ Đã gửi yêu cầu hoàn tiền cho đơn hàng `{self.order_code}` vào ticket của khách!", ephemeral=True)

        current_time_str = datetime.now(VN_TZ).strftime("%d/%m/%Y lúc %H:%M:%S")
        refund_text = (
            f"Đơn hàng của quý khách `{self.order_code}` đang chờ hoàn tiền (Thời gian yêu cầu: {current_time_str})\n"
            f"Quý khách vui lòng gửi **Thông tin ngân hàng** hoặc **Ví điện tử** chính xác của mình để được hoàn tiền nhanh nhất (Có thể gửi mã QR)"
        )
        refund_embed = discord.Embed(
            title="💸 THÔNG BÁO HOÀN TIỀN ĐƠN HÀNG",
            description=refund_text,
            color=discord.Color.orange()
        )

        if ticket_channel:
            await ticket_channel.send(content=f"{self.customer.mention}", embed=refund_embed)


class AdminActionView(discord.ui.View):
    def __init__(self, ticket_channel_id: int, customer: discord.User, order_code: str, product_name: str, quantity: int, total_price: int, ticket_type: str):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.order_code = order_code
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.ticket_type = ticket_type

    @discord.ui.button(label="✅ Xác nhận đã nhận tiền", style=discord.ButtonStyle.green, custom_id="btn_admin_confirm_money")
    async def confirm_money(self, interaction: discord.Interaction, button: discord.ui.Button):
        next_view = AdminPostConfirmView(self.ticket_channel_id, self.customer, self.order_code, self.product_name, self.quantity, self.total_price, self.ticket_type)
        await interaction.message.edit(view=next_view)
        await interaction.response.send_message(f"✅ Đã xác nhận nhận tiền đơn hàng `{self.order_code}`! Bây giờ bạn có thể chọn Gửi tài khoản hoặc Hoàn tiền.", ephemeral=True)

        current_time_str = datetime.now(VN_TZ).strftime("%d/%m/%Y lúc %H:%M:%S")
        guild = interaction.guild
        ticket_channel = guild.get_channel(self.ticket_channel_id)
        
        success_text = (
            f"✅ **ĐÃ XÁC NHẬN NẠP TIỀN / THANH TOÁN THÀNH CÔNG**\n"
            f"• Mã đơn hàng: `{self.order_code}`\n"
            f"• Sản phẩm: **{self.product_name}**\n"
            f"• Số lượng: **{self.quantity}**\n"
            f"• Tổng tiền: **{self.total_price:,} VNĐ**\n"
            f"• Thời gian xác nhận: `{current_time_str}`\n\n"
            f"Admin đã xác nhận nhận được tiền của bạn. Vui lòng đợi trong giây lát để hệ thống gửi thông tin tài khoản nhé!"
        ).replace(",", ".")
        
        success_embed = discord.Embed(
            title="💰 THÔNG BÁO THANH TOÁN THÀNH CÔNG",
            description=success_text,
            color=discord.Color.green()
        )

        if ticket_channel:
            await ticket_channel.send(content=f"{self.customer.mention}", embed=success_embed)

        try:
            dm_embed = discord.Embed(
                title="💰 THÔNG BÁO NẠP TIỀN / THANH TOÁN THÀNH CÔNG",
                description=(
                    f"Xin chào {self.customer.mention},\n"
                    f"Khoản thanh toán cho đơn hàng `{self.order_code}` của bạn đã được Admin xác nhận thành công!\n\n"
                    f"• **Mã đơn hàng:** `{self.order_code}`\n"
                    f"• **Sản phẩm:** {self.product_name}\n"
                    f"• **Số lượng:** {self.quantity}\n"
                    f"• **Tổng tiền:** {self.total_price:,} VNĐ\n"
                    f"• **Thời gian:** `{current_time_str}`\n\n"
                    f"Vui lòng quay lại kênh ticket của bạn trên server để nhận tài khoản."
                ).replace(",", "."),
                color=discord.Color.green()
            )
            await self.customer.send(embed=dm_embed)
        except Exception:
            pass  

    @discord.ui.button(label="💸 Hoàn tiền", style=discord.ButtonStyle.danger, custom_id="btn_admin_refund_start")
    async def start_refund(self, interaction: discord.Interaction, button: discord.ui.Button):
        confirm_refund_view = ConfirmRefundView(self.ticket_channel_id, self.customer, self.order_code)
        await interaction.response.send_message("⚠️ Bạn có chắc chắn muốn hoàn tiền cho đơn hàng này không? Bấm nút xác nhận bên dưới:", view=confirm_refund_view, ephemeral=True)


class AdminPostConfirmView(discord.ui.View):
    def __init__(self, ticket_channel_id: int, customer: discord.User, order_code: str, product_name: str, quantity: int, total_price: int, ticket_type: str):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.order_code = order_code
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.ticket_type = ticket_type

    @discord.ui.button(label="📦 Gửi tài khoản", style=discord.ButtonStyle.green, custom_id="btn_admin_send_acc")
    async def send_account(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = WarrantySelectView(self.ticket_channel_id, self.customer, self.product_name, self.quantity, self.total_price, self.order_code, self.ticket_type)
        await interaction.response.send_message("🛡️ Vui lòng chọn thời gian bảo hành cho sản phẩm ở menu bên dưới trước khi nhập thông tin:", view=view, ephemeral=True)

    @discord.ui.button(label="💸 Hoàn tiền", style=discord.ButtonStyle.danger, custom_id="btn_admin_refund_step2")
    async def refund_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        confirm_refund_view = ConfirmRefundView(self.ticket_channel_id, self.customer, self.order_code)
        await interaction.response.send_message("⚠️ Bạn có chắc chắn muốn hoàn tiền cho đơn hàng này không? Bấm nút xác nhận bên dưới:", view=confirm_refund_view, ephemeral=True)


class QuantityModal(discord.ui.Modal, title="Nhập số lượng muốn mua"):
    quantity = discord.ui.TextInput(
        label="Số lượng",
        placeholder="Nhập số lượng (Ví dụ: 1, 2, 3...)",
        default="1",
        min_length=1,
        max_length=5
    )

    def __init__(self, ticket_type: str, category_key: str, product_name: str, unit_price: int):
        super().__init__()
        self.ticket_type = ticket_type
        self.category_key = category_key
        self.product_name = product_name
        self.unit_price = unit_price

    async def on_submit(self, interaction: discord.Interaction):
        try:
            qty = int(self.quantity.value)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            await interaction.response.send_message("❌ Số lượng phải là một số nguyên lớn hơn 0!", ephemeral=True)
            return

        total_price = self.unit_price * qty
        rand_digits = "".join(random.sample("0123456789", 6))
        
        if self.ticket_type == "mua-acc":
            add_info = f"MUA {rand_digits} {interaction.user.name}"
        else:
            add_info = f"RANDOM {rand_digits} {interaction.user.name}"
            
        order_code = f"#TT-UDF{rand_digits}-{interaction.user.name}"

        encoded_account_name = urllib.parse.quote(ACCOUNT_NAME)
        encoded_add_info = urllib.parse.quote(add_info)
        
        qr_url = f"https://img.vietqr.io/image/{BANK_ID}-{BANK_ACCOUNT}-compact2.png?amount={total_price}&addInfo={encoded_add_info}&accountName={encoded_account_name}"
        current_time_str = datetime.now(VN_TZ).strftime("%d/%m/%Y lúc %H:%M:%S")

        embed = discord.Embed(
            title="💳 THÔNG TIN THANH TOÁN ĐƠN HÀNG",
            description=(
                f"🏷️ Mã đơn hàng: **{order_code}**\n"
                f"🛒 Sản phẩm: **{self.product_name}**\n"
                f"📦 Số lượng: **{qty}**\n"
                f"💵 Đơn giá: **{self.unit_price:,} VNĐ**\n"
                f"⏱️ Thời gian tạo: `{current_time_str}`"
            ).replace(",", "."),
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Tổng tiền cần thanh toán", value=f"**{total_price:,} VNĐ**".replace(",", "."), inline=False)
        embed.add_field(name="🏦 Ngân hàng", value=f"`{BANK_ID}`", inline=True)
        embed.add_field(name="🔢 Số tài khoản", value=f"`{BANK_ACCOUNT}`", inline=True)
        embed.add_field(name="👤 Chủ tài khoản", value=f"`{ACCOUNT_NAME}`", inline=True)
        embed.add_field(name="📝 Nội dung chuyển khoản", value=f"`{add_info}`", inline=False)
        embed.set_image(url=qr_url)
        embed.set_footer(text="Hệ thống tự động tạo mã QR. Vui lòng chuyển khoản đúng nội dung để nhận tài khoản tự động!")

        await interaction.response.send_message(embed=embed)

        guide_text = (
            "📌 **HƯỚNG DẪN THANH TOÁN:**\n"
            "• **Đối với thông tin thanh toán:** Khách hàng có thể sao chép Số tài khoản, Ngân hàng và Nội dung chuyển khoản.\n"
            "• **Đối với quét mã QR:** Khách hàng có thể sử dụng chức năng Scan QR của ngân hàng để chuyển."
        )
        await interaction.channel.send(guide_text)

        manager_channel = interaction.guild.get_channel(MANAGER_CHANNEL_ID)
        if manager_channel:
            admin_embed = discord.Embed(
                title="🔔 CÓ ĐƠN HÀNG MỚI CHỜ XÁC NHẬN",
                description=(
                    f"👤 Khách hàng: {interaction.user.mention} (`{interaction.user}`)\n"
                    f"🎟️ Kênh Ticket: {interaction.channel.mention}\n"
                    f"🏷️ Mã đơn hàng: **{order_code}**\n"
                    f"🛒 Sản phẩm: **{self.product_name}**\n"
                    f"📦 Số lượng: **{qty}**\n"
                    f"💰 Tổng tiền: **{total_price:,} VNĐ**\n"
                    f"📝 Nội dung CK: `{add_info}`\n"
                    f"⏱️ Thời gian: `{current_time_str}`"
                ).replace(",", "."),
                color=discord.Color.blue()
            )
            admin_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            admin_view = AdminActionView(interaction.channel.id, interaction.user, order_code, self.product_name, qty, total_price, self.ticket_type)
            await manager_channel.send(embed=admin_embed, view=admin_view)

class PriceSelect(discord.ui.Select):
    def __init__(self, ticket_type: str, category_key: str):
        self.ticket_type = ticket_type
        self.category_key = category_key
        
        data_source = BUY_CATEGORIES_DATA if ticket_type == "mua-acc" else RANDOM_CATEGORIES_DATA
        prices = data_source[category_key]["prices"]
        dropdown_emoji = "💎" if ticket_type == "mua-acc" else "🎲"
        
        options = [
            discord.SelectOption(label=label, value=str(price), description=desc, emoji=dropdown_emoji)
            for label, price, desc in prices
        ]
        super().__init__(placeholder="👉 Chọn mức giá sản phẩm muốn...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        unit_price = int(self.values[0])
        selected_label = "Sản phẩm"
        
        data_source = BUY_CATEGORIES_DATA if self.ticket_type == "mua-acc" else RANDOM_CATEGORIES_DATA
        for label, price, desc in data_source[self.category_key]["prices"]:
            if price == unit_price:
                selected_label = f"{label}"
                break
        
        modal = QuantityModal(self.ticket_type, self.category_key, selected_label, unit_price)
        await interaction.response.send_modal(modal)

class PriceSelectView(discord.ui.View):
    def __init__(self, ticket_type: str, category_key: str):
        super().__init__(timeout=60)
        self.add_item(PriceSelect(ticket_type, category_key))

class CategoryButton(discord.ui.Button):
    def __init__(self, ticket_type: str, category_key: str, category_info: dict):
        super().__init__(
            label=category_info["name"],
            emoji=category_info["emoji"],
            style=category_info["style"]
        )
        self.ticket_type = ticket_type
        self.category_key = category_key

    async def callback(self, interaction: discord.Interaction):
        data_source = BUY_CATEGORIES_DATA if self.ticket_type == "mua-acc" else RANDOM_CATEGORIES_DATA
        view = PriceSelectView(self.ticket_type, self.category_key)
        await interaction.response.send_message(
            f"🎯 Bạn đã chọn **{data_source[self.category_key]['name']}**. Vui lòng chọn mức giá bên dưới:",
            view=view,
            ephemeral=True
        )

class CategoryButtonsView(discord.ui.View):
    def __init__(self, ticket_type: str):
        super().__init__(timeout=None)
        data_source = BUY_CATEGORIES_DATA if ticket_type == "mua-acc" else RANDOM_CATEGORIES_DATA
        for cat_key, cat_info in data_source.items():
            self.add_item(CategoryButton(ticket_type, cat_key, cat_info))

class ConfirmCloseView(discord.ui.View):
    def __init__(self, channel_to_close: discord.TextChannel):
        super().__init__(timeout=30)
        self.channel_to_close = channel_to_close

    @discord.ui.button(label="🔒 Đồng ý đóng Ticket", style=discord.ButtonStyle.danger)
    async def confirm_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Kênh này sẽ tự động đóng sau 3 giây...")
        await asyncio.sleep(3)
        try:
            await self.channel_to_close.delete()
        except:
            pass

    @discord.ui.button(label="❌ Không", style=discord.ButtonStyle.grey)
    async def cancel_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Đã hủy thao tác đóng ticket.", view=None)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Đóng Ticket", style=discord.ButtonStyle.danger, custom_id="btn_close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        confirm_view = ConfirmCloseView(interaction.channel)
        await interaction.response.send_message("⚠️ Bạn có chắc chắn muốn đóng ticket này không?", view=confirm_view, ephemeral=True)

class ConfirmTicketView(discord.ui.View):
    def __init__(self, ticket_type: str):
        super().__init__(timeout=60)
        self.ticket_type = ticket_type

    @discord.ui.button(label="✅ Xác nhận tạo", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="🔄 Đang khởi tạo ticket riêng cho bạn, vui lòng đợi giây lát...", view=None)
        
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        
        existing_channel = discord.utils.get(guild.text_channels, name=f"{self.ticket_type}-{interaction.user.name.lower()}")
        if existing_channel:
            await interaction.edit_original_response(content=f"❌ Bạn đã có một ticket đang mở tại {existing_channel.mention} rồi!")
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        try:
            ticket_channel = await guild.create_text_channel(
                name=f"{self.ticket_type}-{interaction.user.name}",
                category=category if isinstance(category, discord.CategoryChannel) else None,
                overwrites=overwrites
            )

            title_text = "🛒 HỆ THỐNG MUA ACCOUNT" if self.ticket_type == "mua-acc" else "🎲 HỆ THỐNG RANDOM ACCOUNT"
            embed = discord.Embed(
                title=title_text,
                description=f"Chào {interaction.user.mention},\nVui lòng chọn loại sản phẩm bạn muốn bằng các nút bên dưới để chọn mức giá và nhập số lượng nhé!",
                color=discord.Color.gold()
            )
            
            category_view = CategoryButtonsView(self.ticket_type)
            close_view = CloseTicketView()
            
            await ticket_channel.send(content=f"{interaction.user.mention}", embed=embed, view=category_view)
            await ticket_channel.send(view=close_view)
            
            await interaction.edit_original_response(content=f"✅ Tạo ticket thành công! Hãy vào kênh của bạn tại: {ticket_channel.mention}")
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ Có lỗi xảy ra khi tạo kênh: `{e}`")

    @discord.ui.button(label="❌ Hủy", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Đã hủy yêu cầu tạo ticket.", view=None)

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛒 Mua Account", style=discord.ButtonStyle.green, custom_id="btn_buy_acc_panel")
    async def buy_account(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmTicketView("mua-acc")
        await interaction.response.send_message("🔔 Bạn có chắc chắn muốn mở ticket **Mua Account** không? Hãy bấm xác nhận bên dưới.", view=view, ephemeral=True)

    @discord.ui.button(label="🎲 Random Account", style=discord.ButtonStyle.blurple, custom_id="btn_random_acc_panel")
    async def random_account(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmTicketView("random-acc")
        await interaction.response.send_message("🔔 Bạn có chắc chắn muốn mở ticket **Random Account** không? Hãy bấm xác nhận bên dưới.", view=view, ephemeral=True)

@bot.command(name="rd")
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="🛡️ HỆ THỐNG BÁN LẺ TÀI NGUYÊN MẠNG XÃ HỘI & RANDOM **UDF SHOP**",
        description=(
            "Chuyên Cung Cấp Các Loại Tài Khoản Standard, Pro, Premium, Ultra,.. Cho Các Trang Mạng Xã Hội Với Mục Đích Nâng Cao Trải Nghiệm Người Dùng.\n\n"
            "- UDF Bot chỉ cung cấp tài nguyên mạng xã hội phục vụ cho nhu cầu cao hơn của người dùng.\n"
            "- Chúng tôi cam kết không cung cấp các thông tin hoặc dữ liệu **KHÔNG HỢP PHÁP** của bất kì ai."
        ),
        color=discord.Color.blue()
    )
    embed.set_image(url="https://i.ibb.co/DgQh207Y/07-C69-D4-F-D3-DA-48-FA-B0-DD-3-AA23-EE87-C28.gif")
    
    view = TicketPanelView()
    await ctx.send(embed=embed, view=view)
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command(name="done")
@commands.has_permissions(administrator=True)
async def ticket_done(ctx):
    if not (ctx.channel.name.startswith("mua-acc-") or ctx.channel.name.startswith("random-acc-")):
        await ctx.send("❌ Lệnh này chỉ có thể sử dụng bên trong các kênh ticket giao dịch!", delete_after=5)
        try:
            await ctx.message.delete()
        except:
            pass
        return

    await ctx.send("🔒 Giao dịch hoàn tất! Kênh này sẽ tự động đóng sau 3 giây...")
    try:
        await ctx.message.delete()
    except:
        pass
    await asyncio.sleep(3)
    try:
        await ctx.channel.delete()
    except:
        pass

# KHỞI CHẠY WEB SERVER VÀ BOT
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)