import discord
from discord.ext import commands
import asyncio
import urllib.parse
import random
from datetime import datetime, timedelta
import os
# --- CẤU HÌNH BOT ---
TOKEN = os.getenv("DISCORD_TOKEN")

WELCOME_CHANNEL_ID = 1379468628549963899  
GOODBYE_CHANNEL_ID = 1449415666233774102  
TICKET_CATEGORY_ID = 1483484606735974491  
MANAGER_CHANNEL_ID = 1535624430699417681  # <--- THAY ID KÊNH MANAGER (QUẢN LÝ) CỦA ADMIN VÀO ĐÂY

# --- CẤU HÌNH THÔNG TIN THANH TOÁN (THAY THÔNG TIN CỦA BẠN VÀO ĐÂY) ---
BANK_ID = "MB"          # Mã ngân hàng (Ví dụ: MB, VCB, TCB, ACB, BIDV,...)
BANK_ACCOUNT = "999999999498"  # Số tài khoản ngân hàng của bạn
ACCOUNT_NAME = "NGUYEN THANH TUAN" # Tên chủ tài khoản (Viết không dấu)

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
            
        ]
    },
    "acc-youtube-premium": {
        "name": "Mua Tài Khoản Youtube Premium",
        "emoji": "🛒",
        "style": discord.ButtonStyle.primary,
        "prices": [

        ]
    },
    "acc-tiktok-clone": {
            "name": "Mua Tài Khoản TikTok Clone",
            "emoji": "🛒",
            "style": discord.ButtonStyle.primary,
            "prices": [
    
            ]
    },
    "acc-gmail-clone": {
            "name": "Mua Tài Khoản Gmail (Reg Trên 1 Tháng)",
            "emoji": "🛒",
            "style": discord.ButtonStyle.primary,
            "prices": [
                
            ]
    }
}

# --- CẤU HÌNH DANH MỤC RANDOM ACCOUNT ---
RANDOM_CATEGORIES_DATA = {
    "random-facebook-co": {
        "name": "Random Tài Khoản Facebook Cổ (2012-2022)",
        "emoji": "🎲",
        "style": discord.ButtonStyle.primary,
        "prices": [

        ]
    },
    "random-facebook-co": {
        "name": "Random Tài Khoản Facebook Cổ (2008-2016)",
        "emoji": "🎲",
        "style": discord.ButtonStyle.primary,
        "prices": [

        ]
    },
    "random-facebook": {
        "name": "Random Tài Khoản TikTok US",
        "emoji": "🎲",
        "style": discord.ButtonStyle.primary,
        "prices": [

        ]
    }
}

intents = discord.Intents.default()
intents.members = True  
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

welcome_channels = {}
goodbye_channels = {}

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập thành công với tên: {bot.user}")

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


# ==========================================
# TÍNH NĂNG 1: CHÀO MỪNG & TẠM BIỆT
# ==========================================

@bot.event
async def on_member_join(member):
    channel_id = welcome_channels.get(member.guild.id, WELCOME_CHANNEL_ID)
    channel = member.guild.get_channel(channel_id)
    
    if channel:
        # Lấy thời gian thực tại thời điểm thành viên tham gia
        current_time_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")
        
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
        
        # Đưa thời gian thực vào footer của Embed
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
    def __init__(self, ticket_channel_id: int, customer: discord.User, product_name: str, quantity: int, total_price: int, order_code: str):
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.order_code = order_code

        options = [
            discord.SelectOption(label="Không bảo hành", value="0", description="Sản phẩm không áp dụng bảo hành", emoji="❌")
        ] + [
            discord.SelectOption(label=f"Bảo hành {i} tháng", value=str(i), description=f"Thời hạn bảo hành {i} tháng", emoji="🛡️")
            for i in range(1, 13)
        ]
        super().__init__(placeholder="👉 Chọn thời gian bảo hành cho sản phẩm...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        months = int(self.values[0])
        now = datetime.now()
        if months == 0:
            expiry_str = "Không bảo hành"
        else:
            expiry_date = now + timedelta(days=months * 30) # Tính thời gian bảo hành thực tế cộng dồn tháng
            expiry_str = expiry_date.strftime("%d/%m/%Y lúc %H:%M:%S")

        modal = AccountInputModal(
            self.ticket_channel_id, 
            self.customer, 
            self.product_name, 
            self.quantity, 
            self.total_price,
            months,
            expiry_str,
            self.order_code
        )
        await interaction.response.send_modal(modal)

class WarrantySelectView(discord.ui.View):
    def __init__(self, ticket_channel_id: int, customer: discord.User, product_name: str, quantity: int, total_price: int, order_code: str):
        super().__init__(timeout=60)
        self.add_item(WarrantySelect(ticket_channel_id, customer, product_name, quantity, total_price, order_code))

class AccountInputModal(discord.ui.Modal, title="Gửi thông tin tài khoản cho khách"):
    username_input = discord.ui.TextInput(label="Tài khoản của bạn", placeholder="Nhập tài khoản...", required=True)
    password_input = discord.ui.TextInput(label="Mật khẩu của bạn", placeholder="Nhập mật khẩu...", required=True)
    two_fa_input = discord.ui.TextInput(label="Mã 2FA (nếu có)", placeholder="Nhập mã 2FA...", required=False)
    token_input = discord.ui.TextInput(label="Token (nếu có)", placeholder="Nhập token...", required=False)
    cookie_input = discord.ui.TextInput(label="Cookie (nếu có)", placeholder="Nhập cookie...", required=False, style=discord.TextStyle.paragraph)

    def __init__(self, ticket_channel_id: int, customer: discord.User, product_name: str, quantity: int, total_price: int, warranty_months: int, expiry_str: str, order_code: str):
        super().__init__()
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.warranty_months = warranty_months
        self.expiry_str = expiry_str
        self.order_code = order_code

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        ticket_channel = guild.get_channel(self.ticket_channel_id)

        if not ticket_channel:
            await interaction.response.send_message("❌ Không tìm thấy kênh ticket của khách hàng này!", ephemeral=True)
            return

        current_time_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")

        warranty_display = f"{self.warranty_months} tháng (Đến {self.expiry_str})" if self.warranty_months > 0 else "Không bảo hành"

        acc_text = (
            f"Cảm ơn bạn đã thanh toán, quý khách vui lòng tiến hành đăng nhập theo thông tin tài khoản được cung cấp bên dưới "
            f"(Nếu gặp bất cứ lỗi nào vui lòng trình bày rõ ở Ticket này để Admin Hoặc Support sẽ giải quyết & bảo hành ngay cho bạn)\n\n"
            f"• **Mã đơn hàng:** `{self.order_code}`\n"
            f"• **Tên sản phẩm:** {self.product_name}\n"
            f"• **Số lượng:** {self.quantity}\n"
            f"• **Giá:** {self.total_price:,} VNĐ\n"
            f"• **Thời gian bảo hành:** {warranty_display}\n"
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
        
        # 1. Gửi thông tin tài khoản vào kênh ticket của khách
        await ticket_channel.send(content=f"{self.customer.mention}", embed=embed)

        # 2. Gửi bản sao thông tin tài khoản vào hộp thư riêng (DM) của khách hàng
        try:
            dm_embed = discord.Embed(
                title="📦 THÔNG TIN TÀI KHOẢN ĐÃ GIAO",
                description=acc_text.replace(",", "."),
                color=discord.Color.green()
            )
            await self.customer.send(embed=dm_embed)
        except Exception:
            pass  # Tránh lỗi nếu khách hàng chặn tin nhắn riêng (DM)

        await interaction.response.send_message("✅ Đã gửi thông tin tài khoản vào ticket và hộp thư riêng (DM) của khách hàng thành công!", ephemeral=True)

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

        current_time_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")
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
    def __init__(self, ticket_channel_id: int, customer: discord.User, order_code: str, product_name: str, quantity: int, total_price: int):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.order_code = order_code
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price

    @discord.ui.button(label="✅ Xác nhận đã nhận tiền", style=discord.ButtonStyle.green, custom_id="btn_admin_confirm_money")
    async def confirm_money(self, interaction: discord.Interaction, button: discord.ui.Button):
        next_view = AdminPostConfirmView(self.ticket_channel_id, self.customer, self.order_code, self.product_name, self.quantity, self.total_price)
        await interaction.message.edit(view=next_view)
        await interaction.response.send_message(f"✅ Đã xác nhận nhận tiền đơn hàng `{self.order_code}`! Bây giờ bạn có thể chọn Gửi tài khoản hoặc Hoàn tiền.", ephemeral=True)

        current_time_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")

        # 1. Thông báo nạp tiền thành công lên kênh ticket kèm ngày giờ thực
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

        # 2. Gửi thông báo nạp tiền thành công về hộp thư riêng (DM) của khách hàng kèm ngày giờ thực
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
    def __init__(self, ticket_channel_id: int, customer: discord.User, order_code: str, product_name: str, quantity: int, total_price: int):
        super().__init__(timeout=None)
        self.ticket_channel_id = ticket_channel_id
        self.customer = customer
        self.order_code = order_code
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price

    @discord.ui.button(label="📦 Gửi tài khoản", style=discord.ButtonStyle.green, custom_id="btn_admin_send_acc")
    async def send_account(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = WarrantySelectView(self.ticket_channel_id, self.customer, self.product_name, self.quantity, self.total_price, self.order_code)
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

        current_time_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")

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
            "• **Đối với thông tin thanh toán:** Khách hàng có thể sao chép Số tài khoản, Ngân hàng và Nội dung chuyển khoản *(Check đúng tên Chủ tài khoản và Nội dung chuyển khoản theo đúng thông tin thanh toán rồi mới xác nhận chuyển)*.\n"
            "• **Đối với quét mã QR:** Khách hàng có thể sử dụng chức năng Scan QR của ngân hàng để chuyển *(Trong mã QR tự động trên thông tin thanh toán đã bao gồm đúng tất cả thông tin, sau khi quét bạn có thể kiểm tra lại và ấn xác nhận chuyển)*."
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
            admin_view = AdminActionView(interaction.channel.id, interaction.user, order_code, self.product_name, qty, total_price)
            await manager_channel.send(embed=admin_embed, view=admin_view)

class PriceSelect(discord.ui.Select):
    def __init__(self, ticket_type: str, category_key: str):
        self.ticket_type = ticket_type
        self.category_key = category_key
        
        data_source = BUY_CATEGORIES_DATA if ticket_type == "mua-acc" else RANDOM_CATEGORIES_DATA
        prices = data_source[category_key]["prices"]
        
        # Tự động thay đổi emoji tùy theo loại ticket: Mua Account dùng 💎, Random Account dùng 🎲
        dropdown_emoji = "💎" if ticket_type == "mua-acc" else "🎲"
        
        options = [
            discord.SelectOption(label=label, value=str(price), description=desc, emoji=dropdown_emoji)
            for label, price, desc in prices
        ]
        super().__init__(placeholder="👉 Chọn mức giá sản phẩm bạn muốn...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        unit_price = int(self.values[0])
        selected_label = "Sản phẩm"
        
        data_source = BUY_CATEGORIES_DATA if self.ticket_type == "mua-acc" else RANDOM_CATEGORIES_DATA
        for label, price, desc in data_source[self.category_key]["prices"]:
            if price == unit_price:
                selected_label = f"{label} ({desc})"
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

@bot.command(name="random")
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

@bot.command(name="ticket_done")
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

bot.run(TOKEN)