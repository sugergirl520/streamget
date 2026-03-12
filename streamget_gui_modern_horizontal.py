import asyncio
import json
import threading
import inspect
import sys
from typing import Dict, Optional, Any, List
import customtkinter as ctk
from tkinter import messagebox, filedialog
import configparser
from pathlib import Path
import subprocess
import os

# 设置现代化主题
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# 自定义颜色方案
COLORS = {
    "primary": "#2C3E50",      # 主色调 - 深蓝灰
    "secondary": "#3498DB",    # 次要色 - 亮蓝
    "accent": "#E74C3C",       # 强调色 - 红色
    "success": "#2ECC71",      # 成功色 - 绿色
    "warning": "#F39C12",      # 警告色 - 橙色
    "light_bg": "#F8F9FA",     # 浅背景
    "card_bg": "#FFFFFF",      # 卡片背景
    "border": "#E9ECEF",       # 边框色
    "text_primary": "#2C3E50", # 主文字
    "text_secondary": "#7F8C8D" # 次文字
}

# ================ StreamGet核心模块 ================
class PlatformConfig:
    PLATFORMS = {
        'douyin': {'url': 'https://live.douyin.com/{room_id}', 'module': 'DouyinLiveStream'},
        'tiktok': {'url': 'https://www.tiktok.com/{room_id}/live', 'module': 'TikTokLiveStream'},
        'ks': {'url': 'https://live.kuaishou.com/u/{room_id}', 'module': 'KwaiLiveStream'},
        'huya': {'url': 'https://www.huya.com/{room_id}', 'module': 'HuyaLiveStream'},
        'douyu': {'url': 'https://www.douyu.com/{room_id}', 'module': 'DouyuLiveStream'},
        'yy': {'url': 'https://www.yy.com/{room_id}', 'module': 'YYLiveStream'},
        'bilibili': {'url': 'https://live.bilibili.com/{room_id}', 'module': 'BilibiliLiveStream'},
        'xhs': {'url': 'https://www.rednote.com/live/{room_id}', 'module': 'RedNoteLiveStream'},
        'bigo': {'url': 'https://www.bigo.tv/cn/{room_id}', 'module': 'BigoLiveStream'},
        'soop': {'url': 'https://play.sooplive.co.kr/{room_id}', 'module': 'SoopLiveStream'},
        'cc': {'url': 'https://cc.163.com/{room_id}', 'module': 'NeteaseLiveStream'},
        'qiandu': {'url': 'https://qiandurebo.com/web/video.php?roomnumber={room_id}', 'module': 'QiandureboLiveStream'},
        'maoer': {'url': 'https://fm.missevan.com/live/{room_id}', 'module': 'MaoerLiveStream'},
        'look': {'url': 'https://look.163.com/live?id={room_id}', 'module': 'LookLiveStream'},
        'wink': {'url': 'https://www.winktv.co.kr/live/play/{room_id}', 'module': 'WinkTVLiveStream'},
        'flex': {'url': 'https://www.ttinglive.com/channels/{room_id}/live', 'module': 'FlexTVLiveStream'},
        'popkon': {'url': 'https://www.popkontv.com/live/view?castId={room_id}&partnerCode=P-00001', 'module': 'PopkonTVLiveStream'},
        'twitcast': {'url': 'https://twitcasting.tv/{room_id}', 'module': 'TwitCastingLiveStream'},
        'baidu': {'url': 'https://live.baidu.com/m/media/pclive/pchome/live.html?room_id={room_id}', 'module': 'BaiduLiveStream'},
        'weibo': {'url': 'https://weibo.com/l/wblive/p/show/1022:{room_id}', 'module': 'WeiboLiveStream'},
        'kugou': {'url': 'https://fanxing.kugou.com/{room_id}', 'module': 'KugouLiveStream'},
        'twitch': {'url': 'https://www.twitch.tv/{room_id}', 'module': 'TwitchLiveStream'},
        'liveme': {'url': 'https://www.liveme.com/zh/v/{room_id}', 'module': 'LiveMeLiveStream'},
        'huajiao': {'url': 'https://www.huajiao.com/l/{room_id}', 'module': 'HuajiaoLiveStream'},
        'showroom': {'url': 'https://www.showroom-live.com/room/profile?room_id={room_id}', 'module': 'ShowRoomLiveStream'},
        'acfun': {'url': 'https://live.acfun.cn/live/{room_id}', 'module': 'AcfunLiveStream'},
        'inke': {'url': 'https://www.inke.cn/liveroom/index.html?uid=22954469&id={room_id}', 'module': 'InkeLiveStream'},
        'yinbo': {'url': 'https://live.ybw1666.com/{room_id}', 'module': 'YinboLiveStream'},
        'zhihu': {'url': 'https://www.zhihu.com/people/{room_id}', 'module': 'ZhihuLiveStream'},
        'cuzzk': {'url': 'https://chzzk.naver.com/live/{room_id}', 'module': 'ChzzkLiveStream'},
        'haixiu': {'url': 'https://www.haixiutv.com/{room_id}', 'module': 'HaixiuLiveStream'},
        'vvxq': {'url': 'https://h5webcdn-pro.vvxqiu.com//activity/videoShare/videoShare.html?h5Server=https://h5p.vvxqiu.com&roomId={room_id}', 'module': 'VVXQLiveStream'},
        '17live': {'url': 'https://17.live/en/live/{room_id}', 'module': 'YiqiLiveStream'},
        'langlive': {'url': 'https://www.lang.live/en-US/room/{room_id}', 'module': 'LangLiveLiveStream'},
        'piaopiao': {'url': 'https://m.pp.weimipopo.com/live/preview.html?uid=91648673&anchorUid={room_id}', 'module': 'PiaopaioLiveStream'},
        'sixroom': {'url': 'https://v.6.cn/{room_id}', 'module': 'SixRoomLiveStream'},
        'lehai': {'url': 'https://www.lehaitv.com/{room_id}', 'module': 'LehaiLiveStream'},
        'huamao': {'url': 'https://h.catshow168.com/live/preview.html?uid=19066357&anchorUid={room_id}', 'module': 'HuamaoLiveStream'},
        'shopee': {'url': 'https://sg.shp.ee/GmpXeuf?uid=1006401066&session={room_id}', 'module': 'ShopeeLiveStream'},
        'youtube': {'url': 'https://www.youtube.com/watch?v={room_id}', 'module': 'YoutubeLiveStream'},
        'taobao': {'url': 'https://m.tb.cn/{room_id}', 'module': 'TaobaoLiveStream'},
        'jd': {'url': 'https://3.cn/{room_id}', 'module': 'JDLiveStream'},
        'faceit': {'url': 'https://www.faceit.com/zh/players/{room_id}', 'module': 'FaceitLiveStream'},
        'blued': {'url': 'https://app.blued.cn/live?id={room_id}', 'module': 'BluedLiveStream'},
    }

    @classmethod
    def get_config(cls, platform: str) -> Dict[str, str]:
        platform = platform.lower()
        if platform not in cls.PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        return cls.PLATFORMS[platform]

    @classmethod
    def get_url_template(cls, platform: str) -> str:
        return cls.get_config(platform)['url']

    @classmethod
    def get_class_name(cls, platform: str) -> str:
        return cls.get_config(platform)['module']

    @classmethod
    def get_supported_platforms(cls) -> list:
        return list(cls.PLATFORMS.keys())

class PlatformLoader:
    @staticmethod
    def load_class(platform: str):
        class_name = PlatformConfig.get_class_name(platform)
        try:
            module = __import__('streamget')
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(
                f"Platform module not found: {class_name}"
            ) from e

    @staticmethod
    def create_instance(platform: str, proxy: Optional[str] = None) -> Any:
        cls = PlatformLoader.load_class(platform)
        sig = inspect.signature(cls.__init__)

        params = {}
        if proxy:
            if 'proxy' in sig.parameters:
                params['proxy'] = proxy
            elif 'proxy_addr' in sig.parameters:
                params['proxy_addr'] = proxy
        
        if platform == 'douyin' and 'stream_orientation' in sig.parameters:
            params['stream_orientation'] = 1

        return cls(**params)

class StreamFetcher:
    @staticmethod
    async def fetch(platform: str, room_id: str, proxy: Optional[str] = None) -> str:
        instance = PlatformLoader.create_instance(platform, proxy)
        url_template = PlatformConfig.get_url_template(platform)
        url = url_template.format(room_id=room_id)
        web_data = await instance.fetch_web_stream_data(url)
        stream_obj = await instance.fetch_stream_url(web_data, "OD")
        return stream_obj.to_json()

class OutputFormatter:
    URL_KEYS = ['flv_url', 'm3u8_url', 'record_url', 'rtmp_url']

    @staticmethod
    def format_response(json_data: str, platform: str, room_id: str) -> bytes:
        data = json.loads(json_data)
        urls = []
        seen = set()

        platform_name = data.get("platform", platform)
        
        for key in OutputFormatter.URL_KEYS:
            if key in data and data[key] and data[key] not in seen:
                urls.append({"url": data[key]})
                seen.add(data[key])

        extra = data.get("extra", {})
        if isinstance(extra, dict):
            backup_list = extra.get("backup_url_list", [])
            if isinstance(backup_list, list):
                for url in backup_list:
                    if isinstance(url, str) and url and url not in seen:
                        urls.append({"url": url})
                        seen.add(url)

        return json.dumps({
            "platform": platform_name,
            "rid": room_id,
            "title": data.get("title", ""),
            "anchor": data.get("anchor_name", ""),
            "urls": urls
        }, indent=2, ensure_ascii=False).encode('utf-8')

# ================ 配置管理器模块 ================
class ConfigManager:
    def __init__(self):
        self.config_file = Path(__file__).parent / "streamget_config.ini"
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        if not self.config_file.exists():
            self.create_default_config()
        self.config.read(self.config_file, encoding='utf-8')
    
    def create_default_config(self):
        self.config['PLAYER'] = {
            'vlc_path': '',
            'potplayer_path': '',
            'mpv_path': '',
            'default_player': 'vlc'
        }
        self.config['FONT'] = {
            'size': '11'
        }
        self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_player_path(self, player_name):
        return self.config.get('PLAYER', f'{player_name}_path', fallback='')
    
    def set_player_path(self, player_name, path):
        self.config.set('PLAYER', f'{player_name}_path', path)
        self.save_config()
    
    def get_default_player(self):
        return self.config.get('PLAYER', 'default_player', fallback='vlc')
    
    def set_default_player(self, player_name):
        self.config.set('PLAYER', 'default_player', player_name)
        self.save_config()
    
    def get_font_size(self):
        try:
            return int(self.config.get('FONT', 'size', fallback='11'))
        except:
            return 11
    
    def set_font_size(self, size):
        self.config.set('FONT', 'size', str(size))
        self.save_config()

# ================ 播放器控制器模块 ================
class PlayerController:
    def __init__(self, config_manager):
        self.config = config_manager
    
    def play_url(self, url):
        try:
            default_player = self.config.get_default_player()
            player_path = self.config.get_player_path(default_player)
            
            if not player_path or not os.path.exists(player_path):
                if messagebox.askyesno("提示", f"{default_player.upper()}播放器路径未设置，是否现在设置？"):
                    return False
                return False
            
            if default_player == "vlc":
                cmd = f'"{player_path}" "{url}"'
            elif default_player == "potplayer":
                cmd = f'"{player_path}" "{url}"'
            elif default_player == "mpv":
                cmd = f'"{player_path}" "{url}"'
            else:
                cmd = f'"{player_path}" "{url}"'
            
            def run_play():
                try:
                    subprocess.Popen(cmd, shell=True)
                except Exception as e:
                    messagebox.showerror("错误", f"播放失败: {str(e)}")
            
            thread = threading.Thread(target=run_play, daemon=True)
            thread.start()
            return True
            
        except Exception as e:
            messagebox.showerror("错误", f"播放失败: {str(e)}")
            return False

# ================ StreamGet执行器模块 ================
class StreamGetExecutor:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
    
    async def execute_async(self, platform, room_id):
        try:
            json_data = await StreamFetcher.fetch(platform, room_id)
            formatted_bytes = OutputFormatter.format_response(json_data, platform, room_id)
            return json.loads(formatted_bytes.decode('utf-8')), None
        except Exception as e:
            return None, f"执行出错: {str(e)}"
    
    def execute_sync(self, platform, room_id):
        try:
            return asyncio.run(self.execute_async(platform, room_id))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(self.execute_async(platform, room_id))
            finally:
                loop.close()

# ================ 现代化的设置对话框 ================
class SettingsDialog:
    def __init__(self, parent, config_manager, update_callback=None):
        self.parent = parent
        self.config = config_manager
        self.update_callback = update_callback
        self.font_size = self.config.get_font_size()
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title("设置")
        self.window.geometry("750x550")
        self.window.configure(fg_color=COLORS["light_bg"])
        self.center_window()
        self.window.grab_set()
        self.setup_ui()
    
    def center_window(self):
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        x = parent_x + (parent_width - 750) // 2
        y = parent_y + (parent_height - 550) // 2
        
        self.window.geometry(f"750x550+{x}+{y}")
    
    def setup_ui(self):
        main_container = ctk.CTkFrame(
            self.window, 
            fg_color=COLORS["light_bg"],
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        header_frame = ctk.CTkFrame(
            main_container,
            fg_color=COLORS["primary"],
            height=60,
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙ 设置",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=25, pady=0)
        
        content_frame = ctk.CTkFrame(
            main_container,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tabs = ctk.CTkTabview(
            content_frame,
            fg_color=COLORS["card_bg"],
            segmented_button_fg_color=COLORS["primary"],
            segmented_button_selected_color=COLORS["secondary"],
            segmented_button_selected_hover_color=COLORS["secondary"],
            text_color="white",
            segmented_button_unselected_color=COLORS["primary"],
            segmented_button_unselected_hover_color=COLORS["text_primary"],
            corner_radius=8
        )
        tabs.pack(fill="both", expand=True, padx=0, pady=0)
        
        player_tab = tabs.add("🎮 播放器设置")
        font_tab = tabs.add("🔤 字体设置")
        
        self.setup_player_tab(player_tab)
        self.setup_font_tab(font_tab)
        
        button_frame = ctk.CTkFrame(
            main_container,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack(expand=True)
        
        cancel_btn = ctk.CTkButton(
            button_container,
            text="取消",
            command=self.window.destroy,
            height=40,
            width=120,
            font=ctk.CTkFont(size=max(self.font_size, 10)),
            fg_color=COLORS["border"],
            hover_color="#D6D8DB",
            text_color=COLORS["text_primary"],
            corner_radius=6
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            button_container,
            text="💾 保存设置",
            command=self.save_settings,
            height=40,
            width=120,
            font=ctk.CTkFont(size=max(self.font_size, 10), weight="bold"),
            fg_color=COLORS["success"],
            hover_color="#27AE60",
            text_color="white",
            corner_radius=6
        )
        save_btn.pack(side="left")
    
    def setup_player_tab(self, tab):
        tab.configure(fg_color=COLORS["card_bg"])
        
        default_player_frame = ctk.CTkFrame(
            tab,
            fg_color=COLORS["card_bg"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        default_player_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        section_title = ctk.CTkLabel(
            default_player_frame,
            text="🎯 选择默认播放器",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS["primary"]
        )
        section_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.player_var = ctk.StringVar(value=self.config.get_default_player())
        players = [("vlc", "🎬 VLC"), ("potplayer", "▶ PotPlayer"), ("mpv", "🎵 MPV")]
        
        radio_container = ctk.CTkFrame(default_player_frame, fg_color="transparent")
        radio_container.pack(fill="x", padx=20, pady=(0, 15))
        
        for i, (player_id, player_name) in enumerate(players):
            radio_frame = ctk.CTkFrame(radio_container, fg_color="transparent")
            radio_frame.pack(side="left", padx=(0, 20))
            
            radio = ctk.CTkRadioButton(
                radio_frame,
                text=player_name,
                variable=self.player_var,
                value=player_id,
                font=ctk.CTkFont(size=max(self.font_size-1, 10)),
                radiobutton_width=16,
                radiobutton_height=16,
                fg_color=COLORS["secondary"],
                hover_color=COLORS["secondary"],
                border_color=COLORS["text_secondary"],
                text_color=COLORS["text_primary"]
            )
            radio.pack(side="left", padx=(0, 5))
        
        path_frame = ctk.CTkFrame(
            tab,
            fg_color=COLORS["card_bg"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        path_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        section_title = ctk.CTkLabel(
            path_frame,
            text="📁 播放器路径设置",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS["primary"]
        )
        section_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.path_entries = {}
        
        for player_id, player_name in players:
            player_row = ctk.CTkFrame(path_frame, fg_color="transparent")
            player_row.pack(fill="x", padx=20, pady=(0, 10))
            
            label_container = ctk.CTkFrame(player_row, fg_color="transparent", width=120)
            label_container.pack(side="left")
            label_container.pack_propagate(False)
            
            ctk.CTkLabel(
                label_container,
                text=f"{player_name.split(' ')[-1]}:",
                font=ctk.CTkFont(size=max(self.font_size-1, 10)),
                text_color=COLORS["text_primary"]
            ).pack(anchor="w")
            
            input_container = ctk.CTkFrame(player_row, fg_color="transparent")
            input_container.pack(side="left", fill="x", expand=True, padx=(10, 0))
            
            path_var = ctk.StringVar(value=self.config.get_player_path(player_id))
            entry = ctk.CTkEntry(
                input_container,
                textvariable=path_var,
                placeholder_text="点击浏览选择播放器路径...",
                height=36,
                font=ctk.CTkFont(size=max(self.font_size-1, 10)),
                fg_color="white",
                border_color=COLORS["border"],
                border_width=1,
                corner_radius=4
            )
            entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            browse_btn = ctk.CTkButton(
                input_container,
                text="浏览",
                width=80,
                height=36,
                font=ctk.CTkFont(size=max(self.font_size-1, 10)),
                fg_color=COLORS["secondary"],
                hover_color="#2980B9",
                command=lambda e=entry: self.browse_player_path(e)
            )
            browse_btn.pack(side="right")
            
            self.path_entries[player_id] = (entry, path_var)
    
    def setup_font_tab(self, tab):
        tab.configure(fg_color=COLORS["card_bg"])
        
        font_frame = ctk.CTkFrame(
            tab,
            fg_color=COLORS["card_bg"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        font_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        section_title = ctk.CTkLabel(
            font_frame,
            text="🔤 字体大小设置",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS["primary"]
        )
        section_title.pack(anchor="w", padx=20, pady=(20, 20))
        
        input_frame = ctk.CTkFrame(font_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            input_frame,
            text="字体大小:",
            font=ctk.CTkFont(size=max(self.font_size, 11), weight="bold"),
            text_color=COLORS["text_primary"],
            width=80
        ).pack(side="left", padx=(0, 10))
        
        current_size = self.config.get_font_size()
        self.font_size_var = ctk.StringVar(value=str(current_size))
        
        self.font_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.font_size_var,
            width=80,
            height=36,
            font=ctk.CTkFont(size=max(self.font_size, 11)),
            fg_color="white",
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=4,
            justify="center"
        )
        self.font_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            input_frame,
            text="(建议范围: 8-16)",
            font=ctk.CTkFont(size=max(self.font_size-1, 10)),
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        preview_container = ctk.CTkFrame(font_frame, fg_color="transparent")
        preview_container.pack(fill="x", padx=20, pady=(0, 20))
        
        preview_label = ctk.CTkLabel(
            preview_container,
            text="字体预览:",
            font=ctk.CTkFont(size=max(self.font_size, 11), weight="bold"),
            text_color=COLORS["text_primary"]
        )
        preview_label.pack(anchor="w", pady=(0, 10))
        
        preview_frame = ctk.CTkFrame(
            preview_container,
            fg_color="#F8F9FA",
            corner_radius=6,
            border_width=1,
            border_color=COLORS["border"],
            height=100
        )
        preview_frame.pack(fill="x")
        preview_frame.pack_propagate(False)
        
        preview_text = "🎯 StreamGet 直播获取工具 - 这是字体大小的预览文本"
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text=preview_text,
            font=ctk.CTkFont(family="Segoe UI", size=current_size),
            text_color=COLORS["text_primary"],
            wraplength=600
        )
        self.preview_label.pack(expand=True, padx=20, pady=20)
        
        self.font_entry.bind("<KeyRelease>", self.update_font_preview)
    
    def update_font_preview(self, event):
        try:
            size = int(self.font_size_var.get())
            if 8 <= size <= 20:
                self.preview_label.configure(font=ctk.CTkFont(family="Segoe UI", size=size))
        except:
            pass
    
    def browse_player_path(self, entry):
        file_types = [("可执行文件", "*.exe"), ("所有文件", "*.*")]
        
        file_path = filedialog.askopenfilename(
            title="选择播放器路径",
            filetypes=file_types
        )
        
        if file_path:
            entry.delete(0, "end")
            entry.insert(0, file_path)
    
    def save_settings(self):
        try:
            for player_id, (entry, var) in self.path_entries.items():
                path = var.get().strip()
                if path and os.path.exists(path):
                    self.config.set_player_path(player_id, path)
            
            self.config.set_default_player(self.player_var.get())
            
            try:
                font_size = int(self.font_size_var.get())
                if 8 <= font_size <= 20:
                    self.config.set_font_size(font_size)
                else:
                    raise ValueError("字体大小超出范围")
            except:
                messagebox.showwarning("警告", "字体大小应在8-20之间，使用默认值")
                self.config.set_font_size(11)
            
            messagebox.showinfo("成功", "设置已保存，部分设置需要重启程序生效")
            
            if self.update_callback:
                self.update_callback()
                
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存设置时出错: {str(e)}")

# ================ 现代化的流地址对话框 ================
class StreamUrlDialog:
    def __init__(self, parent, url_data, room_info, config_manager):
        self.parent = parent
        self.url_data = url_data
        self.room_info = room_info
        self.config = config_manager
        self.font_size = self.config.get_font_size()
        self.player_controller = PlayerController(config_manager)
        
        url_count = len(url_data.get("urls", []))
        base_height = 220
        row_height = 80
        height = min(base_height + url_count * row_height, 600)
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title(self.get_window_title())
        self.window.geometry(f"900x{height}")
        self.window.configure(fg_color=COLORS["light_bg"])
        
        self.center_window()
        self.window.grab_set()
        self.setup_ui()
    
    def get_window_title(self):
        anchor = self.room_info.get('anchor', '')
        rid = self.room_info.get('rid', '')
        title = self.room_info.get('title', '')
        
        title_parts = []
        
        if anchor and rid:
            title_parts.append(f"主播：{anchor}－房间号：{rid}")
        elif anchor:
            title_parts.append(f"主播：{anchor}")
        elif rid:
            title_parts.append(f"房间号：{rid}")
        
        if title:
            if title_parts:
                title_parts.append(f"      {title}")
            else:
                title_parts.append(title)
        
        if not title_parts:
            return "🎯 流地址"
        else:
            return "🎯 " + "".join(title_parts)
    
    def center_window(self):
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 900
        url_count = len(self.url_data.get("urls", []))
        base_height = 220
        row_height = 80
        height = min(base_height + url_count * row_height, 600)
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color=COLORS["light_bg"]
        )
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["primary"],
            height=80,
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=15)
        
        anchor = self.room_info.get('anchor', '')
        rid = self.room_info.get('rid', '')
        
        if anchor or rid:
            info_parts = []
            if anchor:
                info_parts.append(f"👤 {anchor}")
            if rid:
                info_parts.append(f"# {rid}")
            
            info_text = " | ".join(info_parts)
            ctk.CTkLabel(
                header_content,
                text=info_text,
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color="white"
            ).pack(anchor="w")
        
        title = self.room_info.get('title', '')
        if title:
            if len(title) > 50:
                title = title[:47] + "..."
            ctk.CTkLabel(
                header_content,
                text=title,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#E0E0E0",
                wraplength=700
            ).pack(anchor="w", pady=(5, 0))
        
        content_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        url_count = len(self.url_data.get("urls", []))
        ctk.CTkLabel(
            title_frame,
            text=f"📡 可用流地址 ({url_count}个)",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(side="left")
        
        scroll_container = ctk.CTkFrame(content_frame, fg_color=COLORS["card_bg"], corner_radius=8)
        scroll_container.pack(fill="both", expand=True)
        
        scroll_frame = ctk.CTkScrollableFrame(scroll_container, height=300)
        scroll_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.display_urls(scroll_frame)
        
        if not self.url_data.get("urls", []):
            ctk.CTkLabel(
                scroll_frame,
                text="📭 无可用流地址",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=COLORS["text_secondary"]
            ).pack(expand=True, pady=50)
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="关闭",
            command=self.window.destroy,
            width=120,
            height=40,
            font=ctk.CTkFont(size=max(self.font_size, 11)),
            fg_color=COLORS["border"],
            hover_color="#D6D8DB",
            text_color=COLORS["text_primary"],
            corner_radius=6
        )
        close_btn.pack(side="right")
    
    def display_urls(self, scroll_frame):
        for i, url_item in enumerate(self.url_data.get("urls", [])):
            url = url_item.get("url", "")
            if not url:
                continue
            self.create_url_row(scroll_frame, i, url, url_item)
    
    def create_url_row(self, parent, index, url, url_item):
        row_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["card_bg"],
            corner_radius=6,
            border_width=1,
            border_color=COLORS["border"]
        )
        row_frame.pack(fill="x", pady=(0, 10), padx=5)
        
        main_container = ctk.CTkFrame(row_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=12)
        
        # 横向布局：标签 + URL + 按钮
        left_section = ctk.CTkFrame(main_container, fg_color="transparent")
        left_section.pack(side="left", fill="y", padx=(0, 15))
        
        # 流标签
        quality = url_item.get("quality", f"流{index+1}")
        label_frame = ctk.CTkFrame(left_section, fg_color="transparent")
        label_frame.pack(side="left", padx=(0, 15))
        
        quality_badge = ctk.CTkFrame(
            label_frame,
            fg_color=COLORS["secondary"],
            corner_radius=4,
            width=60,
            height=36
        )
        quality_badge.pack()
        quality_badge.pack_propagate(False)
        
        ctk.CTkLabel(
            quality_badge,
            text=f" {quality} ",
            font=ctk.CTkFont(size=max(self.font_size-1, 10), weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # URL显示区域
        url_container = ctk.CTkFrame(main_container, fg_color="transparent")
        url_container.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        url_display_frame = ctk.CTkFrame(
            url_container,
            fg_color="#F8F9FA",
            corner_radius=4,
            border_width=1,
            border_color=COLORS["border"],
            height=36
        )
        url_display_frame.pack(fill="both", expand=True)
        
        url_text = ctk.CTkTextbox(
            url_display_frame,
            height=36,
            font=ctk.CTkFont(family="Consolas", size=max(self.font_size-1, 9)),
            wrap="none",
            fg_color="transparent",
            border_width=0
        )
        url_text.pack(fill="both", expand=True, padx=8, pady=6)
        
        display_url = url[:150] + "..." if len(url) > 150 else url
        url_text.insert("1.0", display_url)
        url_text.configure(state="disabled")
        
        # 按钮区域
        button_container = ctk.CTkFrame(main_container, fg_color="transparent")
        button_container.pack(side="right")
        
        # 按钮行
        btn_row = ctk.CTkFrame(button_container, fg_color="transparent")
        btn_row.pack()
        
        copy_btn = ctk.CTkButton(
            btn_row,
            text="📋 复制",
            width=90,
            height=36,
            font=ctk.CTkFont(size=max(self.font_size-1, 10)),
            fg_color=COLORS["secondary"],
            hover_color="#2980B9",
            command=lambda u=url: self.copy_url(u)
        )
        copy_btn.pack(side="left", padx=(0, 8))
        
        play_btn = ctk.CTkButton(
            btn_row,
            text="▶ 播放",
            width=90,
            height=36,
            font=ctk.CTkFont(size=max(self.font_size-1, 10)),
            fg_color=COLORS["success"],
            hover_color="#27AE60",
            command=lambda u=url: self.play_url(u)
        )
        play_btn.pack(side="left")
    
    def copy_url(self, url):
        self.window.clipboard_clear()
        self.window.clipboard_append(url)
        messagebox.showinfo("成功", "✅ URL已复制到剪贴板")
    
    def play_url(self, url):
        if not self.player_controller.play_url(url):
            self.open_settings()
    
    def open_settings(self):
        self.window.withdraw()
        settings_window = SettingsDialog(self.parent, self.config, None)
        self.parent.wait_window(settings_window.window)
        self.window.deiconify()

# ================ 现代化的主应用程序 ================
class MainApplication:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.stream_get_executor = StreamGetExecutor()
        self.player_controller = PlayerController(self.config_manager)
        
        self.window = ctk.CTk()
        self.window.title("🎯 StreamGet 直播获取工具")
        self.window.geometry("800x450")
        self.window.configure(fg_color=COLORS["light_bg"])
        
        self.platforms = {
            "douyu": "🐟 斗鱼",
            "douyin": "🎵 抖音", 
            "huya": "🐯 虎牙",
            "bilibili": "📺 B站",
            "ks": "⚡ 快手"
        }
        
        self.selected_platform = ctk.StringVar(value="douyu")
        self.room_id = ctk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        self.font_size = self.config_manager.get_font_size()
        
        main_container = ctk.CTkFrame(
            self.window,
            fg_color=COLORS["light_bg"]
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        header_frame = ctk.CTkFrame(
            main_container,
            fg_color=COLORS["primary"],
            height=60,
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=0)
        
        title_container = ctk.CTkFrame(header_content, fg_color="transparent")
        title_container.pack(side="left", fill="y", expand=True)
        
        title_label = ctk.CTkLabel(
            title_container,
            text="🎯 StreamGet 直播获取工具",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left")
        
        version_label = ctk.CTkLabel(
            title_container,
            text="v1.0",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#B0BEC5"
        )
        version_label.pack(side="left", padx=(8, 0), pady=(2, 0))
        
        settings_btn = ctk.CTkButton(
            header_content,
            text="⚙ 设置",
            width=80,
            height=34,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=COLORS["secondary"],
            hover_color="#2980B9",
            command=self.open_settings
        )
        settings_btn.pack(side="right")
        
        content_container = ctk.CTkFrame(
            main_container,
            fg_color="transparent"
        )
        content_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        card_frame = ctk.CTkFrame(
            content_container,
            fg_color=COLORS["card_bg"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        card_frame.pack(expand=True, fill="both")
        
        card_content = ctk.CTkFrame(card_frame, fg_color="transparent")
        card_content.pack(expand=True, fill="both", padx=40, pady=30)
        
        platform_section = ctk.CTkFrame(card_content, fg_color="transparent")
        platform_section.pack(fill="x", pady=(0, 25))
        
        platform_label = ctk.CTkLabel(
            platform_section,
            text="📺 选择直播平台",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLORS["primary"]
        )
        platform_label.pack(anchor="w", pady=(0, 12))
        
        platform_row = ctk.CTkFrame(platform_section, fg_color="transparent")
        platform_row.pack()
        
        for i, (platform_key, platform_name) in enumerate(self.platforms.items()):
            radio = ctk.CTkRadioButton(
                platform_row,
                text=platform_name,
                variable=self.selected_platform,
                value=platform_key,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                radiobutton_width=16,
                radiobutton_height=16,
                fg_color=COLORS["secondary"],
                hover_color=COLORS["secondary"],
                border_color=COLORS["text_secondary"],
                text_color=COLORS["text_primary"],
                width=100
            )
            radio.pack(side="left", padx=(0, 15) if i < len(self.platforms)-1 else 0)
        
        input_section = ctk.CTkFrame(card_content, fg_color="transparent")
        input_section.pack(fill="x", pady=(0, 25))
        
        input_label = ctk.CTkLabel(
            input_section,
            text="🔢 输入房间号",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLORS["primary"]
        )
        input_label.pack(anchor="w", pady=(0, 12))
        
        input_container = ctk.CTkFrame(input_section, fg_color="transparent")
        input_container.pack(fill="x")
        
        entry_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        entry_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        self.room_entry = ctk.CTkEntry(
            entry_frame,
            textvariable=self.room_id,
            placeholder_text="请输入房间号，按 Enter 快速获取...",
            height=40,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="white",
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=6
        )
        self.room_entry.pack(fill="x")
        self.room_entry.bind("<Return>", lambda event: self.get_stream_info())
        
        get_button = ctk.CTkButton(
            input_container,
            text="🚀 获取直播信息",
            command=self.get_stream_info,
            height=40,
            width=180,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=COLORS["success"],
            hover_color="#27AE60",
            text_color="white",
            corner_radius=6
        )
        get_button.pack(side="right")
        
        status_section = ctk.CTkFrame(card_content, fg_color="transparent")
        status_section.pack(fill="x", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            status_section,
            text="✨ 准备就绪，请输入房间号开始获取",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(expand=True)
    
    def open_settings(self):
        SettingsDialog(self.window, self.config_manager, self.update_font_sizes)
    
    def update_font_sizes(self):
        self.font_size = self.config_manager.get_font_size()
        self.window.destroy()
        new_app = MainApplication()
        new_app.run()
    
    def update_status(self, message, color=None):
        if color == "red":
            text_color = "#E74C3C"
        elif color == "green":
            text_color = COLORS["success"]
        elif color == "blue":
            text_color = COLORS["secondary"]
        elif color == "orange":
            text_color = COLORS["warning"]
        else:
            text_color = COLORS["text_secondary"]
        
        self.status_label.configure(text=message, text_color=text_color)
    
    def get_stream_info(self):
        room_id = self.room_id.get().strip()
        platform = self.selected_platform.get()
        
        if not room_id:
            self.update_status("❌ 请输入房间号", "red")
            return
        
        self.update_status("⏳ 正在获取直播信息...", "blue")
        
        thread = threading.Thread(
            target=self.execute_streamget,
            args=(platform, room_id)
        )
        thread.daemon = True
        thread.start()
    
    def execute_streamget(self, platform, room_id):
        json_data, error = self.stream_get_executor.execute_sync(platform, room_id)
        
        if error:
            self.window.after(0, lambda: self.update_status(f"❌ {error}", "red"))
            return
        
        anchor = json_data.get("anchor", "")
        urls = json_data.get("urls", [])
        
        valid_urls = []
        for url_item in urls:
            url = url_item.get("url", "")
            if url and isinstance(url, str) and url.strip():
                valid_urls.append(url_item)
        
        if valid_urls:
            if anchor:
                self.window.after(0, lambda: self.update_status(f"✅ 获取成功！{anchor} 正在直播", "green"))
            else:
                self.window.after(0, lambda: self.update_status("✅ 获取成功！正在直播", "green"))
            
            room_info = {
                "anchor": anchor,
                "rid": json_data.get("rid", room_id),
                "title": json_data.get("title", ""),
                "platform": json_data.get("platform", platform)
            }
            
            json_data["urls"] = valid_urls
            self.window.after(0, lambda: self.show_url_dialog(json_data, room_info))
        else:
            if anchor:
                self.window.after(0, lambda: self.update_status(f"⚠️ 获取成功！{anchor} 当前未直播", "orange"))
            else:
                self.window.after(0, lambda: self.update_status("⚠️ 获取成功！当前未直播", "orange"))
            return
    
    def show_url_dialog(self, data, room_info):
        StreamUrlDialog(self.window, data, room_info, self.config_manager)
    
    def run(self):
        self.window.mainloop()

# ================ 主程序入口 ================
if __name__ == "__main__":
    app = MainApplication()
    app.run()
